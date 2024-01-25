import json

from pyscripture.scripts import download_footnotes_dataset
from download_footnotes_dataset import BASE_DIR
import datasets


_DESCRIPTION = """\
A dataset of pairs of verses of scripture from the Church of Jesus Christ of Latter-day Saints.

Pairs are generated by taking a verse and its footnotes and pairing it with each of its footnotes.
"""



class ScriptureFootnoteDataset(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("0.0.1")
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="default",
            version=VERSION,
            description="Default version",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "verse": datasets.Value("string"),
                    "footnote": datasets.Value("string"),
                }
            ),
            supervised_keys=('verse', 'footnote'),
        )

    def _split_generators(self, dl_manager):
        # The training set will be generated from the Book of Mormon, Doctrine and Covenants, New Testament, and Old Testament.
        # Files: "Book of Mormon*.json", "Doctrine and Covenants*.json", "New Testament*.json", "Old Testament*.json"
        # The test set will be generated from the Pearl of Great Price.
        # Files: "Pearl of Great Price*.json"

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "files": [
                        *BASE_DIR.glob("Book of Mormon*.json"),
                        *BASE_DIR.glob("Doctrine and Covenants*.json"),
                        *BASE_DIR.glob("New Testament*.json"),
                        *BASE_DIR.glob("Old Testament*.json"),
                    ]
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "files": [
                        *BASE_DIR.glob("Pearl of Great Price*.json"),
                    ]
                },
            ),
        ]

    def _generate_examples(self, files):
        for file in files:
            with open(file) as f:
                data = json.load(f)
            for verse, verse_data in data.items():
                for footnote_i, footnote in enumerate(verse_data['footnotes']):
                    yield f"{verse} (Footnote {footnote_i})", {
                        "verse": verse_data['verse'],
                        "footnote": footnote,
                    }

if __name__=="__main__":
    scripture_footnotes = ScriptureFootnoteDataset()
    scripture_footnotes.download_and_prepare()
    scripture_footnotes = scripture_footnotes.as_dataset()
    print(scripture_footnotes.info)
