#!/usr/bin/env python3
"""fetch_corpus.py - download the arXiv LaTeX sources of every paper that lists an author.

  python fetch_corpus.py --author "Mei_Weidong" --out corpus/ [--workers 4]

Writes  <out>/meta.json  (id, title, authors, date, category, author position)
        <out>/src/<id>.eprint   (the arXiv e-print, tar.gz or single .gz)

Uses the arXiv API and `arxiv.org/e-print` (export mirror) through the system `curl`
(python's urllib fails the certificate chain on some Windows installs). Downloads run
with a small worker pool and retry with back-off on HTTP errors; be considerate with the
number of workers. The sources are read for statistics only and are not redistributed.
Then run: style_stats.py -> aggregate.py -> fig_stats.py -> aggregate_floats.py ->
phrases.py -> extras.py -> calibrate.py --write-norms (see profiles/weidong-mei/README.md).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import quote

UA = "aris-style-distill/1.0"
NS = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}


def curl(url: str, out: Path | None = None, retries: int = 4) -> bytes:
    for i in range(retries):
        cmd = ["curl", "-sSL", "-m", "180", "-A", UA, "-w", "\n%{http_code}", url]
        r = subprocess.run(cmd, capture_output=True)
        body, _, code = r.stdout.rpartition(b"\n")
        if code.strip() == b"200":
            if out:
                out.write_bytes(body)
            return body
        time.sleep(3 * (i + 1))
    raise RuntimeError(f"failed: {url}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--author", required=True, help='arXiv author query, e.g. "Mei_Weidong"')
    ap.add_argument("--name-contains", help="substring that must appear in an author name (default: the query with _ -> space, reversed)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    out = Path(a.out)
    (out / "src").mkdir(parents=True, exist_ok=True)
    q = quote(f'au:"{a.author}"')
    xml = curl(f"https://export.arxiv.org/api/query?search_query={q}&start=0&max_results=300&sortBy=submittedDate&sortOrder=descending")
    root = ET.fromstring(xml)
    want = a.name_contains or " ".join(reversed(a.author.split("_")))
    rows = []
    for e in root.findall("a:entry", NS):
        authors = [x.find("a:name", NS).text for x in e.findall("a:author", NS)]
        if not any(want.lower() in n.lower() for n in authors):
            continue
        aid = e.find("a:id", NS).text.split("/abs/")[-1]
        rows.append(
            {
                "id": aid,
                "title": re.sub(r"\s+", " ", e.find("a:title", NS).text).strip(),
                "authors": authors,
                "pub": e.find("a:published", NS).text[:10],
                "cat": e.find("x:primary_category", NS).get("term"),
            }
        )
    (out / "meta.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"{len(rows)} papers listed")

    def get(r):
        base = r["id"].split("v")[0]
        dst = out / "src" / f"{base}.eprint"
        if dst.exists() and dst.stat().st_size > 0:
            return base, "cached"
        try:
            curl(f"https://export.arxiv.org/e-print/{base}", dst)
            return base, "ok"
        except RuntimeError as ex:
            return base, str(ex)

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        for base, st in ex.map(get, rows):
            if st not in ("ok", "cached"):
                print("FAILED", base, st, file=sys.stderr)
    print("done ->", out)


if __name__ == "__main__":
    main()
