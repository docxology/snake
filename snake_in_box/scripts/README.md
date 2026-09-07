# snake_in_box/scripts — Orchestration Scripts (thin orchestrators)

Command-line front doors that call into `snake_in_box` library modules. Each
script only parses arguments, sets up paths/logging, and makes one delegated
call into `snake_in_box/` (see `AGENTS.md` for the contract).

Scripts import the installed package — there are no `sys.path` hacks. Run them
from the repository root via uv, which syncs and installs the package first:

```bash
uv run --extra dev python snake_in_box/scripts/run_analysis.py --help
```

(`--extra dev` adds matplotlib/pytest; scripts that only print or move files
run without it.)

## Inventory

| Script | Purpose | Delegates to | Command |
|--------|---------|--------------|---------|
| `run_analysis.py` | Analysis pipeline for dims 1-16 (`--mode basic\|full\|organized`) | `snake_in_box.analysis.workflows` | `uv run --extra dev python snake_in_box/scripts/run_analysis.py` |
| `crack_high_dimensions.py` | Record searches for dims 11-16, serial and resumable | `snake_in_box.search.crack` | `uv run python snake_in_box/scripts/crack_high_dimensions.py` |
| `crack_high_dimensions_parallel.py` | Same searches, one process per dimension | `snake_in_box.search.crack` | `uv run python snake_in_box/scripts/crack_high_dimensions_parallel.py` |
| `generate_snakes_for_all_dimensions.py` | Generate/retrieve baseline snakes for dims 1-16 | `snake_in_box.benchmarks.generation` | `uv run python snake_in_box/scripts/generate_snakes_for_all_dimensions.py` |
| `reorganize_outputs.py` | Move stray artifacts into `output/` subdirectories | `snake_in_box.utils.outputs` | `uv run python snake_in_box/scripts/reorganize_outputs.py` |
| `run_tests.py` | Run the test suite (pytest, verbose) | `pytest snake_in_box/tests/` | `uv run python snake_in_box/scripts/run_tests.py` |

## `run_analysis.py`

Single front door for the three analysis workflows; all pipeline logic lives in
`snake_in_box/analysis/workflows.py`:

```bash
uv run --extra dev python snake_in_box/scripts/run_analysis.py --mode organized   # default
uv run --extra dev python snake_in_box/scripts/run_analysis.py --mode full
uv run --extra dev python snake_in_box/scripts/run_analysis.py --mode basic
uv run --extra dev python snake_in_box/scripts/run_analysis.py --output-base output
```

- `--mode organized` (default): analysis/validation/performance/feasibility reports, graphical abstract, individual + heatmap/3D/transition-matrix visualizations, comprehensive data exports.
- `--mode full`: adds exponential-analysis report, performance plots, and computation-time tracking.
- `--mode basic`: analysis/validation/performance reports, graphical abstract, per-dimension visualizations, simple JSON dump.
- Flags: `--mode {basic,full,organized}`, `--output-base DIR` (default `output/`).
- Exit status: 0 on success; argparse exits 2 on unknown flags.

Outputs (under the output base): `reports/`, `visualizations/`, `graphical_abstracts/`, `data/`.

## `crack_high_dimensions.py` / `crack_high_dimensions_parallel.py`

Front doors for the dim 11-16 record searches. Strategies, validation, logging,
and resumable progress live in `snake_in_box/search/crack.py`; the parallel
variant adds multiprocessing wiring (one process per dimension):

```bash
uv run python snake_in_box/scripts/crack_high_dimensions.py            # serial
uv run python snake_in_box/scripts/crack_high_dimensions_parallel.py   # parallel
```

Outputs: `output/crack_results/` (best + timestamped JSON per dimension, summary report), `output/crack_logs/` (per-dimension logs), and `output/crack_visualizations/` (parallel variant). Ctrl-C keeps saved progress; re-runs resume from `output/crack_results/dimension_<N>_best.json`. Long-running: dims 14-16 are research-scale searches.

## `generate_snakes_for_all_dimensions.py`

Prints per-dimension generation results for dims 1-16 (logic in
`snake_in_box/benchmarks/generation.py`):

```bash
uv run python snake_in_box/scripts/generate_snakes_for_all_dimensions.py
```

## `reorganize_outputs.py`

Moves stray generated files from the repository root into the unified layout —
`output/reports/`, `output/visualizations/`, `output/graphical_abstracts/`,
`output/test_outputs/`, `output/data/` (logic in
`snake_in_box/utils/outputs.py`). No-op when there is nothing to move; exits 0.

## `run_tests.py`

Runs `python3 -m pytest snake_in_box/tests/ -v` from the repository root and
exits with pytest's return code (0 = pass). For targeted runs prefer pytest
directly, e.g. `uv run --extra dev pytest snake_in_box/tests/test_analysis.py -q`.

## `output/`

Scripts write to the repository-root `output/` (canonical, see
`output/README.md`). Partial result duplicates may exist under
`snake_in_box/scripts/output/` — treat the top-level `output/` as canonical.
