# Discussion

Marking the current endpoint's neighbors before extending it can remove
legal paths. A cube path that returns to its first coordinate gives a small
regression case. The search now delays those marks until the endpoint becomes
an earlier vertex. The independent adjacency check catches any chord admitted
by an incorrect bitmap update.

Fresh higher-dimensional discovery would require a separate resource-bounded
experiment with recorded search settings. The retained paths establish
reachable lengths for the archived runs and the published sequences.
Heuristic pruning discards viable branches, so a path recovered from a
pruned run provides a lower bound. The cube maximum comes from the complete
enumeration.
