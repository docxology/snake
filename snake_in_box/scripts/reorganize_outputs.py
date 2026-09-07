#!/usr/bin/env python3
"""Reorganize all outputs into the unified output/ directory structure.

Moves stray generated files from the repository root into organized
subdirectories:
- output/reports/
- output/visualizations/
- output/graphical_abstracts/
- output/test_outputs/
- output/data/

The move logic lives in ``snake_in_box.utils.outputs``; this script only
computes the repository root and delegates. Exits 0 on success.

Usage (from repository root):
    uv run python snake_in_box/scripts/reorganize_outputs.py
"""

import os

from snake_in_box.utils.outputs import reorganize_outputs

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    reorganize_outputs(base_dir)
