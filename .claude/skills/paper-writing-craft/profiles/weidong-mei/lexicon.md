# Phrase bank: formulaic collocations

> Word sequences that recur across the corpus, with the number of the 85 technical papers that use
> the exact sequence (n-gram document frequency, `stats_phrases.md`). They are the field's and this
> group's formulae: short, generic, and carrying no claim. Use them for the *frame* of a sentence;
> the content (variables, methods, numbers, claims) is always the paper's own.

## Section openers and roadmaps

| frame | papers |
|---|---|
| `In this section, we <verb> ...` | 80 |
| `In this section, we provide numerical results to evaluate the performance of ...` | 26 (as a full 8-gram) |
| `This section presents / provides ...` | rare variant |
| `The rest of this paper is organized as follows.` (`This paper is organized as follows`) | 39 |
| `Section II presents ... Finally, Section VI concludes this paper and discusses future directions.` | with the line above |
| `As shown in Fig. N, we consider <system>, where ...` | 50 (6-gram `as shown in Fig. N we`) |
| `In this paper, we <aim to | consider | propose | investigate | study> ...` | 63 (`in this paper`), 23 (`we aim to`) |

## Set-up, definitions, assumptions

`Let X denote ...` · `Denote by X ...` · `denote the set of ...` (35) · `We assume that ...` (68) ·
`is assumed to be` (62) · `are assumed to be` (37) · `is equipped with` (55) / `equipped with a` (55) ·
`is set to` (61) · `For convenience, we refer to ... as ...` · `Without loss of generality` (42) ·
`for any given <X>` (53) · `the total number of` (48) / `total number of` (49) · `the set of all` (34) ·
`the received signal at` (42) · `channel state information (CSI)` (41) · `with respect to (w.r.t.)` (57) ·
`in terms of` (54) · `we consider the following` (38) · `we consider a / the` (61 / 66).

## Formulation and derivation

`is given by` (81) · `can be expressed as` (58) · `can be obtained by` (37) · `can be simplified as` (34) ·
`can be recast as` · `is formulated as` (34, `the problem is formulated as`) · `we aim to maximize the` (31) ·
`to maximize the` (74) · `by jointly optimizing the` (42) · `the objective function` (54) /
`the objective function of` (35) · `the optimal solution to (P1)` (47) · `it can be shown that` (43) ·
`we can obtain` (47) · `Note that ...` (94% of papers; `Note that the` 66) ·
`Specifically,` (99%) · `Based on the above,` (42) · `As such, ...` (51) · `As a result, ...` (61) ·
`which, however, is still <non-convex>` · `To tackle this challenge / issue / problem, we ...` (56).

## Reading results

`It is observed that ...` (70) · `It is also observed that ...` (38) · `As shown in Fig. N, ...` (75) ·
`In Fig. N, we plot / compare <X> versus <Y>` (68 / 27) · `Fig. N shows the <X>` (40) ·
`versus the number of <X>` (47) · `the performance gap between <A> and <B>` (35) ·
`the performance of the proposed <X>` (42) / `of our proposed` (53) · `compared to the <benchmark>` (59) ·
`This is because ...` (49; 66% of papers in any form) · `thanks to ...` (47%) · `This implies / indicates / suggests ...` ·
`The possible reason is ...` · `to evaluate the performance of` (41) · `Unless otherwise stated / specified ...` ·
`All results are averaged over N independent channel realizations.`

## Contribution and prior-art frames

`The main contributions of this paper are summarized as follows.` · `We formulate ... by jointly
optimizing ...` · `Next, to solve ..., we propose ...` · `Finally, numerical results show / demonstrate ...` ·
`the authors in [x] <past-tense verb> ...` (48) · `In [x], ...` · `Unlike / Different from <prior work>, ...` ·
`However, all of the above works only ...` · `most of them rely on ...` · `Motivated by the above, ...` ·
`To fill this gap, ...` · `In our previous work [x], we ...`.

## Conclusion frames

`In this paper, we investigated / studied / proposed / considered ...` · `Specifically, ...` ·
`Numerical results showed / validated ...` · `This paper can be extended along several directions in
future work. For example, ...`

## Logic and insight connectors

`On the other hand` (49) · `In contrast` · `As well as` (57) · `To this end, we ...` (38 with `we`) ·
`to unveil / reveal insights` · `useful insights` · `it is worth noting that` (49) · `Recall that ...` ·
`In particular, ...` (92%) · `Similarly, ...` (56%) · `For example, ...` (76%).

## Field vocabulary that recurs (use when it is true of your system)

`degrees of freedom (DoFs)` · `channel state information (CSI)` · `line-of-sight (LoS)` ·
`far-field / near-field` · `fixed-position antennas (FPAs)` · `high-quality suboptimal solution` ·
`closed-form` · `near-optimal` · `performance gain / gap` · `trade-off` · `computational complexity` (92%) ·
`alternating optimization (AO)` · `successive convex approximation (SCA)` · `graph-based` ·
`sequential update` · `benchmark schemes` · `numerical results` · `efficacy / effectiveness / superiority` (79%).
