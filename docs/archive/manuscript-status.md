# Manuscript status — snake (Snake-in-the-Box)

**Repo type:** Tool / algorithm implementation with an embedded paper text.
Python implementation of the N-dimensional snake-in-the-box search
(`pyproject.toml`: name `snake-in-box`, "N-dimensional snake-in-the-box
algorithm implementation"), based on Ace (2025),
doi:10.5281/zenodo.17538015.

**Evidence checked:** repo root listing (`README.md`, `pyproject.toml`,
`requirements.txt`, `snake_in_box/` package with `tests/`, `output/`,
`snake13.pdf`), `docs/` tree (algorithm/, api/, architecture/, diagrams/,
guides/, theory/). The paper text for the underlying result already exists in
this repo as `docs/snake_paper.md` (published at the DOI above) and as
`snake13.pdf`; no `manuscript/` or `docs/manuscript/` directory existed
before this file.

**Why no publication-target manuscript applies today:** the publication that
 motivates the repo is already written and DOI-published
(`docs/snake_paper.md`, doi:10.5281/zenodo.17538015); the repo itself is the
algorithm implementation, and its deliverables are code, search results, and
visualizations under `output/`.

**What would trigger creating one:** a methods paper on the implementation
itself (heuristically-pruned BFS engineering, performance, and reproduction
of the 732/1439/2854 lower bounds), or a new-results paper. At that point,
add a full `manuscript/` tree at the repo top level (config.yaml, section
files 00–99, references.bib) following the docxology/template standard.
