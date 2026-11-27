# Snake-in-the-Box repository

- [Documentation index](docs/index.md) and [canonical manuscript](docs/manuscript/README.md)
- [Python package](snake_in_box/) and its [maintenance guidance](snake_in_box/AGENTS.md)
- [Retained results](output/) and [reference publication](docs/reference/ace-2025.pdf)

Use the repository root for commands. Run `MPLBACKEND=Agg python -m pytest -q`
with the `dev` extra installed. The manuscript recipe uses a separate clean worktree
so its generated evidence and renders stay outside the working copy.
