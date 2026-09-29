# Upstream (snl-default) mechanical gate applied to 85 technical papers of the corpus

Per-1,000-word hit rate of the upstream regexes on the author's own papers. Every non-zero row is text the upstream gate would have rejected.

| upstream rule | median /1k | p90 /1k | papers with >=1 hit |
|---|---|---|---|
| M1 em-dash | 0.00 | 0.32 | 11/85 (13%) |
| M5 banned adjectives | 1.35 | 2.95 | 84/85 (99%) |
| M6 throat-clearing openers | 1.31 | 2.27 | 84/85 (99%) |
| M6 'It is worth noting / should be noted' | 0.13 | 0.47 | 48/85 (56%) |
| M11 passive voice | 18.16 | 21.65 | 85/85 (100%) |
| M12 in order to / in terms of / the fact that | 0.32 | 0.88 | 66/85 (78%) |
| M13 weak qualifiers | 0.00 | 0.54 | 39/85 (46%) |
| M16 pompous single words | 0.32 | 1.63 | 61/85 (72%) |
| M17 fancy verbs (delve/harness/orchestrate ...) | 0.00 | 0.27 | 21/85 (25%) |
| M18 'In this paper/section, we' | 0.71 | 1.34 | 84/85 (99%) |
| M14 firstly/secondly | 0.00 | 0.00 | 2/85 (2%) |
| M2 antithesis (rather than / not only ... but / on the other hand) | 0.00 | 0.36 | 38/85 (45%) |
