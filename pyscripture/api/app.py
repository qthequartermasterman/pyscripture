"""For our purposes, we need an API that can do the following:

1. Given a language, book, chapter, and verse, return the text of that verse, wrapped in a data structure that includes the verse number and the verse text, potentially with footnotes and other metadata.
2. Given a range of verses, parse the range into a data structure that includes a list of all relevant verse references.
3. Given a verse, return a list of the footnotes for that verse, each individually wrapped in a data structure that includes the footnote id and the footnote text.
"""

from typing import Tuple

import fastapi

from pyscripture import church_api, books

APP = fastapi.FastAPI()


@APP.post("/verse", response_model=books.Verse)
def get_verse_from_reference(verse_reference: books.VerseReference) -> books.Verse:
    """Get a single verse of scripture."""

    content_link = church_api.website_api_client.post_scripture_content_from_verse(
        lang=verse_reference.lang.value,
        parent_book=verse_reference.parent_book,
        book=verse_reference.book,
        chapter=verse_reference.chapter,
        verse=verse_reference.verse,
    )
    text = [
        church_api.website_api_client.extract_scripture_text_from_html(
            content_link[uri].content[0].markup,
            remove_superscripts=False,
        )
        for uri in content_link
    ]

    # Note IDs are of the format "note{verse_number}{footnote_letter}"
    # We can filter out the footnotes that don't belong to this verse by filtering out the footnotes that don't start with the verse number.
    def get_footnote_id(note_id: str) -> Tuple[int, str]:
        """Get the footnote id from the footnote text."""
        note_id = note_id.replace("note", "")
        return int(note_id[:-1]), note_id[-1]

    response = church_api.website_api_client.get_scripture_content(
        verse_reference.lang.value, verse_reference.parent_book, verse_reference.book, verse_reference.chapter
    )
    response_footnotes = {
        get_footnote_id(note_id): footnote for note_id, footnote in response.content.footnotes.items()
    }
    response_footnotes = {
        key[1]: footnote for key, footnote in response_footnotes.items() if key[0] == verse_reference.verse
    }

    footnotes = {footnote_id: footnote.text for footnote_id, footnote in response_footnotes.items()}

    return books.Verse(
        lang=verse_reference.lang,
        parent_book=verse_reference.parent_book,
        book=verse_reference.book,
        chapter=verse_reference.chapter,
        verse=verse_reference.verse,
        text=text[0],
        footnotes=footnotes,
    )


# @APP.get("/verse/{lang}/{parent_book}/{book}/{chapter}/{verse}", response_model=books.Verse)
# def get_verse(lang: SupportedLanguage, parent_book: books.ParentBooks, book: books.Book, chapter: int, verse: int) -> books.Verse:
#     """Get a single verse of scripture.
#
#     Examples:
#     """
#     verse_reference = books.VerseReference(
#         lang=lang,
#         parent_book=parent_book,
#         book=book,
#         chapter=chapter,
#         verse=verse,
#     )
#
#     return get_verse_from_reference(verse_reference)
