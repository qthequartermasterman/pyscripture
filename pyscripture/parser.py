import dataclasses
from typing import List, Tuple, TypeAlias
from pyscripture import books



@dataclasses.dataclass
class ChapterVerse:
    chapter: int
    verse: int
    
@dataclasses.dataclass
class VerseRange:
    start: ChapterVerse
    end: ChapterVerse


ScriptureRanges: TypeAlias = Tuple[
    str, # Book name
    List[  # List of ranges
        Tuple[
            Tuple[int, int], # Start chapter and verse
            Tuple[int, int], # End chapter and verse
        ]
    ]
]

def parse_scripture_reference(ref: str) -> ScriptureRanges:
    """Parse a scripture reference into a book and list of ((start_chapter, start_verse), (end_chapter, end_verse) tuples for each range
    in the reference.

    Examples:
        # Single verse
        >>> parse_scripture_reference("Jarom 1:1")
        ('Jarom', [((1, 1), (1, 1))])

        # Single range of verses
        >>> parse_scripture_reference("Jarom 1:1-2")
        ('Jarom', [((1, 1), (1, 2))])

        # Multiple verses
        >>> parse_scripture_reference("Jarom 1:1,5,8")
        ('Jarom', [((1, 1), (1, 1)), ((1, 5), (1, 5)), ((1, 8), (1, 8))])

        # Multiple verses and/or ranges
        >>> parse_scripture_reference("Jarom 1:1,2,3-4")
        ('Jarom', [((1, 1), (1, 1)), ((1, 2), (1, 2)), ((1, 3), (1, 4))])

        # Single range that spans chapters
        >>> parse_scripture_reference("Jarom 1:1-2:3")
        ('Jarom', [((1, 1), (2, 3))])

        # Multiple ranges that span chapters
        >>> parse_scripture_reference("Jarom 1:1-2:3,4:5-6")
        ('Jarom', [((1, 1), (2, 3)), ((4, 5), (4, 6))])

        # Books with numbers in their names should be prefixed with a number
        >>> parse_scripture_reference("1 Nephi 1:1")
        ('1 Nephi', [((1, 1), (1, 1))])

        # Books with spaces in their names
        >>> parse_scripture_reference("Words of Mormon 1:3")
        ('Words of Mormon', [((1, 3), (1, 3))])

        # TODO: Additional range
        >>> parse_scripture_reference("John 20:31 (30–31)")
        ('John', [((20, 30), (20, 31))])

        # TODO: Additional verses
        >>> parse_scripture_reference("2 Ne. 9:41 (41, 45, 51)")
        ('2 Ne.', [((9, 41), (9, 41)), ((9, 45), (9, 45)), ((9, 51), (9, 51))])

    Args:
        ref: The scripture reference to parse.

    Returns:
        Book and list of ranges.
    """
    ref = ref.strip()

    num_colons = ref.count(":")
    if num_colons == 0:
        raise ValueError(f"Invalid scripture reference: {ref}")

    name_chapter, verses = ref.split(":", maxsplit=1)
    name, chapter = name_chapter.rsplit(" ", maxsplit=1)
    chapter = int(chapter)
    if num_colons != 1:
        verses = f"{chapter}:{verses}"

    name = name.strip()

    ranges_str = verses.split(",")
    ranges_str = [r.strip() for r in ranges_str]
    ranges = []
    for range in ranges_str:
        if "-" in range:
            start, end = range.split("-", maxsplit=1)
            start = tuple(int(n) for n in start.split(":"))
            end = tuple(int(n) for n in end.split(":"))
            if len(start) == 1:
                start = (chapter, start[0])
            if len(end) == 1:
                end = (start[0], end[0])
        else:
            start = tuple(int(n) for n in range.split(":"))
            if len(start) == 1:
                start = (chapter, start[0])
            end = start

        ranges.append((start, end))

    return name, ranges

def parse_ranges_to_verse_references(lang:str, ranges: ScriptureRanges) -> List[books.VerseReference]:
    """Parse a list of ranges into a list of verse references.

    Examples:
        >>> parse_ranges_to_verse_references('eng', ("Jarom", [((1, 1), (1, 1))]))
        [VerseReference(lang=<SupportedLanguage.eng: 'eng'>, parent_book=<ParentBooks.BookOfMormon: <BookOfMormon.Jarom: 'Jarom'>>, book=<BookOfMormon.Jarom: 'Jarom'>, chapter=1, verse=1)]

        >>> parse_ranges_to_verse_references('eng', ("Jarom", [((1, 1), (1, 2))]))
        [VerseReference(lang=<SupportedLanguage.eng: 'eng'>, parent_book=<ParentBooks.BookOfMormon: <BookOfMormon.Jarom: 'Jarom'>>, book=<BookOfMormon.Jarom: 'Jarom'>, chapter=1, verse=1), VerseReference(lang=<SupportedLanguage.eng: 'eng'>, parent_book=<ParentBooks.BookOfMormon: <BookOfMormon.Jarom: 'Jarom'>>, book=<BookOfMormon.Jarom: 'Jarom'>, chapter=1, verse=2)]

        >>> parse_ranges_to_verse_references('eng', ("Jarom", [((1, 1), (1, 1)), ((1, 5), (1, 5)), ((1, 8), (1, 8))]))
        [VerseReference(lang=<SupportedLanguage.eng: 'eng'>, parent_book=<ParentBooks.BookOfMormon: <BookOfMormon.Jarom: 'Jarom'>>, book=<BookOfMormon.Jarom: 'Jarom'>, chapter=1, verse=1), VerseReference(lang=<SupportedLanguage.eng: 'eng'>, parent_book=<ParentBooks.BookOfMormon: <BookOfMormon.Jarom: 'Jarom'>>, book=<BookOfMormon.Jarom: 'Jarom'>, chapter=1, verse=5), VerseReference(lang=<SupportedLanguage.eng: 'eng'>, parent_book=<ParentBooks.BookOfMormon: <BookOfMormon.Jarom: 'Jarom'>>, book=<BookOfMormon.Jarom: 'Jarom'>, chapter=1, verse=8)]

    """
    book_name, range_list = ranges

    parent_book = books.ParentBooks.from_book_name(book_name)
    book = parent_book.value[book_name]

    verse_references = []

    for range_tup in range_list:
        start_tup, end_tup = range_tup
        start = ChapterVerse(*start_tup)
        end = ChapterVerse(*end_tup)
        if start.chapter != end.chapter:
            raise NotImplementedError("Chapter spans are not yet supported")
        verse_references.extend(
            books.VerseReference(
                lang=lang,
                parent_book=parent_book,
                book=book,
                chapter=start.chapter,
                verse=verse,
            )
            for verse in range(start.verse, end.verse + 1)
        )

    return verse_references