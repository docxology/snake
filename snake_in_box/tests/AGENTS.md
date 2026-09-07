# AGENTS.md — snake_in_box/tests/

Tests are organized per-package: test_core/, test_search/, test_utils/, test_benchmarks/ (each with test_<module>.py), plus top-level test_analysis.py and generate_test_outputs.py.
Gotcha: run tests per-package directory (`python -m pytest tests/test_core -q`) rather than whole tree in one process if import conflicts appear. generate_test_outputs.py regenerates expected artifacts.
