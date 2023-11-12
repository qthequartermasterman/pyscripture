import unittest

from pyscripture import books


class TestBooks(unittest.TestCase):
    def test_book_of_mormon_len(self):
        """Test that the Book of Mormon has the correct number of books."""
        self.assertEqual(len(books.BookOfMormonBooks), 15)

    def test_old_testament_len(self):
        """Test that the Old Testament has the correct number of books."""
        self.assertEqual(len(books.OldTestamentBooks), 39)

    def test_new_testament_len(self):
        """Test that the New Testament has the correct number of books."""
        self.assertEqual(len(books.NewTestamentBooks), 27)

    def test_doctrine_and_covenants_len(self):
        """Test that the Doctrine and Covenants has the correct number of books."""
        self.assertEqual(len(books.DoctrineAndCovenantsBooks), 1)

    def test_pearl_of_great_price_len(self):
        """Test that the Pearl of Great Price has the correct number of books."""
        self.assertEqual(len(books.PearlOfGreatPriceBooks), 5)
