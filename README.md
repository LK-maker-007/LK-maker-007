<picture>
  <source media="(prefers-color-scheme: dark)" srcset="header-terminal-dark.svg">
  <img alt="Singaraj B, machine learning practitioner" src="header-terminal-light.svg">
</picture>

I work on the internals of the open-source ML stack. Most of what I ship is other people's
libraries, fixed.

```console
$ gh pr list --author LK-maker-007 --state merged --json repository

huggingface/sentence-transformers   5   semantic search, ONNX export, hard-negative mining
huggingface/peft                    3   DoRA merge and unmerge, adapter injection
embeddings-benchmark/mteb           5   first Mauritian Creole task, model entries
embeddings-benchmark/results        3   published evaluation results
deepset-ai/haystack                 1   typing.Literal serialisation
                                   --
                                   17   merged, every diff and review thread public
```

Credited by name in [PEFT v0.21.0](https://github.com/huggingface/peft/releases/tag/v0.21.0)
and [sentence-transformers v5.7.0](https://github.com/huggingface/sentence-transformers/releases/tag/v5.7.0).

Three of the fixes are the same bug class, which is the one I keep finding: **something fails
and reports success.**

```python
# peft#3534  an adapter targeting no modules attached silently and trained nothing
model.add_adapter("second", LoraConfig(target_modules=["does_not_exist"]))
# before:  returns cleanly, adapts nothing, loss moves, you ship a broken model
# after:   raises NoMatchingPeftModuleError

# sentence-transformers#3909  a 1-D query embedding read as a batch
semantic_search_qdrant(query_embeddings=one_query)
# before:  30,522 vector searches, 30,522 identical result rows
# after:   one search
```

### Models

```console
$ hf api models/Singaraj --jq '.[] | "\(.id)  \(.downloads)/30d"'

Singaraj/morisien-embed-v1.5      302/30d   first embedding model for Mauritian Creole
Singaraj/morisien-embed           222/30d   0.928 mean F1, MTEB task I also authored
Singaraj/sante-embed               88/30d   rank 9 of 387, MTEB(Medical, v1)
Singaraj/MorisienMTBitextMining    45/30d   benchmark task, MIT
```

**sante-embed** is 1.5B, rank 9 of 387 on MTEB(Medical, v1). Complete 12-task submission,
which only 158 of 371 models on that board manage.

**morisien-embed** is the first text embedding model for Mauritian Creole, and
`MorisienMTBitextMining` is the language's first task in MTEB. Auditing the standard evaluation
split turned up 97% of the Kreyòl-MT test set sitting inside its own training data. I released a
leak-filtered benchmark instead of publishing the contaminated number.

### Writing

[morisien-embed: A Dedicated Text Embedding Model and Benchmark for Mauritian Creole](https://doi.org/10.5281/zenodo.21877805).
Sole author, indexed in OpenAIRE. Model, dataset and training code under MIT.

<sub>
<a href="https://huggingface.co/Singaraj">huggingface.co/Singaraj</a> ·
<a href="https://orcid.org/0009-0002-1502-362X">ORCID 0009-0002-1502-362X</a> ·
<img src="https://komarev.com/ghpvc/?username=LK-maker-007&style=flat&color=555555&label=views" alt="profile views">
</sub>
