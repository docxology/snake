#!/usr/bin/env python3
"""Run the snake_in_box test suite.

Delegates to ``python3 -m pytest snake_in_box/tests/`` from the repository
root. Prints verbose test output and exits with pytest's return code
(0 = all tests passed, 1 = failures, 2 = interrupted, 4 = usage error).

Usage (from repository root):
    python3 snake_in_box/scripts/run_tests.py
"""

import subprocess
import sys
import os


def main():
    """Run all tests."""
    result = subprocess.run(
        ["python3", "-m", "pytest", "snake_in_box/tests/", "-v"],
        cwd=os.path.join(os.path.dirname(__file__), '..', '..')
    )
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())
