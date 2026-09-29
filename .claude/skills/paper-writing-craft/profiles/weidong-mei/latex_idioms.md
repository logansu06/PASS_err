# LaTeX and math idioms

> Counts are over the 85 technical papers (papers using it / total uses). The snippets are
> structural templates with placeholder content.

## Class, packages, bibliography

- `\documentclass[journal]{IEEEtran}` (76 of 102 papers use `journal`; 19 `conference`; letters
  use `[lettersize,journal]`, `[journal,comsoc]` for magazine-style articles). Section numbers
  are Roman (I, II, ...), set by the class.
- Front matter: `\begin{IEEEkeywords}` (65) with 5 index terms; `\thanks{}` for affiliations (73);
  `\IEEEPARstart` drop cap in 11 papers.
- Packages seen: `graphicx` (all), `amsmath`, `amssymb`, `cite` (62 explicit), `algorithm` +
  `algorithmic` (or `algpseudocode`), `subfigure` (61) / `subfig` (26) / `subcaption` (17), `bm` (61),
  `color` / `xcolor`, `multirow` (33), `booktabs` (25), `amsthm` (29), `epstopdf`, `balance` (20).
- `\bibliographystyle{IEEEtran}` (68). Numeric citations. Most `\cite{}` hold one key (75%),
  82 papers also use multi-key `\cite{a,b,c}`. Write `the authors in \cite{x} studied ...` and
  sentence-initial `In \cite{x}, ...`; a plain space (not `~`) before `\cite` in 89% of the cites that follow a word (3,548 vs 420 with `~`).
- `\vspace{-...}` is used in 68 papers (1,049 times) to reclaim space after figures, equations, and
  captions; it is a page-limit tactic, applied last.

## Notation (85 papers agree on the first three)

| object | form | note |
|---|---|---|
| sets | `\mathcal{N}`, `\mathcal{M}` (85 of 85) | index sets `\mathcal{N}=\{1,\ldots,N\}`; `n\in\mathcal{N}` |
| fields | `\mathbb{C}^{M\times N}`, `\mathbb{R}` (73) | `\mathbb{E}\{\cdot\}` (45), `\mathcal{CN}(0,\sigma^2)` (56) |
| definitions | `\triangleq` (70 papers, 771 uses) | not `:=` (4 papers) |
| vectors, matrices | bold (`\mathbf`, `\boldsymbol`, or a short macro) | lowercase vector, uppercase matrix; mixed spellings across papers |
| named functions / labels | `\mathrm{}` or `\text{}` inside math | `\text{}` 79 papers, `\mathrm{}` 38 |
| optimal value | superscript `\star` (41 papers), `^{*}` also used | pick one per paper |
| iteration | `x^{(l)}`, `\eta^{(l-1)}` | `l` or `r` for the iteration counter |
| transpose / Hermitian | `(\cdot)^T`, `(\cdot)^H` | listed in the `Notations:` paragraph |
| norm | `\|\cdot\|` or `\left\|\cdot\right\|` | 31 papers use `\left`/`\right` norms |

Personal macro set in recent group sources (define once in the preamble and reuse): `\bs{x}` =
`\boldsymbol{x}`, `\mbf{W}` = `\mathbf{W}`, `\ca{N}` = `\mathcal{N}`, `\mrm{EE}` = `\mathrm{EE}`,
`\ib{C}` = `\in\mathbb{C}`, `\ic{N}` = `\in\mathcal{N}` (so `n\ic{N}`).

## Notations paragraph (end of the introduction: F 62%, Cf 67%, L 32%)

`Notations:` (or `\emph{Notations}:` / `The following notations are used in this paper.`) then
one sentence per group: `Bold lowercase and uppercase symbols denote vectors and matrices,
respectively. (\cdot)^T and (\cdot)^H denote the transpose and conjugate transpose. \mathbb{C}^{M\times N}
denotes the set of complex matrices. \|\cdot\| denotes the Euclidean norm. \mathcal{CN}(0,\sigma^2)
denotes the circularly symmetric complex Gaussian distribution. |\mathcal{A}| denotes the
cardinality of set \mathcal{A}. \mathcal{O}(\cdot) denotes the order of complexity.`
Only symbols the paper uses.

## Equations

```latex
% inline definition inside a sentence
The received signal power is given by
\begin{equation}\label{eqn_Power}
  \gamma(\bs{X},\bs{w}) \triangleq \left|\bs{h}^H(\bs{X})\bs{w}\right|^2,
\end{equation}
where $\bs{h}(\bs{X})\in\mathbb{C}^{N\times 1}$ denotes the channel and $\bs{w}$ the beamforming vector.
```
`\begin{equation}` (78 papers), `\begin{align}` (79), `\nonumber` to number only the equations
that are cited (80 papers). Punctuate: a comma when `where ...` follows, a period when the equation
ends the sentence (83% of display equations carry `,` or `.`). Cite with `\eqref{...}` (43 papers) or
`(\ref{...})` (25), rendered `(12)`; no `Eq.`.

