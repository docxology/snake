# TODO

## Workflowz review — 2026-11-10

Reviewed the bounded evidence packet at base `0de647e4336653bef6b16321638ad415b8b05e53`. Probes below run from the repository root in a fresh environment with the package installed in editable mode and the declared development extras available; use the project's supported Python runtime rather than changing dependency versions blindly.

- [ ] **SNAKE-001 — P1 — Make the documented known-snake validation example importable.** Observable outcome: the public README example either imports successfully and validates a known snake, or is corrected to the actual supported API. Evidence: README.md:55-56 imports `validate_known_snake` from `snake_in_box.benchmarks`, while that package's exports in snake_in_box/benchmarks/__init__.py:1-14 contain no such name. Acceptance probe: `python - <<'PY'
from snake_in_box.benchmarks import validate_known_snake
is_valid, message = validate_known_snake(13)
assert isinstance(is_valid, bool), (is_valid, message)
assert is_valid, message
print('known 13D snake validated')
PY`. Dependencies/constraints: none beyond the package and its declared runtime dependencies; if the function exists elsewhere in unexcerpted source, re-export it deliberately or update README.md:55-56 to the real import path without changing record data.

- [ ] **SNAKE-002 — P2 — Align the advertised Python support contract.** Observable outcome: README, package metadata, and trove classifiers describe one coherent supported Python range, with the development/runtime pin documented as a pin rather than an accidental support claim. Evidence: README.md:24 says Python 3.8+, pyproject.toml:10 requires Python >=3.11, pyproject.toml:21-24 advertises 3.8–3.11, and .python-version:1 selects 3.15. Acceptance probe: `python - <<'PY'
import pathlib, re, tomllib
root = pathlib.Path('.')
project = tomllib.loads((root / 'pyproject.toml').read_text())['project']
readme = (root / 'README.md').read_text()
assert '>=3.11' in project['requires-python']
assert re.search(r'Python 3\.11\+', readme)
assert not any(c.endswith(('3.8', '3.9', '3.10')) for c in project['classifiers'])
print(project['requires-python'])
PY`. Dependencies/constraints: this is a metadata/documentation correction, not a demand to drop working versions or upgrade scientific dependencies; preserve any evidenced deployment/reproducibility constraints and update the probe if maintainers intentionally widen and verify support.

- [ ] **SNAKE-003 — P1 — Surface visualization failures in analysis workflows.** Observable outcome: a requested visualization either produces its file or yields a visible, dimension-specific warning/error; unexpected exceptions are no longer silently discarded while a successful-looking pipeline continues. Evidence: snake_in_box/analysis/workflows.py:92-98 catches every `Exception` around automatic visualization and executes `pass`; the same pattern appears at snake_in_box/analysis/workflows.py:312-318. Acceptance probe: `python - <<'PY'
import contextlib, io, tempfile
import snake_in_box.analysis.workflows as workflows

original = workflows.visualize_snake_auto
def broken(*args, **kwargs):
    raise RuntimeError('review visualization probe')
workflows.visualize_snake_auto = broken
try:
    stream = io.StringIO()
    with tempfile.TemporaryDirectory() as output, contextlib.redirect_stdout(stream), contextlib.redirect_stderr(stream):
        try:
            workflows.run_organized_analysis(output)
        except RuntimeError as exc:
            assert 'review visualization probe' in str(exc)
        else:
            assert 'review visualization probe' in stream.getvalue(), stream.getvalue()
finally:
    workflows.visualize_snake_auto = original
print('visualization failure is observable')
PY`. Dependencies/constraints: choose either fail-fast behavior or an explicit warning policy and apply it consistently to both visible sites; do not convert intentional `ImportError` handling for optional matplotlib into a mandatory visualization dependency. The probe may be adapted to the smallest public workflow entry point if maintainers expose a visualization-only stage, but it must still force the runtime exception and assert observable reporting.

- [ ] **SNAKE-004 — P1 — Prevent known-snake generation from silently substituting another path after invalid data.** Observable outcome: when a known sequence exists but `SnakeNode` rejects it, generation reports the invalid known sequence with its dimension instead of hiding the construction error and continuing as though no known snake were available. Evidence: snake_in_box/benchmarks/generation.py:43-49 catches a bare exception around `SnakeNode(known_seq, dimension)` and discards it; lines 51-56 repeat silent fallback for simple generation. Acceptance probe: `python - <<'PY'
import snake_in_box.benchmarks.generation as generation

original_get = generation.get_known_snake
original_node = generation.SnakeNode
generation.get_known_snake = lambda dimension: [0, 1]
def invalid_known(sequence, dimension):
    raise ValueError('review invalid known snake')
generation.SnakeNode = invalid_known
try:
    try:
        generation.generate_snake(9)
    except ValueError as exc:
        assert 'review invalid known snake' in str(exc)
    else:
        raise AssertionError('invalid known snake was silently accepted or replaced')
finally:
    generation.get_known_snake = original_get
    generation.SnakeNode = original_node
print('invalid known data is reported')
PY`. Dependencies/constraints: use the actual public function name/signature from the full generation.py before implementing; the excerpt proves the branch but not its enclosing function name. Catch `ValueError` specifically where fallback remains intentional, and include the original error context. Do not alter valid known-record contents or remove the separate documented fallback for dimensions without known sequences.

- [ ] **SNAKE-005 — P1 — Make graphical-panel tests fail on real rendering defects.** Observable outcome: panel-generation regressions fail the suite instead of being unconditionally ignored, while an absent optional matplotlib still produces an explicit skip. Evidence: snake_in_box/tests/test_utils/test_graphical_abstract.py:34-44 checks file creation but then catches every non-ImportError exception and passes; lines 42-44 even discard the exception variable without inspection. Acceptance probe: `python -m pytest snake_in_box/tests/test_utils/test_graphical_abstract.py -q` after adding a regression case that monkeypatches the rendering helper to raise `RuntimeError('forced rendering failure')` and asserts that the exception propagates; the normal test must still assert that its output PNG exists and skip only on `ImportError`. Dependencies/constraints: use a temporary directory/pytest `tmp_path` for output cleanup; retain the intentional optional-dependency skip at lines 40-41. Avoid asserting source text—the new test must exercise the rendering call and its failure behavior.

- [ ] **SNAKE-006 — P2 — Preserve diagnostic context when graphical PCA projection falls back.** Observable outcome: an unexpected PCA/projection failure either propagates or emits a visible warning identifying the fallback, rather than silently drawing a potentially misleading two-bit projection. Evidence: snake_in_box/utils/graphical_abstract.py:135-146 catches all exceptions around PCA projection and substitutes the first two dimensions without exposing the error. Acceptance probe: `python - <<'PY'
import warnings
import snake_in_box.utils.graphical_abstract as graphical

original = graphical.pca_projection
def broken(*args, **kwargs):
    raise RuntimeError('review PCA failure')
graphical.pca_projection = broken
try:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        try:
            graphical.generate_16d_panel({2: graphical.SnakeNode([0, 1], 2)}, output_file='/tmp/snake-review-panel.png')
        except RuntimeError as exc:
            assert 'review PCA failure' in str(exc)
        else:
            assert any('review PCA failure' in str(w.message) for w in caught), caught
finally:
    graphical.pca_projection = original
print('PCA fallback is observable')
PY`. Dependencies/constraints: matplotlib is optional, so run this probe with the visualization extra installed and use pytest's `tmp_path` rather than a fixed output path in the committed test. Keep a deliberate first-two-dimensions fallback only if it is a supported visualization policy; warn with exception context and ensure the figure is closed on both paths.
