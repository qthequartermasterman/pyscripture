import unittest

import pyscripture.books
from pyscripture.api import app
from pyscripture import books


class MyTestCase(unittest.TestCase):
    def test_get_verse_from_reference(self) -> None:
        """Test that `get_verse_from_reference` returns the expected verse."""
        verse = app.get_verse_from_reference(
            pyscripture.books.VerseReference(
                lang="eng",
                parent_book=books.BookOfMormon,
                book=books.BookOfMormon["1 Nephi"],
                chapter=1,
                verse=1,
            )
        )

        print(verse)
