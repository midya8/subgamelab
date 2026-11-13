# SubgameLab

SubgameLab checks small, supplied two-player sequential games with exact rational arithmetic. Compare root one-node stability, full-player pure Nash equilibrium and subgame perfection while retaining off-path choices and backward-induction ties.

## Choose a stability question

- **Root one-node stability:** can a player improve the root payoff by changing a single decision?
- **Root Nash:** can a player improve it by changing any combination of its decisions?
- **Subgame perfection:** does a profitable full-player change exist in any continuation, including one with zero root reach probability?

A negative answer to the first question does not settle the second. Root Nash
alone does not rule out a profitable change in an unreached continuation.

## Finite-game controls

The default control has P1 choose action 0 for payoff (1, 4), or action 1 to a P2 decision. P2's action 0 gives (-1, 0); action 1 gives (3, 2). Complete plans 00 and 11 are root Nash. Plan 00 contains an empty threat: P2 would gain 2 by changing its action in the unreached continuation, although its root gain is 0. Only 11 is subgame perfect.

A same-player control gives P1 root payoff 1 by stopping, 0 by entering then stopping, and 3 by entering then continuing. Plan 00 has no profitable one-node root change but gains 2 from changing both nodes. Root one-node stability is not Nash.

A chance-zero control always reaches a terminal (2, 2), while probability 0 leads to P2 choosing (0, 0) or (0, 5). Both plans are root Nash, but only the latter is subgame perfect. We evaluate that subtree directly, never divide by zero reach.

Ties are preserved as complete contingent plans, not merged outcomes. A tied P2 continuation yielding P1 either 1 or 4 changes P1's root choice relative to outside payoff 2. Both resulting subgame-perfect plans survive. All-zero three-decision control keeps all 8 plans.

## Run locally

Python 3.10+, standard library runtime. Node 22 and Chrome for browser checks. No API keys.

```sh
python -m tools.make_cases
python -m unittest discover -s tests -v
node tools/crosscheck.mjs
npm test
python -m tools.check_installed
python -m http.server 8000 --directory docs
```

Open the local inspector at localhost:8000. Select complete plans, continuation roots, and deviation players. Every alternative for a player's descendant decisions is shown. Tables and the complete tree scroll sideways on small screens. Editing input clears stale evidence and disables downloads until recomputation.

```sh
python -m subgamelab solve input.json > certificate.json
python -m subgamelab verify certificate.json
pip install .
subgamelab verify certificate.json
```

Native generation uses dynamic value evaluation and child-plan Cartesian products for backward induction. A separate checker imports validation only: it enumerates terminal paths and every unilateral subgame alternative, then reconstructs every certificate field. Browser BigInt generation is cross-checked against complete native reports; browser replay is same-engine and is not called independent verification.

## Verification

- 14 Python tests, including all 2,916 two-decision player/payoff assignments: 4 owner patterns times 729 ternary six-payoff assignments.
- 65 complete cross-language reports: 10 developed controls and 55 seeded trees, 1,233 complete profiles, 12,820 subgame/player audits, and 48,250 full-player alternatives.
- 317 noninput primitive certificate forgeries rejected per engine; shape, type, ordering and duplicate-key failures also checked.
- Actual Chrome: 40 responsive views at 1440/768/390/320, 388 plan selections, 1,209 continuation selections, 2,837 alternative rows, and 20 trusted input/certificate downloads. Downloaded certificates replayed by native checker.
- Installed wheel outside checkout: 5 module origins, 10 controls, 2 entrypoints, 20 CLI forgery failures.
- Optional actual Nashpy 0.0.43 reference: 533 input-built normal-form matrices, 2,353 pure-pair best-response checks, 1,233 profile classifications. Matrices derive from input terminal paths, not expected certificate values. Rational matrices are scaled to integers; largest absolute scaled entry 18 on this corpus. Nashpy uses numerical isclose, so this is supplemental evidence, not an exact proof.

```sh
pip install nashpy==0.0.43
python -m tools.check_reference
```

These are developed finite controls, not held-out tournaments or a speed/real-agent-quality benchmark. [CONTRACT.md](CONTRACT.md) gives the exact semantics and proof outline. [SOURCES.md](SOURCES.md) credits established theory and existing software.

## Boundaries

Two players, at most 6 binary decisions and 2 binary chance nodes, at most 17 nodes. Every information set is a singleton. Canonical rational strings with absolute numerator and denominator at most 1000. Parent-before-child node indices; each nonroot node has exactly one parent. Chance probabilities are nonnegative and sum exactly to 1. Complete pure plans include self-precluded decisions. No pruning, hidden information, mixed equilibrium enumeration, CFR, learning, payoff estimation, market advice, new theorem, formal verification or scalability claim.

A valid certificate establishes arithmetic relative to its included input, not payoff provenance or real-world rationality. Browser JSON.parse keeps last duplicate keys and limits input to 32,768 characters; native JSON rejects duplicate keys and limits input/certificate text to 8 MiB. No external code, data, figures, models or weights copied. Implementation and developed controls by Midya Rahmani.
