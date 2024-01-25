import enum
from typing import Any

from typing_extensions import Literal, TypeAlias, Self

import pydantic


class Book(pydantic.BaseModel):
    """A book of scripture."""

    name: str
    abbreviation: str

    def __hash__(self):
        return hash(self.name)


class ParentBook(pydantic.BaseModel):
    """A parent book of scripture."""

    name: str
    books: list[Book]

    def __hash__(self):
        return hash((self.name, tuple(self.books)))

    def __contains__(self, item) -> bool:
        return item in self.books

    @pydantic.computed_field()
    def book_dict(self) -> dict[str, Book]:
        return {book.name: book for book in self.books}

    def __getitem__(self, item) -> Book:
        return self.book_dict[item]


BookOfMormon = ParentBook(
    name="Book of Mormon",
    books=[
        Book(name="1 Nephi", abbreviation="1 Ne."),
        Book(name="2 Nephi", abbreviation="2 Ne."),
        Book(name="Jacob", abbreviation="Jacob"),
        Book(name="Enos", abbreviation="Enos"),
        Book(name="Jarom", abbreviation="Jarom"),
        Book(name="Omni", abbreviation="Omni"),
        Book(name="Words of Mormon", abbreviation="W of M"),
        Book(name="Mosiah", abbreviation="Mosiah"),
        Book(name="Alma", abbreviation="Alma"),
        Book(name="Helaman", abbreviation="Hel."),
        Book(name="3 Nephi", abbreviation="3 Ne."),
        Book(name="4 Nephi", abbreviation="4 Ne."),
        Book(name="Mormon", abbreviation="Morm."),
        Book(name="Ether", abbreviation="Ether"),
        Book(name="Moroni", abbreviation="Moro."),
    ],
)

OldTestament = ParentBook(
    name="Old Testament",
    books=[
        Book(name="Genesis", abbreviation="Gen."),
        Book(name="Exodus", abbreviation="Ex."),
        Book(name="Leviticus", abbreviation="Lev."),
        Book(name="Numbers", abbreviation="Num."),
        Book(name="Deuteronomy", abbreviation="Deut."),
        Book(name="Joshua", abbreviation="Josh."),
        Book(name="Judges", abbreviation="Judg."),
        Book(name="Ruth", abbreviation="Ruth"),
        Book(name="1 Samuel", abbreviation="1 Sam."),
        Book(name="2 Samuel", abbreviation="2 Sam."),
        Book(name="1 Kings", abbreviation="1 Kgs."),
        Book(name="2 Kings", abbreviation="2 Kgs."),
        Book(name="1 Chronicles", abbreviation="1 Chr."),
        Book(name="2 Chronicles", abbreviation="2 Chr."),
        Book(name="Ezra", abbreviation="Ezra"),
        Book(name="Nehemiah", abbreviation="Neh."),
        Book(name="Esther", abbreviation="Esth."),
        Book(name="Job", abbreviation="Job"),
        Book(name="Psalms", abbreviation="Ps."),
        Book(name="Proverbs", abbreviation="Prov."),
        Book(name="Ecclesiastes", abbreviation="Eccl."),
        Book(name="Song of Solomon", abbreviation="Song"),
        Book(name="Isaiah", abbreviation="Isa."),
        Book(name="Jeremiah", abbreviation="Jer."),
        Book(name="Lamentations", abbreviation="Lam."),
        Book(name="Ezekiel", abbreviation="Ezek."),
        Book(name="Daniel", abbreviation="Dan."),
        Book(name="Hosea", abbreviation="Hosea"),
        Book(name="Joel", abbreviation="Joel"),
        Book(name="Amos", abbreviation="Amos"),
        Book(name="Obadiah", abbreviation="Obad."),
        Book(name="Jonah", abbreviation="Jonah"),
        Book(name="Micah", abbreviation="Micah"),
        Book(name="Nahum", abbreviation="Nahum"),
        Book(name="Habakkuk", abbreviation="Hab."),
        Book(name="Zephaniah", abbreviation="Zeph."),
        Book(name="Haggai", abbreviation="Hag."),
        Book(name="Zechariah", abbreviation="Zech."),
        Book(name="Malachi", abbreviation="Mal."),
    ],
)

