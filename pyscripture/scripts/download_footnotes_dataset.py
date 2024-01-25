from pyscripture.church_api import website_api_client
from typing import Sequence
from pyscripture import books, download
import asyncio
import httpx
import json
import pathlib
import tqdm.auto

SCRIPTURE_DF = download.get_dataframe()

BASE_DIR = pathlib.Path('scripture_footnotes')
BASE_DIR.mkdir(exist_ok=True, parents=True)

README_YAML_BLOCK = """---
configs:
- config_name: default
  data_files:
    - split: train
      path: 
      - "Book of Mormon*.json"
      - "Doctrine and Covenants*.json"
      - "New Testament*.json"
      - "Old Testament*.json"
    - split: test
      path: "Pearl of Great Price*.json"
---
"""

async def run(scripture_references: Sequence[books.VerseReference]) -> dict[str, list[str]]:
    async def get_verse_and_footnotes_from_reference(scripture_reference: books.VerseReference, client:httpx.AsyncClient) -> tuple[str, list[str]]:
        """Get the verse and footnotes from a reference."""

        parent_book = scripture_reference.parent_book
        book = scripture_reference.book
        chapter = scripture_reference.chapter
        verse = scripture_reference.verse
        lang = scripture_reference.lang.value
        # verse_content = await website_api_client.post_scripture_content_from_verse(lang=lang, parent_book=parent_book,
        #                                                                            book=book, chapter=chapter,
        #                                                                            verse=verse, client=client)
        # assert len(verse_content) == 1
        #
        # verse_text = website_api_client.extract_scripture_text_from_html(
        #     next(iter(verse_content.values())).content[0].markup, remove_superscripts=True)

        verse_text = SCRIPTURE_DF.loc[parent_book.name, book.name, chapter, verse]['Text']
        footnotes = await website_api_client.get_footnote_texts(lang=lang, parent_book=parent_book, book=book,
                                                                chapter=chapter, verse=verse, client=client)
        return verse_text, footnotes



    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(*[get_verse_and_footnotes_from_reference(scripture_reference, client) for scripture_reference in scripture_references])

    return {scripture_reference.reference_str: {'verse': verse, 'footnotes': footnotes} for scripture_reference, (verse, footnotes) in zip(scripture_references, results)}




parent_book_books:list[tuple[books.ParentBook, books.Book]] = [(parent_book.value, book) for parent_book in books.ParentBooks for book in parent_book.value.books]


for parent_book, book in tqdm.tqdm(parent_book_books):
    json_path = BASE_DIR / f'{parent_book.name}_{book.name}.json'
    if json_path.exists():
        continue
    chapter_verses = SCRIPTURE_DF.loc[parent_book.name, book.name].index
    references = [
        books.VerseReference(lang="eng", parent_book=parent_book, book=book, chapter=chapter, verse=verse) for chapter, verse in chapter_verses
    ]
    try:
        results = asyncio.run(run(references))
    except RuntimeError as e:
        print(f'Runtime error for {parent_book.name} {book.name}, {str(e)}')
        continue
    json_path.write_text(json.dumps(results, indent=4))
    
readme_path = BASE_DIR / 'README.md'
readme_path.write_text(README_YAML_BLOCK)
