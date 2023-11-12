import enum


class BookOfMormonBooks(str, enum.Enum):
    """The books of the Book of Mormon."""

    Nephi1 = "1 Nephi"
    Nephi2 = "2 Nephi"
    Jacob = "Jacob"
    Enos = "Enos"
    Jarom = "Jarom"
    Omni = "Omni"
    WordsOfMormon = "Words of Mormon"
    Mosiah = "Mosiah"
    Alma = "Alma"
    Helaman = "Helaman"
    Nephi3 = "3 Nephi"
    Nephi4 = "4 Nephi"
    Mormon = "Mormon"
    Ether = "Ether"
    Moroni = "Moroni"



class OldTestamentBooks(str, enum.Enum):
    """The books of the Old Testament."""

    Genesis = "Genesis"
    Exodus = "Exodus"
    Leviticus = "Leviticus"
    Numbers = "Numbers"
    Deuteronomy = "Deuteronomy"
    Joshua = "Joshua"
    Judges = "Judges"
    Ruth = "Ruth"
    Samuel1 = "1 Samuel"
    Samuel2 = "2 Samuel"
    Kings1 = "1 Kings"
    Kings2 = "2 Kings"
    Chronicles1 = "1 Chronicles"
    Chronicles2 = "2 Chronicles"
    Ezra = "Ezra"
    Nehemiah = "Nehemiah"
    Esther = "Esther"
    Job = "Job"
    Psalms = "Psalms"
    Proverbs = "Proverbs"
    Ecclesiastes = "Ecclesiastes"
    SongOfSolomon = "Song of Solomon"
    Isaiah = "Isaiah"
    Jeremiah = "Jeremiah"
    Lamentations = "Lamentations"
    Ezekiel = "Ezekiel"
    Daniel = "Daniel"
    Hosea = "Hosea"
    Joel = "Joel"
    Amos = "Amos"
    Obadiah = "Obadiah"
    Jonah = "Jonah"
    Micah = "Micah"
    Nahum = "Nahum"
    Habakkuk = "Habakkuk"
    Zephaniah = "Zephaniah"
    Haggai = "Haggai"
    Zechariah = "Zechariah"
    Malachi = "Malachi"


class NewTestamentBooks(str, enum.Enum):
    """The books of the New Testament."""

    Matthew = "Matthew"
    Mark = "Mark"
    Luke = "Luke"
    John = "John"
    Acts = "Acts"
    Romans = "Romans"
    Corinthians1 = "1 Corinthians"
    Corinthians2 = "2 Corinthians"
    Galatians = "Galatians"
    Ephesians = "Ephesians"
    Philippians = "Philippians"
    Colossians = "Colossians"
    Thessalonians1 = "1 Thessalonians"
    Thessalonians2 = "2 Thessalonians"
    Timothy1 = "1 Timothy"
    Timothy2 = "2 Timothy"
    Titus = "Titus"
    Philemon = "Philemon"
    Hebrews = "Hebrews"
    James = "James"
    Peter1 = "1 Peter"
    Peter2 = "2 Peter"
    John1 = "1 John"
    John2 = "2 John"
    John3 = "3 John"
    Jude = "Jude"
    Revelation = "Revelation"



class DoctrineAndCovenantsBooks(str, enum.Enum):
    """The books of the Doctrine and Covenants."""

    DoctrineAndCovenants = "Doctrine and Covenants"



class PearlOfGreatPriceBooks(str, enum.Enum):
    """The books of the Pearl of Great Price."""

    Moses = "Moses"
    Abraham = "Abraham"
    JosephSmithMatthew = "Joseph Smith--Matthew"
    JosephSmithHistory = "Joseph Smith--History"
    ArticlesOfFaith = "Articles of Faith"

parent_names = {
    BookOfMormonBooks: "Book of Mormon",
    OldTestamentBooks: "Old Testament",
    NewTestamentBooks: "New Testament",
    DoctrineAndCovenantsBooks: "Doctrine and Covenants",
    PearlOfGreatPriceBooks: "Pearl of Great Price",
}
