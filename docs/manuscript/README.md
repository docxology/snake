# Reproduce the Snake-in-the-Box methods paper

The numbered sections describe the Python implementation, a fresh small search,
and checks on the retained path sequences. The earlier publication by Thomas E. Ace
is available separately. [Reference PDF](../reference/ace-2025.pdf) · [Zenodo](https://doi.org/10.5281/zenodo.17538015)

Install Git, uv, Pandoc, pandoc-crossref, and a TeX distribution with XeLaTeX.
Use a separate Docxology Template checkout. Run the following from the
Snake-in-the-Box checkout. [Docxology Template](https://github.com/docxology/template)

```sh
template_dir=/absolute/path/to/template
project_dir="$template_dir/projects/working/snake"
git -C "$template_dir" switch --detach 87704feae0a4490ef7dad9c931d268e8c30273c2
mkdir -p "$template_dir/projects/working"
git worktree add --detach "$project_dir" HEAD
cd "$template_dir"
uv sync --locked --python 3.14 --no-dev
(cd "$project_dir" && MPLBACKEND=Agg "$template_dir/.venv/bin/python" -m docs.reproduce)
uv run --no-sync python scripts/pipeline/stage_03_render.py --project working/snake
uv run --no-sync python scripts/pipeline/stage_04_validate.py --project working/snake
```

Find the PDF, HTML, figure, JSON evidence, and validation report under
`projects/working/snake/output/` in the Template checkout. Reproduction checks the
retained high-dimensional paths and runs fresh searches in dimensions three through five.
