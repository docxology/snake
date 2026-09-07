# AGENTS.md — snake_in_box/scripts/

Thin orchestrator front doors over the `snake_in_box` package.

## Contract

- Scripts contain ONLY: argument parsing, path/output setup, logging, and a
  single delegated call into `snake_in_box/` library modules.
- Business, search, plot, report, and analysis logic lives in `snake_in_box/`
  (`analysis/workflows.py`, `search/crack.py`, `benchmarks/generation.py`,
  `utils/outputs.py`) — importable and testable. Never import one script from
  another script; promote shared logic into the owning subpackage and have
  both call it.
- Scripts import the installed package (pyproject
  `[tool.setuptools.packages.find]` includes `snake_in_box*`). Run from the
  repo root with `uv run [--extra dev] python snake_in_box/scripts/<script>.py`.
  No `sys.path.insert` bootstrap is used or allowed.
- When adding a script: keep it thin per this contract, put the logic in the
  owning subpackage, and update this inventory plus `README.md`.

## Inventory

| Script | Delegates to | Purpose |
|--------|--------------|---------|
| `run_analysis.py` | `snake_in_box.analysis.workflows` (`run_basic_analysis`, `run_full_analysis`, `run_organized_analysis`) | Analysis pipeline for dims 1-16; `--mode basic\|full\|organized` (default organized), `--output-base` |
| `crack_high_dimensions.py` | `snake_in_box.search.crack.run_all_dimensions` | Serial validated record searches for dims 11-16; resumable via `output/crack_results/` |
| `crack_high_dimensions_parallel.py` | `snake_in_box.search.crack` (`search_dimension`, `setup_logging`, config constants) | Same searches with one process per dimension |
| `generate_snakes_for_all_dimensions.py` | `snake_in_box.benchmarks.generation.generate_all` | Baseline snakes for dims 1-16 |
| `reorganize_outputs.py` | `snake_in_box.utils.outputs.reorganize_outputs` | Moves stray artifacts into `output/` subdirectories |
| `run_tests.py` | `pytest snake_in_box/tests/` | Test-suite runner |

Gotcha: scripts write to the repository-root `output/` (canonical). Partial
result duplicates may exist under `scripts/output/` — see its AGENTS.md; treat
the top-level `output/` as canonical.
