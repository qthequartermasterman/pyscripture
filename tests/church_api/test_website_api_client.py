import unittest

from pyscripture.church_api import website_api_client
from pyscripture import books


class TestGetScriptureContent(unittest.TestCase):
    def test_get_scripture_content(self) -> None:
        """Test that `get_scripture_content` returns the expected content."""
        response = website_api_client.get_scripture_content(
            "eng", books.BookOfMormonBooks, books.BookOfMormonBooks.Nephi1, 7
        )

        for footnote in response.content.footnotes.items():
            print(footnote)

    def test_get_scripture_content_from_uri(self) -> None:
        """Test that `get_scripture_content_from_uri` returns the expected content."""
        uri = "/eng/scriptures/pgp/moses/5.58"
        content_link = website_api_client.post_scripture_content(uri)
        text = website_api_client.extract_scripture_text_from_html(content_link[uri].content[0].markup)
        print(text)

    def test_get_footnote_texts(self) -> None:
        """Test that `get_footnote_texts` returns the expected footnote texts."""
        footnote_texts = website_api_client.get_footnote_texts(
            "eng", books.BookOfMormon, books.BookOfMormon["1 Nephi"], 1, 1
        )
        print(footnote_texts)


class TestPostScriptureContent(unittest.TestCase):
    def test_post_scripture_content(self) -> None:
        """Test that `post_scripture_content` returns the expected content."""
        lang = "eng"
        parent_book = books.BookOfMormon
        book = books.BookOfMormon["1 Nephi"]
        chapter = 1
        verse = 1

        content_link = website_api_client.post_scripture_content_from_verse(lang, parent_book, book, chapter, verse)
        text = [
            website_api_client.extract_scripture_text_from_html(
                content_link[uri].content[0].markup, remove_superscripts=False
            )
            for uri in content_link
        ]
        print(text)
