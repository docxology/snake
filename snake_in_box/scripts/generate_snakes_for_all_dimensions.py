#!/usr/bin/env python3
"""Generate snakes for dimensions 1-16 (thin front door).

Generation logic lives in ``snake_in_box.benchmarks.generation``; this script
only delegates. Prints per-dimension progress and exits 0 on success.
"""

from snake_in_box.benchmarks.generation import generate_all

if __name__ == "__main__":
    generate_all()
