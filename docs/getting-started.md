# Getting started

## Installation

From the repository root, use Python 3.11 or newer and install the package into a virtual environment.

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
```

NumPy and SciPy are installed with the package. The `dev` extra includes pytest,
Matplotlib, and the optional memory profiler. Use `.[visualization]` if you only need
the plotting extra.

## Basic example

The search returns a path whose consecutive vertices differ by one bit.
`validate_snake` additionally checks that every nonconsecutive pair is distinct
and has Hamming distance greater than one.

```python
from snake_in_box import pruned_bfs_search, transition_to_vertex, validate_snake

snake = pruned_bfs_search(dimension=3, memory_limit_gb=0.1, verbose=False)
vertices = transition_to_vertex(snake.transition_sequence, snake.dimension)
valid, reason = validate_snake(vertices)
assert valid, reason
print(snake.get_length(), vertices)
```

The example prints `4 [0, 1, 3, 7, 6]`. Path length counts edges. The memory
argument controls frontier pruning after child generation. A large search can
allocate more memory than the pruning target.

## Retained sequences

`get_known_snake(dimension)` retrieves a stored transition sequence in dimensions
9 through 13. `get_known_record(dimension)` returns a literature value for the
dimensions covered by the package table. Read [the manuscript results](manuscript/03_results.md)
for the validated archive and literature values in each dimension.

## Testing and plotting

Use `MPLBACKEND=Agg python -m pytest -q` for the local suite. See the
[visualization guide](guides/visualization.md) for plots and
[the manuscript recipe](manuscript/README.md) for a headless example with saved evidence.
