from pyscripture.scripts import build_footnotes_dataset
import sentence_transformers
import sentence_transformers.losses
from torch.utils.data import DataLoader

scripture_footnotes = build_footnotes_dataset.ScriptureFootnoteDataset()
scripture_footnotes.download_and_prepare()
scripture_footnotes = scripture_footnotes.as_dataset()

model = sentence_transformers.SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

train_examples = [
    sentence_transformers.InputExample(texts=[example['verse'], example['footnote']]) for example in scripture_footnotes['train']
]

train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=64)

loss = sentence_transformers.losses.MultipleNegativesRankingLoss(model)

model.fit(
    train_objectives=[(train_dataloader, loss)],
    epochs=1,
    warmup_steps=100,
    output_path="scripture_footnotes_model",
)

