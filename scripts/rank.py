from __future__ import annotations

import json
import pathlib

import mteb
import pandas as pd
import polars as pl
from huggingface_hub import hf_hub_download
from mteb.benchmarks._create_table import _borda_rank_from_long

MODEL = "Singaraj/sante-embed"
BENCHMARK = "MTEB(Medical, v1)"
ROOT = pathlib.Path(__file__).resolve().parent.parent


def main() -> None:
    tasks = {t.metadata.name for t in mteb.get_benchmark(BENCHMARK).tasks}
    parts = []
    for i in range(4):
        f = hf_hub_download("mteb/results", f"data/train-0000{i}-of-00004.parquet",
                            repo_type="dataset")
        d = pd.read_parquet(f, columns=["model_name", "task_name", "score", "is_public"])
        parts.append(d[d.task_name.isin(tasks) & d.is_public])
    df = pd.concat(parts, ignore_index=True)[["model_name", "task_name", "score"]]

    # revisions are joined, not deduplicated: a model's rows are split across its revisions and
    # dropping any of them costs it whole tasks, which scores 0 under Borda
    r = _borda_rank_from_long(pl.from_pandas(df)).to_pandas()
    row = r[r.model_name == MODEL]
    if row.empty:
        raise SystemExit(f"{MODEL} not present in {BENCHMARK} results")

    out = {"rank": int(row["Rank (Borda)"].iloc[0]), "field": int(df.model_name.nunique())}
    (ROOT / "rank.json").write_text(json.dumps(out) + "\n", encoding="utf-8")
    print(f"{MODEL}: rank {out['rank']} of {out['field']}")


if __name__ == "__main__":
    main()