NewTestament = ParentBook(
    name="New Testament",
    books=[
        Book(name="Matthew", abbreviation="Matt."),
        Book(name="Mark", abbreviation="Mark"),
        Book(name="Luke", abbreviation="Luke"),
        Book(name="John", abbreviation="John"),
        Book(name="Acts", abbreviation="Acts"),
        Book(name="Romans", abbreviation="Rom."),
        Book(name="1 Corinthians", abbreviation="1 Cor."),
        Book(name="2 Corinthians", abbreviation="2 Cor."),
        Book(name="Galatians", abbreviation="Gal."),
        Book(name="Ephesians", abbreviation="Eph."),
        Book(name="Philippians", abbreviation="Philip."),
        Book(name="Colossians", abbreviation="Col."),
        Book(name="1 Thessalonians", abbreviation="1 Thes."),
        Book(name="2 Thessalonians", abbreviation="2 Thes."),
        Book(name="1 Timothy", abbreviation="1 Tim."),
        Book(name="2 Timothy", abbreviation="2 Tim."),
        Book(name="Titus", abbreviation="Titus"),
        Book(name="Philemon", abbreviation="Philem."),
        Book(name="Hebrews", abbreviation="Heb."),
        Book(name="James", abbreviation="James"),
        Book(name="1 Peter", abbreviation="1 Pet."),
        Book(name="2 Peter", abbreviation="2 Pet."),
        Book(name="1 John", abbreviation="1 Jn."),
        Book(name="2 John", abbreviation="2 Jn."),
        Book(name="3 John", abbreviation="3 Jn."),
        Book(name="Jude", abbreviation="Jude"),
        Book(name="Revelation", abbreviation="Rev."),
    ],
)

DoctrineAndCovenants = ParentBook(
    name="Doctrine and Covenants",
    books=[
        Book(name="Doctrine and Covenants", abbreviation="D&C"),
    ],
)

PearlOfGreatPrice = ParentBook(
    name="Pearl of Great Price",
    books=[
        Book(name="Moses", abbreviation="Moses"),
        Book(name="Abraham", abbreviation="Abr."),
        Book(name="Joseph Smith--Matthew", abbreviation="JS—M"),
        Book(name="Joseph Smith--History", abbreviation="JS—H"),
        Book(name="Articles of Faith", abbreviation="A of F"),
    ],
)


class ParentBooks(enum.Enum):
    BookOfMormon = BookOfMormon
    OldTestament = OldTestament
    NewTestament = NewTestament
    DoctrineAndCovenants = DoctrineAndCovenants
    PearlOfGreatPrice = PearlOfGreatPrice

    @classmethod
    def from_book_name(cls, book_name: str) -> "ParentBooks":
        for parent_book in cls:
            if book_name in parent_book.value.book_dict:
                return parent_book
        raise ValueError(f"Invalid book name: {book_name}")


class SupportedLanguage(str, enum.Enum):
    eng = "eng"


class VerseReference(pydantic.BaseModel):
    """A reference to a single verse of scripture.

    Examples:
    """

    lang: SupportedLanguage = pydantic.Field(
        description="The language of the verse.",
        examples=list(SupportedLanguage),
    )
    parent_book: ParentBook = pydantic.Field(
        description="The parent book of the verse.",
        examples=list(ParentBooks),
    )
    book: Book = pydantic.Field(
        description="The book of the verse.",
        examples=[book for parent_book in ParentBooks for book in parent_book.value.books],
    )
    chapter: int = pydantic.Field(description="The chapter number of the verse.", ge=1)
    verse: int = pydantic.Field(description="The verse number.", ge=1)

    @pydantic.model_validator(mode="after")
    def validate_book_in_parent(self) -> Self:
        """Validate that the book is in the parent book."""
        if self.book not in self.parent_book:
            raise ValueError(f"Book {self.book} is not in parent book {self.parent_book}")
        return self

    @property
    def reference_str(self) -> str:
        """Get the reference string of the verse."""
        return f"{self.book.name} {self.chapter}:{self.verse}"


class Verse(VerseReference):
    """A single verse of scripture.

    Examples:
    """

    text: str = pydantic.Field(description="The text of the verse.")
    footnotes: dict[str, Any] = pydantic.Field(description="The footnotes of the verse.")
