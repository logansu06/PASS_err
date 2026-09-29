#!/usr/bin/env python3
"""selftest.py - assertions for style_gate.py, fact_guard.py and rules.json (standard library only).

  python selftest.py            # exit 0 = all checks passed
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import fact_guard  # noqa: E402
import style_gate as G  # noqa: E402

PROFILE = "weidong-mei"

GOOD = r"""
\documentclass[journal]{IEEEtran}
\begin{document}
\title{A Test Paper}
\begin{abstract}
Movable antenna (MA) has emerged as a promising technology for wireless communications. However, the antenna position
optimization is challenging. In this paper, we aim to maximize the received signal power by optimizing the positions.
To tackle this challenge, we first consider a special case. Numerical results show that the proposed algorithm
outperforms the benchmarks.
\end{abstract}
\section{Introduction}
Recently, MA has attracted increasing attention. As compared to fixed-position antennas (FPAs), MAs can move, i.e., they
reshape the channel. However, most existing works only consider a single user, which may not fully exploit the gain.
To fill this gap, we study a multi-user system, as shown in Fig.~\ref{fig:sys}.
\section{System Model}
As shown in Fig.~\ref{fig:sys}, we consider a downlink system, where a BS equipped with $N$ antennas serves $K$ users.
The received power is given by
\begin{equation}\label{eqn_P}
P = |h|^2,
\end{equation}
where $h$ denotes the channel. Note that (\ref{eqn_P}) holds for any given $N$.
\begin{figure}[!t]
\centering
\caption{Received SNR versus the number of sampling points.}
\end{figure}
\section{Numerical Results}
In this section, we provide numerical results to evaluate the performance of the proposed algorithm. It is observed
that the received SNR increases with $N$, thanks to the array gain.
\section{Conclusion}
In this paper, we investigated the MA position optimization problem.
\end{document}
"""

BAD = r"""
\documentclass[journal]{IEEEtran}
\begin{document}
\begin{abstract}
We truly believe this is groundbreaking! The scheme is proposed --- and it indeed works, see \cite{a}.
\end{abstract}
\section{introduction}
It's a novel, novel paradigm. Figure~\ref{fig:1} shows the result, i.e. it works. See Eq. \eqref{e1}.
\begin{figure}[!t]
\caption{This figure shows the throughput versus power. It is very good and the trends are clear}
\end{figure}
The the method works.
\end{document}
"""


def expect(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (f"  [{detail}]" if detail and not cond else ""))
    return bool(cond)


def gate(text: str, register="full"):
    d = Path(tempfile.mkdtemp())
    (d / "a.tex").write_text(text, encoding="utf-8")
    rep = G.run_gate(d / "a.tex", PROFILE, register, metrics=False)
    return {r["id"]: r for r in rep["results"]}


def main():
    ok = True
    rules = json.load(open(HERE.parent / "profiles" / PROFILE / "rules.json", encoding="utf-8"))["rules"]
    ids = [r["id"] for r in rules]
    ok &= expect("rules.json ids are unique", len(ids) == len(set(ids)))
    doc = (HERE.parent / "profiles" / PROFILE / "gate_mechanical.md").read_text(encoding="utf-8")
    missing = [i for i in ids if f"| {i} |" not in doc]
    ok &= expect("gate_mechanical.md lists every rule id", not missing, f"missing {missing}")
    ok &= expect("norms.json has letter/full/all", set(json.load(open(HERE.parent / 'profiles' / PROFILE / 'norms.json')).keys()) >= {"letter", "full", "all"})

    g = gate(GOOD)
    fails = [i for i, r in g.items() if r["status"] == "FAIL"]
    ok &= expect("compliant sample has no FAIL rule", not fails, str(fails))

    b = gate(BAD)
    for rid, why in [
        ("MM01", "dash"), ("MM02", "exclamation"), ("MM03", "truly / groundbreaking"), ("MM04", "contraction"),
        ("MM05", "Figure~\\ref"), ("MM07", "i.e. without comma"), ("MM09", "the the"),
    ]:
        ok &= expect(f"{rid} fires on {why}", b[rid]["n"] >= 1, f"n={b[rid]['n']}")
    ok &= expect("MM06 fires on 'Eq.'", b["MM06"]["n"] >= 1 or b["MM06"]["allowed"] >= 1)
    ok &= expect("MM20 flags a 30-word abstract", b["MM20"]["n"] >= 1)
    ok &= expect("MM21/MM22 flag a two-sentence caption without period", b["MM21"]["n"] + b["MM22"]["n"] >= 1)
    ok &= expect("MM40 counts novel/paradigm", b["MM40"]["n"] >= 3)

    # fact guard
    d = Path(tempfile.mkdtemp())
    a1 = r"We achieve 5 dB at 30 GHz \cite{x,y}, see Fig.~\ref{f1} and $N=8$."
    a2 = r"At 30 GHz we reach 5 dB \cite{x,y}, as shown in Fig.~\ref{f1} with $N=8$."
    a3 = r"We achieve 6 dB at 30 GHz \cite{x}, see Fig.~\ref{f1} and $N=8$."
    for n, t in (("a1", a1), ("a2", a2), ("a3", a3)):
        (d / f"{n}.tex").write_text(t, encoding="utf-8")
    ok &= expect("fact_guard: reworded sentence keeps every fact", fact_guard.main([str(d / "a1.tex"), str(d / "a2.tex")]) == 0)
    ok &= expect("fact_guard: changed number and dropped cite key are detected", fact_guard.main([str(d / "a1.tex"), str(d / "a3.tex")]) == 1)

    print("\nALL CHECKS PASSED" if ok else "\nSOME CHECKS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
