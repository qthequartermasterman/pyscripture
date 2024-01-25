import hashlib
import itertools
import unittest

import hypothesis
import pandas as pd
from hypothesis import strategies as st

from pyscripture import books, download

EXPECTED_BOOKS = itertools.chain(
    books.BookOfMormon.books,
    books.OldTestament.books,
    books.NewTestament.books,
    books.DoctrineAndCovenants.books,
    books.PearlOfGreatPrice.books,
)


class TestExpectedHash(unittest.TestCase):
    @hypothesis.given(st.text())
    def test_expected_hash(self, text: str) -> None:
        """Test that `expected_hash` returns the same string it was passed."""
        expected_hash = hashlib.sha256(text.encode()).hexdigest()

        @download.expected_hash(expected_sha256_hash=expected_hash)
        def func_correct() -> str:
            """A function that returns the string it was passed.

            Note:
                This function's expected hash is correct.
            """
            return text

        @download.expected_hash(expected_sha256_hash=expected_hash[::-1])
        def func_incorrect() -> str:
            """A function that returns the string it was passed.

            Note:
                This function's expected hash is incorrect.
            """
            return text

        # Return value should be unaffected by the decorator
        # Should pass the hash assertion
        assert func_correct() == text

        # Hash assertion should fail
        with self.assertRaises(ValueError):
            func_incorrect()


class TestDownloadTextIntegration(unittest.TestCase):
    def test_download_text(self) -> None:
        """Test that `download_text` downloads the text of all scripture in the same format we expect."""
        downloaded_text = download.download_text()
        # Hardcoded hash of the text when I wrote this test.
        # If the text changes, then we cannot guarantee that the text will parse correctly, so we should fail this test.
        expected_sha256_hash = "ccbd4765243daafcf5e8536d421a93cc7037e86d6a067bfaa4c55d8f0de5ea6e"
        actual_sha256_hash = hashlib.sha256(downloaded_text.encode()).hexdigest()
        assert downloaded_text.startswith("Genesis 1:1     In the beginning God created the heaven and the earth.")
        assert actual_sha256_hash == expected_sha256_hash


class TestOrganizeBooksLookup(unittest.TestCase):
    def test_organize_books_lookup(self) -> None:
        """Test that `organize_books_lookup` returns the correct dictionary."""
        books_lookup = download.organize_books_lookup()

        for book in EXPECTED_BOOKS:
            self.assertIn(book.value, books_lookup)
            self.assertEqual(books_lookup[book.value], books.parent_names[book.__class__])


class TestGetDataframe(unittest.TestCase):
    def test_get_dataframe(self) -> None:
        """Test that `get_dataframe` returns a dataframe with the correct columns."""
        dataframe = download.get_dataframe()
        self.assertEqual(dataframe.columns.tolist(), ["Text"])
        self.assertEqual(len(dataframe), 41995)  # Hardcoded number of verses in the text when I wrote this test.

        # Make sure our index has the desired structure
        self.assertIsInstance(dataframe.index, pd.MultiIndex)
        # 0-th level of index should be the parent book
        self.assertSetEqual(set(dataframe.index.get_level_values(0).unique()), set(books.parent_names.values()))
        # 1st level of index should be the book
        self.assertSetEqual(
            set(dataframe.index.get_level_values(1).unique()),
            {book.value for book in EXPECTED_BOOKS},
        )
        # 2nd level of index should be the chapter number
        self.assertTrue(
            all(isinstance(chapter, int) and chapter >= 0 for chapter in dataframe.index.get_level_values(2))
        )
        # 3rd level of index should be the verse number
        self.assertTrue(all(isinstance(verse, int) and verse >= 0 for verse in dataframe.index.get_level_values(3)))

        # Make sure we can access the text of a verse
        self.assertTrue(all(isinstance(text, str) for text in dataframe["Text"]))
        self.assertEqual(
            dataframe.loc[("Book of Mormon", "1 Nephi", 1, 1), "Text"],
            "I, Nephi, having been born of goodly parents, therefore I was taught somewhat in all the learning of my father; and having seen many afflictions in the course of my days, nevertheless, having been highly favored of the Lord in all my days; yea, having had a great knowledge of the goodness and the mysteries of God, therefore I make a record of my proceedings in my days.",
        )
