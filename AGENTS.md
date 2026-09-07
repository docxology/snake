# AGENTS.md — snake (root)

Subdirs: `docs/` (topic-split documentation), `output/` (analysis artifacts), `snake_in_box/` (Python package; see snake_in_box/AGENTS.md). Files: README.md, requirements.txt, pyproject.toml, snake13.pdf (reference paper PDF).
Gotcha: results appear in BOTH `output/` and `snake_in_box/scripts/output/` — the top-level copy covers dims 11-16, scripts/output only dims 11-14; treat top-level `output/` as canonical.
Verify: `cd snake_in_box && python -m pytest tests/ -q` (run per-package dirs if conflicts).
Policy: see ../../../../AGENTS.md (repo root).
