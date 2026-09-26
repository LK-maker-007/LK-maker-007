from __future__ import annotations

import json
import os
import pathlib
import urllib.request

USER = "LK-maker-007"
ROOT = pathlib.Path(__file__).resolve().parent.parent

REPOS = [
    ("huggingface/sentence-transformers", "semantic search, ONNX export, hard-negative mining"),
    ("huggingface/peft", "DoRA merge and unmerge, adapter injection"),
    ("embeddings-benchmark/mteb", "first Mauritian Creole task, model entries"),
    ("embeddings-benchmark/results", "published evaluation results"),
    ("deepset-ai/haystack", "typing.Literal serialisation"),
]

MODELS = [
    ("Singaraj/morisien-embed-v1.5", "model", "first embedding model for Mauritian Creole"),
    ("Singaraj/morisien-embed", "model", "0.928 mean F1, MTEB task I also authored"),
    ("Singaraj/sante-embed", "model", "rank {rank} of {field}, MTEB(Medical, v1)"),
    ("Singaraj/MorisienMTBitextMining", "dataset", "benchmark task, MIT"),
]


def get(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "profile-build"})
    token = os.environ.get("GH_TOKEN")
    if token and "api.github.com" in url:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def merged_prs() -> list[tuple[str, int, str]]:
    out = []
    for repo, note in REPOS:
        q = f"author:{USER}+type:pr+is:merged+repo:{repo}"
        n = get(f"https://api.github.com/search/issues?q={q}&per_page=1")["total_count"]
        out.append((repo, n, note))
    return out


def downloads() -> list[tuple[str, int, str]]:
    rank = json.loads((ROOT / "rank.json").read_text())
    out = []
    for name, kind, note in MODELS:
        d = get(f"https://huggingface.co/api/{kind}s/{name}")["downloads"]
        out.append((name, d, note.format(**rank)))
    return out


def svg(dark: bool, prs: int, rank: dict) -> str:
    if dark:
        bg, chrome, border = "#0b0f19", "#111827", "#7c3aed"
        mid, hi, dim = "#2563eb", "#0891b2", "#64748b"
        prompt, body, sub = "#22c55e", "#e2e8f0", "#94a3b8"
        g1, g2, num, rk = "#22d3ee", "#a78bfa", "#fbbf24", "#22d3ee"
    else:
        bg, chrome, border = "#f8fafc", "#e2e8f0", "#6d28d9"
        mid, hi, dim = "#1d4ed8", "#0e7490", "#64748b"
        prompt, body, sub = "#16a34a", "#0f172a", "#475569"
        g1, g2, num, rk = "#0e7490", "#6d28d9", "#b45309", "#0e7490"
    o = "0.65" if dark else "0.5"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="860" height="290" viewBox="0 0 860 290" role="img" aria-label="Singaraj B, machine learning practitioner">
  <defs>
    <linearGradient id="glow" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{border}"/><stop offset="50%" stop-color="{mid}"/><stop offset="100%" stop-color="{hi}"/>
    </linearGradient>
    <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{g1}"/><stop offset="100%" stop-color="{g2}"/>
    </linearGradient>
  </defs>
  <rect width="860" height="290" rx="10" fill="{bg}"/>
  <rect x="0.5" y="0.5" width="859" height="289" rx="10" fill="none" stroke="url(#glow)" stroke-width="1.5" opacity="{o}"/>
  <rect x="1" y="1" width="858" height="34" rx="9" fill="{chrome}"/>
  <circle cx="22" cy="18" r="5.5" fill="#ef4444"/><circle cx="41" cy="18" r="5.5" fill="#eab308"/><circle cx="60" cy="18" r="5.5" fill="#22c55e"/>
  <text x="84" y="23" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="12.5" fill="{dim}">singaraj@ml — zsh — 86x24</text>

  <text font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="14.5">
    <tspan x="26" y="68" fill="{prompt}">$</tspan><tspan fill="{body}"> whoami</tspan>
    <tspan x="26" y="92" fill="url(#fade)" font-size="22" font-weight="700">Singaraj B</tspan>
    <tspan x="26" y="114" fill="{sub}">machine learning practitioner · retrieval, embeddings, adapter training</tspan>

    <tspan x="26" y="150" fill="{prompt}">$</tspan><tspan fill="{body}"> gh pr list --author {USER} --state merged | wc -l</tspan>
    <tspan x="26" y="172" fill="{num}">{prs}</tspan><tspan fill="{dim}">  across peft, sentence-transformers, mteb, haystack</tspan>

    <tspan x="26" y="206" fill="{prompt}">$</tspan><tspan fill="{body}"> mteb rank --benchmark "MTEB(Medical, v1)"</tspan>
    <tspan x="26" y="228" fill="{rk}">#{rank['rank']}</tspan><tspan fill="{dim}"> of </tspan><tspan fill="{body}">{rank['field']}</tspan>

    <tspan x="26" y="262" fill="{prompt}">$</tspan><tspan fill="{body}"> _</tspan>
  </text>
</svg>
"""


def main() -> None:
    prs = merged_prs()
    total = sum(n for _, n, _ in prs)
    rank = json.loads((ROOT / "rank.json").read_text())
    dl = downloads()

    w = max(len(r) for r, _, _ in prs)
    pr_lines = [f"{r:<{w}}  {n:>2}   {note}" for r, n, note in prs]
    pr_lines += [f"{'':<{w}}  --", f"{'':<{w}}  {total:>2}   merged, every diff and review thread public"]

    w2 = max(len(n) for n, _, _ in dl)
    dl_lines = [f"{n:<{w2}}  {d:>6}/30d   {note}" for n, d, note in dl]

    tpl = (ROOT / "README.template.md").read_text(encoding="utf-8")
    out = (tpl
           .replace("{{PRS}}", "\n".join(pr_lines))
           .replace("{{MODELS}}", "\n".join(dl_lines))
           .replace("{{RANK}}", str(rank["rank"]))
           .replace("{{FIELD}}", str(rank["field"])))
    (ROOT / "README.md").write_text(out, encoding="utf-8")
    (ROOT / "header-terminal-dark.svg").write_text(svg(True, total, rank), encoding="utf-8")
    (ROOT / "header-terminal-light.svg").write_text(svg(False, total, rank), encoding="utf-8")

    print(f"{total} merged PRs across {len(prs)} repos")
    for r, n, _ in prs:
        print(f"  {r:<34} {n}")
    print(f"rank {rank['rank']} of {rank['field']}")
    for n, d, _ in dl:
        print(f"  {n:<34} {d}/30d")


if __name__ == "__main__":
    main()
