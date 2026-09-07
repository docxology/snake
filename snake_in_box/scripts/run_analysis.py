#!/usr/bin/env python3
"""Run the snake-in-the-box analysis pipeline for dimensions 1-16.

Single front door for all analysis workflows. All pipeline logic lives in
``snake_in_box.analysis.workflows``; this script only parses arguments and
delegates one call.

Modes:
    organized  Organized outputs, feasibility report, comprehensive data
               exports (default; formerly run_analysis_with_output_organization.py)
    full       Adds exponential analysis, performance plots and computation-
               time tracking (formerly run_full_analysis.py)
    basic      Reports, graphical abstract, visualizations, simple JSON dump
               (formerly the bare run_analysis.py workflow)

Exit status: 0 on success, non-zero on argument or pipeline error.

Usage (from repository root, requires the installed package):
    uv run --extra dev python snake_in_box/scripts/run_analysis.py --mode organized
"""

import argparse
import sys

from snake_in_box.analysis.workflows import (
    run_basic_analysis,
    run_full_analysis,
    run_organized_analysis,
)


def main():
    """Parse arguments and delegate to the selected analysis workflow."""
    parser = argparse.ArgumentParser(
        description="Run snake-in-the-box analysis for dimensions 1-16."
    )
    parser.add_argument(
        "--mode",
        choices=["basic", "full", "organized"],
        default="organized",
        help="Analysis workflow to run (default: organized)"
    )
    parser.add_argument(
        "--output-base",
        default="output",
        help="Base directory for generated outputs (default: output)"
    )
    args = parser.parse_args()

    workflows = {
        "basic": run_basic_analysis,
        "full": run_full_analysis,
        "organized": run_organized_analysis,
    }
    workflows[args.mode](args.output_base)
    return 0


if __name__ == "__main__":
    sys.exit(main())
