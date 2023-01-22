import requests
import pandas as pd

from typing import Dict


def download_text() -> str:
    """Download text of all scripture from GitHub.

    Returns:
        All scripture text as a single string.
    """
    req = requests.get('http://raw.githubusercontent.com/beandog/lds-scriptures/master/text/lds-scriptures.txt')
    return req.text


book_of_mormon_books = ('1 Nephi', '2 Nephi', 'Jacob', 'Enos', 'Jarom', 'Omni', 'Words of Mormon', 'Mosiah', 'Alma',
                        'Helaman', '3 Nephi', '4 Nephi', 'Mormon', 'Ether', 'Moroni')
old_testament_books = (
    'Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth', '1 Samuel', '2 Samuel',
    '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles', 'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalms', 'Proverbs',
    'Ecclesiastes', 'Song of Solomon', 'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel',
    'Amos',
    'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi',)
new_testament_books = (
    'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians',
    'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians', '1 Timothy', '2 Timothy', 'Titus', 'Philemon',
    'Hebrews', 'James', '1 Peter', '2 Peter', '1 John', '2 John', '3 John', 'Jude', 'Revelation',)
doctrine_and_covenants_books = ('Doctrine and Covenants',)
pearl_of_great_price_books = ('Moses', 'Abraham', 'Joseph Smith--Matthew', 'Joseph Smith--History', 'Articles of Faith')


def organize_books_lookup() -> Dict[str, str]:
    books = {b: "Book of Mormon" for b in book_of_mormon_books}
    for b in old_testament_books:
        books[b] = "Old Testament"
    for b in new_testament_books:
        books[b] = "New Testament"
    for b in doctrine_and_covenants_books:
        books[b] = "Doctrine and Covenants"
    for b in pearl_of_great_price_books:
        books[b] = "Pearl of Great Price"
    return books

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
    books = organize_books_lookup()

    lines = text.splitlines()
    verses = dict([tuple(t.split("     ", maxsplit=1)) for t in lines])
    verses = {tuple(k.rsplit(" ", maxsplit=1)): v for k, v in verses.items()}
    verses = {(books[k[0]], k[0], *[int(n) for n in k[1].split(":")]): v for k, v in verses.items()}

    df = pd.DataFrame.from_dict(verses, orient="index", columns=['Text'])
    df.index = pd.MultiIndex.from_tuples(df.index)
    return df
