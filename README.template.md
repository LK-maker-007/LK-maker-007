<picture>
  <source media="(prefers-color-scheme: dark)" srcset="header-terminal-dark.svg">
  <img alt="Singaraj B, machine learning practitioner" src="header-terminal-light.svg">
</picture>

```console
$ gh pr list --author LK-maker-007 --state merged --json repository

{{PRS}}
```

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

{{MODELS}}
```

**sante-embed** is 1.5B, rank {{RANK}} of {{FIELD}} on MTEB(Medical, v1). It is one of the
{{COMPLETE_FIELD}} models that submitted all {{TASKS}} tasks, and is rank {{COMPLETE_RANK}} among them.

**morisien-embed** is the first text embedding model for Mauritian Creole, and
`MorisienMTBitextMining` is the language's first task in MTEB. Auditing the obvious evaluation
split turned up 97% of Kreyòl-MT's test set already inside the training data I was merging. I
benchmarked on MorisienMT's test split instead, which shares no Creole sentence with training.

### Writing

[morisien-embed: Text Embedding Models and Evaluation for Mauritian Creole](https://doi.org/10.5281/zenodo.21877805).
Sole author, indexed in OpenAIRE. Model, dataset and training code under MIT.

<p>
<a href="https://huggingface.co/Singaraj"><img alt="Hugging Face" height="20" src="https://img.shields.io/badge/%F0%9F%A4%97-Singaraj-lightgrey?style=flat&labelColor=555555"></a>
<a href="https://orcid.org/0009-0002-1502-362X"><img alt="ORCID" height="20" src="https://img.shields.io/badge/ORCID-0009--0002--1502--362X-lightgrey?style=flat&labelColor=555555"></a>
<img alt="profile views" height="20" src="https://komarev.com/ghpvc/?username=LK-maker-007&style=flat&color=lightgrey&label=views">
</p>
