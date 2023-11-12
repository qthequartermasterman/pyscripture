import unittest

import hypothesis

from pyscripture import parser


class TestParseReference(unittest.TestCase):
    def hard_code_tests(self) -> None:
        """Test that the parser works for a few hard-coded examples."""
        with self.subTest("Single verse"):
            self.assertEqual(
                parser.parse_scripture_reference("Jarom 1:1"),
                ("Jarom", [((1, 1), (1, 1))]),
            )
        with self.subTest("Single range of verses"):
            self.assertEqual(
                parser.parse_scripture_reference("Jarom 1:1-2"),
                ("Jarom", [((1, 1), (1, 2))]),
            )
        with self.subTest("Multiple verses"):
            self.assertEqual(
                parser.parse_scripture_reference("Jarom 1:1,5,8"),
                ("Jarom", [((1, 1), (1, 1)), ((1, 5), (1, 5)), ((1, 8), (1, 8))]),
            )
        with self.subTest("Multiple verses and/or ranges"):
            self.assertEqual(
                parser.parse_scripture_reference("Jarom 1:1,2,3-4"),
                ("Jarom", [((1, 1), (1, 1)), ((1, 2), (1, 2)), ((1, 3), (1, 4))]),
            )
        with self.subTest("Single range that spans chapters"):
            self.assertEqual(
                parser.parse_scripture_reference("Jarom 1:1-2:3"),
                ("Jarom", [((1, 1), (1, 1)), ((1, 2), (2, 3))]),
            )
        with self.subTest("Multiple ranges that span chapters"):
            self.assertEqual(
                parser.parse_scripture_reference("Jarom 1:1-2:3,4:5-6"),
                ("Jarom", [((1, 1), (1, 1)), ((1, 2), (2, 3)), ((4, 5), (4, 6))]),
            )
        with self.subTest("Books with numbers in their names should be prefixed with a number"):
            self.assertEqual(
                parser.parse_scripture_reference("1 Nephi 1:1"),
                ("1 Nephi", [((1, 1), (1, 1))]),
            )
        with self.subTest("Books with spaces in their names"):
            self.assertEqual(
                parser.parse_scripture_reference("Words of Mormon 1:3"),
                ("Words of Mormon", [((1, 3), (1, 3))]),
            )