## Optimization problems

```latex
\begin{subequations}
\begin{align}
  \text{(P1)}\quad &\underset{\bs{X},\bs{w}}{\max}\quad \gamma(\bs{X},\bs{w}) \nonumber\\
  \mathrm{s.t.}\quad & x_i - x_j \ge D_{\min},\ \forall i\ne j,\label{eqn_Spacing}\\
  & \bs{x}\in\mathcal{C}, \ \|\bs{w}\|=1.\label{eqn_Region}
\end{align}
\end{subequations}
```
`(P1)` label left of the objective (1,125 plain `(P1)` mentions, 134 as `\text{(P1)}` in an align),
`\mathrm{s.t.}` / `\text{s.t.}` (63 papers), constraints labelled and explained by `where` or
`i.e.`. After the block: `However, (P1) is a non-convex problem that is challenging to solve due to
the spacing constraint (\ref{eqn_Spacing}).` Sub-problems continue the numbering `(P2)`, `(P3)`,
or `(P2-1)`.

## Lemmas, propositions, remarks

- Environments: Proposition (75 uses), Remark (63), Lemma (48), Theorem (22), Definition (17),
  Corollary (8). `\newtheorem{lemma}{\bf Lemma}` style: bold heading, in 15 papers the
  `\bf` form; body italic by default.
- Statement: `Let ... denote ... If ..., <consequence> holds / can be approximated as ...`.
- Proofs live in the appendix, titled `Proof of Proposition 1` (55 titles) with the main text
  saying `Proof: See Appendix A.` (31) and, rarely, a `proof` environment (10 papers, 29 uses).
- Remark: starts by contrasting with a conventional case (`Different from ...`) or stating an
  implication (`The main reason for ... lies in the fact that ...`); may contain its own equation.
- Footnotes (58 papers, 137 uses) hold practical justifications of assumptions (`Note that these
  conditions usually hold in practice, as ...`).

## Figures, tables, algorithms (environments)

```latex
\begin{figure}[!t]
  \centering
  \captionsetup{justification=raggedright,singlelinecheck=false}
  \centerline{\includegraphics[width=0.45\textwidth]{SysModel.eps}}
  \captionsetup{font=footnotesize}
  \caption{<System> with <feature>.}\label{fig:sysmodel}
\end{figure}

% group of panels: empty subfloat labels, panels enumerated in the caption
\begin{figure}[!t]
  \centering
  \subfloat[]{\includegraphics[width=0.50\linewidth]{FigA.eps}}
  \subfloat[]{\includegraphics[width=0.50\linewidth]{FigB.eps}}
  \captionsetup{font=footnotesize}
  \caption{(a) <Metric A> versus <x>; (b) <Metric B> versus <x>.}
\end{figure}

\begin{algorithm}[!t]
  \caption{Proposed Algorithm for Solving (P1)}
  \begin{algorithmic}[1]
    \STATE Initialize $\bs{x}^{(0)}$ and the convergence accuracy $\epsilon$.
    \STATE Set $l=0$.
    \REPEAT
      \STATE Set $l=l+1$.
      \STATE Update $\bs{w}^{(l)}$ according to \eqref{eqn_W}.
      \STATE Update $\bs{x}^{(l)}$ via \eqref{eqn_X}.
    \UNTIL{the increase of the objective value is below $\epsilon$.}
    \STATE Output $\bs{w}^{\star}$ and $\bs{x}^{\star}$ as the optimized solution to (P1).
  \end{algorithmic}
\end{algorithm}
```
Tables: `\begin{table}[t]\centering\caption{Simulation Parameters}` caption above,
`\renewcommand{\arraystretch}{1.2}` + `\hline`.

## Benchmarks in the results section

```latex
We compare our proposed algorithm with the following benchmarks:
\begin{itemize}
  \item \textbf{FPA}: The $N$ antennas are deployed symmetrically and separated by the minimum distance $D_{\min}$. ...
  \item \textbf{Antenna selection (AS)}: In this benchmark, ... Among them, $N$ antennas are selected for transmission.
\end{itemize}
```
(21 papers use `\item \textbf{name}:`; the rest write `Benchmark 1: ...` paragraphs.)
`\emph{}` marks a coined term at its definition and occasionally one key word
(`solved \emph{optimally}`); 63 papers use it, ~18 times each on average.

## Cross-reference spelling

`Fig.~\ref{}` / `Figs.~\ref{} and \ref{}`, `Section~\ref{}`, `Table~\ref{}`, `Algorithm~\ref{}`,
`Lemma~\ref{}`, `Proposition~\ref{}`, `(\ref{})` or `\eqref{}` for equations. `Fig. \ref` with a plain
space is more frequent in the sources (805 vs 377 with `~`) but `~` is the safe form.
