import functools
import hashlib
from typing import Callable, Dict

import pandas as pd
import requests
from typing_extensions import ParamSpec

from pyscripture import books

P = ParamSpec("P")


def expected_hash(expected_sha256_hash: str) -> Callable[[Callable[P, str]], Callable[P, str]]:
    """Decorator to check that a function returns a string with a specific hash.

    Args:
        expected_sha256_hash: The expected sha256 hash of the string returned from the decorated function.

    Raises:
        ValueError: If the hash of the returned string does not match the expected hash.

    Returns:
        A decorator that checks that the returned string has the expected hash.
    """

    def decorator(func: Callable[P, str]) -> Callable[P, str]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> str:
            downloaded_text = func(*args, **kwargs)
            actual_sha256_hash = hashlib.sha256(downloaded_text.encode()).hexdigest()
            if actual_sha256_hash != expected_sha256_hash:
                raise ValueError(
                    f"When calling {func}, Expected hash {expected_sha256_hash}, but got {actual_sha256_hash}"
                )
            return downloaded_text

        return wrapper

    return decorator


@functools.lru_cache(maxsize=1)
@expected_hash(expected_sha256_hash="ccbd4765243daafcf5e8536d421a93cc7037e86d6a067bfaa4c55d8f0de5ea6e")
def download_text() -> str:
    """Download text of all scripture from GitHub.

    Returns:
        All scripture text as a single string.
    """
    req = requests.get("http://raw.githubusercontent.com/beandog/lds-scriptures/master/text/lds-scriptures.txt")
    return req.text


def organize_books_lookup() -> Dict[str, str]:
    """Organize books with their Parent Books into a lookup table."""
    parent_books = {b.name: "Book of Mormon" for b in books.BookOfMormon.books}
    for b in books.OldTestament.books:
        parent_books[b.name] = "Old Testament"
    for b in books.NewTestament.books:
        parent_books[b.name] = "New Testament"
    for b in books.DoctrineAndCovenants.books:
        parent_books[b.name] = "Doctrine and Covenants"
    for b in books.PearlOfGreatPrice.books:
        parent_books[b.name] = "Pearl of Great Price"
    return parent_books


def get_dataframe() -> pd.DataFrame:
    """Obtain scripture DataFrame.

    Each verse is contained the column "Text", and can be referenced via a `pd.MultiIndex` with the following heirarchy:
        1. Parent Book ("Old Testament", "New Testament", "Book of Mormon", "Doctrine and Covenants", "Pearl of Great Price")
        2. Book ("Genesis", "Exodus", "3 Nephi", "Doctrine and Covenants", "Abraham", etc...)
        3. Chapter Number (as an integer)
        4. Verse Number (as an integer)

    Note: "Doctrine and Covenants" needs to be specified as both the Parent and Child book names for verses in the Doctrine and Covenants.
    Note: For books with only a single chapter, the chapter number is `1`.

    Returns:
        MultiIndexed Dataframe of scripture verses.

    """
    text = download_text()
    parents_books = organize_books_lookup()

    lines = text.splitlines()
    verses = dict([tuple(t.split("     ", maxsplit=1)) for t in lines])
    verses = {tuple(k.rsplit(" ", maxsplit=1)): v for k, v in verses.items()}
    verses = {(parents_books[k[0]], k[0], *[int(n) for n in k[1].split(":")]): v for k, v in verses.items()}

    df = pd.DataFrame.from_dict(verses, orient="index", columns=["Text"])
    df.index = pd.MultiIndex.from_tuples(df.index)
    df["Text"] = df["Text"].str.strip()
    return df
