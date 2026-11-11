# Exact finite contract

## Input and plans

A rooted binary tree has terminal payoff pairs, player nodes with player index 0 or 1, and chance nodes with two exact probabilities. Node indices increase along every edge, and every nonroot node has one parent. At most six player decisions and two chance decisions. A full pure profile assigns one action at every player decision, including decisions unreachable because of that same player's earlier actions. No strategy equivalence reduction.

Expected continuation utility V_i(k,s) is terminal payoff at a leaf, the chosen child's value at a player node, or the probability-weighted sum at a chance node. Root reach is computed separately. In particular a node with zero root reach still has a well-defined continuation value. No conditioning by division is used.

## Classification

Root one-node stability: changing only one player node never gives that node's owner a positive root utility gain. This is root-weighted agent-form stability only, not a claim of Nash or subgame perfection.

Root Nash: each player's complete alternative assignment over its own descendant decisions at node 0 has payoff no greater than its current root payoff. Other players' actions stay fixed.

Subgame perfection: repeat this full-player Nash test starting separately at every nonterminal node. Every node starts a subgame because all information sets are singletons. Including terminal nodes is vacuous. All alternatives, including the unchanged plan, are retained, so best gains are nonnegative and equilibrium means gain exactly zero.

The finite perfect-information one-deviation principle tests continuation gains at every player node, not reach-weighted gains only at the root. It does not justify replacing full-player root Nash by one-node root stability. The same-player control makes that error visible.

## Backward-induction correspondence

A leaf has one empty plan. A chance node combines every pair of child equilibrium plans. A player node combines every pair of child equilibrium plans, evaluates both actions under that fixed pair, and retains every maximizing action for the moving player. Off-path child plans remain in the combined plan. Sorting actions lexicographically makes output deterministic.

By finite induction each retained plan is equilibrium in all child subgames. Choosing an optimal current action gives equilibrium at the parent as well. Conversely every pure subgame-perfect plan restricts to a retained child plan and must choose a maximizing parent action. Hence the correspondence is exactly the set of pure subgame-perfect plans, including ties. Chance nodes use fixed distributions and impose no optimizing player at that node. Zero-probability child subgames remain required.

This is established finite backward induction, not a new theorem or formal proof. The implementation checks its root correspondence against the separate full-deviation classification. The independent verifier builds every subtree's accepted plans directly using leaf paths and unilateral alternatives, not induction.

## Certificate

Schema subgamelab/1 includes input, ordered decision nodes, every lexicographic profile, all node continuation payoff pairs and root reach probabilities, every one-node root/continuation gain, and every nonterminal-node/player audit with all alternatives and maximizing ties. Three ID lists give the classification sets. Every node's backward-induction correspondence gives decision-node keys and all complete subplans. Exact recursive comparison is type-sensitive and rejects extra, missing, reordered or forged content.

Native input rational syntax is canonical Fraction spelling, with |numerator|<=1000 and denominator<=1000. Generated arithmetic is unbounded exact Fraction. Browser uses BigInt rationals and the same input bounds. Truth booleans are not integers in native schema. Python duplicate JSON keys are rejected; browser JSON.parse keeps the last duplicate. Native text cap is 8MiB, browser editable input cap 32768 characters. The bounded generator's result can be larger than its input. The browser verifier is same-engine; only the Python path-census checker is independent.
