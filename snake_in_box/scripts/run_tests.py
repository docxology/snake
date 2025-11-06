#!/usr/bin/env python3
"""Run test suite."""

import sys
import subprocess
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

def main():
    """Run all tests."""
    result = subprocess.run(
        ["python3", "-m", "pytest", "snake_in_box/tests/", "-v"],
        cwd=os.path.join(os.path.dirname(__file__), '..', '..')
    )
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())

