from typing import List, Tuple


def parse_scripture_reference(ref: str) -> Tuple[str, List[Tuple[Tuple[int, int], Tuple[int, int]]]]:
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
