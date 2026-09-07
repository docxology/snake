#!/usr/bin/env python3
"""Comprehensive exhaustive search for dimensions 11-16 (serial front door).

Search strategies, logging, validation, and progress saving live in
``snake_in_box.search.crack``; this script only delegates.

Strategies run per dimension:
1. Priming from known lower dimensions (N-1, N-2, N-3)
2. Direct pruned BFS search from empty snake
3. Multiple seed starting points (truncated snakes, various prefixes)

All results are validated and compared against known records. Progress is
saved periodically to ``output/crack_results/`` and resumed on re-run;
Ctrl-C keeps saved progress. Exits 0 on completion.

For the parallel (one process per dimension) variant, see
``crack_high_dimensions_parallel.py``.
"""

from snake_in_box.search.crack import run_all_dimensions

if __name__ == "__main__":
    run_all_dimensions()
