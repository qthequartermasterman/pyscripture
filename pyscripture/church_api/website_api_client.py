"""This file contains the API client for the Church of Jesus Christ of Latter-day Saints website."""
import asyncio
import warnings
from typing import Type, List, Dict, TypeVar

import pydantic

from pyscripture.church_api import church_schema, uri_mappers
from bs4 import BeautifulSoup
import re

import httpx
from pyscripture import books

BASE_STUDY_CONTENT_URL = "https://www.churchofjesuschrist.org/study/api/v3/language-pages/type/content"
BASE_CONTENT_URL = "https://www.churchofjesuschrist.org/content/api/v3"
STUDY_CONTENT_URL_FORMAT = f"{BASE_STUDY_CONTENT_URL}?lang={{lang}}&uri={{uri}}"
BASE_CONTENT_URL_FORMAT = "/{lang}/scriptures/{parent_book_uri}/{book_uri}/{chapter}.{verse}"

NOTE_ID_REGEX = re.compile(r"note(\d+)(\w+)")

T = TypeVar("T")
def flatten(list_of_lists: list[list[T]]) -> list[T]:
    """Flatten a list of lists into a single list.

    Args:
        list_of_lists: The list of lists to flatten.

    Returns:
        The flattened list.

    Examples:
        >>> flatten([[1, 2, 3], [4, 5, 6]])
        [1, 2, 3, 4, 5, 6]
        >>> flatten([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        [1, 2, 3, 4, 5, 6, 7, 8, 9]

    """
    return [item for sublist in list_of_lists for item in sublist]

def prepare_uri(parent_book: books.ParentBook, book: books.Book, chapter: int) -> str:
    """Prepare the uri for a chapter or verse.

    Args:
        parent_book: The parent book of the chapter or verse.
        book: The book of the chapter or verse.
        chapter: The chapter of the chapter or verse.

    Returns:
        The uri of the chapter or verse.
    """
    if parent_book not in uri_mappers.parent_book_uri_mapper:
        raise ValueError(f"Invalid parent book: {parent_book}")
    parent_book_uri, book_uri_mapper = uri_mappers.parent_book_uri_mapper[parent_book]
    if book not in book_uri_mapper:
        raise ValueError(f"Invalid book: {book}")
    book_uri = book_uri_mapper[book]

    return f"/scriptures/{parent_book_uri}/{book_uri}/{chapter}"


async def get_scripture_content(
    lang: str, parent_book: books.ParentBook, book: books.Book, chapter: int, client: httpx.AsyncClient
) -> church_schema.ScriptureStudyContent:
    """Get the content of a scripture chapter or verse.

    Args:
        lang: The language of the content.
        parent_book: The parent book of the chapter or verse.
        book: The book of the chapter or verse.
        chapter: The chapter of the chapter or verse.

    Returns:
        The content of the chapter or verse.
    """
    uri = prepare_uri(parent_book, book, chapter)
    return await get_scripture_content_from_uri(lang, uri, client)


async def get_scripture_content_from_uri(lang: str, uri: str, client: httpx.AsyncClient) -> church_schema.ScriptureStudyContent:
    url = STUDY_CONTENT_URL_FORMAT.format(lang=lang, uri=uri)
    response = await client.get(url)
    return church_schema.ScriptureStudyContent(**response.json())


async def post_scripture_content_from_verse(
    lang: str, parent_book: books.ParentBook, book: books.Book, chapter: int, verse: int, client: httpx.AsyncClient
) -> Dict[str, church_schema.ContentApiResponse]:
    uri = BASE_CONTENT_URL_FORMAT.format(
        lang=lang,
        parent_book_uri=uri_mappers.parent_book_uri_mapper[parent_book][0],
        book_uri=uri_mappers.parent_book_uri_mapper[parent_book][1][book],
        chapter=chapter,
        verse=verse,
    )
    return await post_scripture_content(uri, client=client)


async def post_scripture_content(uri: str, client:httpx.AsyncClient) -> Dict[str, church_schema.ContentApiResponse]:
    response = await client.post(BASE_CONTENT_URL, json={"uris": [uri]})

    if response.status_code != 200:
        # If the response is not 200, wait a few seconds and try again
        await asyncio.sleep(3)
        response = await client.post(BASE_CONTENT_URL, json={"uris": [uri]})
        if response.status_code != 200:
            raise RuntimeError(f"Failed to get content for uri {uri}: {response.text}")

    contents = {}
    for uri, content in response.json().items():
        if "type" in content and content["type"] == "ERROR":
            continue
        try:
            contents[uri] = church_schema.ContentApiResponse(**content)
        except pydantic.ValidationError as e:
            warnings.warn(f"Failed to parse content for uri {uri}: {e}")
    return contents


def extract_scripture_text_from_html(
    html: str, remove_superscripts: bool = True, remove_verse_number: bool = True
) -> str:
    """Extract the scripture text from the html.

    Args:
        html: The html to extract the scripture text from.

    Returns:
        The scripture text.
    """
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all("sup"):
        if remove_superscripts:
            tag.decompose()
        else:
            tag.replace_with(f"[{tag.get_text()}]")
    if remove_verse_number:
        for tag in soup.find_all("span", {"class": "verse-number"}):
            tag.decompose()
    return soup.get_text()


async def get_footnote_texts(
    lang: str, parent_book: books.ParentBook, book: books.Book, chapter: int, verse: int, client: httpx.AsyncClient
) -> List[str]:
    response = await get_scripture_content(lang, parent_book, book, chapter, client=client)

    footnote_urls = []
    for note_id, footnote in response.content.footnotes.items():
        # Make sure the footnote is for the correct verse
        # The id has the structure `note{verse}{letter}`
        # Note: the verse number is not zero-padded and could be multiple digits (arbitrarily long)
        if not NOTE_ID_REGEX.match(note_id):
            continue
        verse_number, _ = NOTE_ID_REGEX.match(note_id).groups()
        if int(verse_number) != verse:
            continue
        footnote_urls.extend(footnote.uris())

    footnote_urls = [url.replace("/study", f"/{lang}") for url in footnote_urls if url.startswith("/study")]

    async def extract_texts_from_url_response(footnote_url: str) -> list[str]:
        try:
            responses = await post_scripture_content(footnote_url, client=client)
        except RuntimeError as e:
            warnings.warn(f"Failed to get footnote content (from {(parent_book.name, book.name, chapter, verse)}) for url {footnote_url}: {e}")
            return []
        texts = []
        for _, content in responses.items():
            texts.extend(
                [extract_scripture_text_from_html(content_item.markup) for content_item in content.content]
            )
        return texts

    footnote_texts:list[list[str]] = await asyncio.gather(*[extract_texts_from_url_response(url) for url in footnote_urls])
    # for footnote_url in footnote_urls:
        # for _, content in post_scripture_content(footnote_url).items():
        #     footnote_texts.extend(
        #         [extract_scripture_text_from_html(content_item.markup) for content_item in content.content]
        #     )

    return flatten(footnote_texts)
