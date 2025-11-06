#!/usr/bin/env python3
"""Generate snakes for all dimensions 1-16."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from snake_in_box.core.snake_node import SnakeNode
from snake_in_box.benchmarks.known_snakes import get_known_snake, KNOWN_RECORDS


def generate_simple_snake(dimension: int) -> SnakeNode:
    """Generate snake for small dimensions."""
    if dimension == 1:
        # 1D: just flip bit 0
        return SnakeNode([0], 1)
    elif dimension == 2:
        # 2D: 0->1->3->2
        return SnakeNode([0, 1, 0], 2)
    elif dimension == 3:
        # 3D: known optimal 0120
        return SnakeNode([0, 1, 2, 0], 3)
    elif dimension == 4:
        # 4D: simple pattern
        return SnakeNode([0, 1, 2, 3, 0, 1, 2], 4)
    elif dimension == 5:
        # 5D: extend pattern
        transitions = [0, 1, 2, 3, 4, 0, 1, 2, 3, 0, 1, 2]
        return SnakeNode(transitions, 5)
    elif dimension == 6:
        # 6D: extend further
        transitions = [0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 0, 1, 2, 3, 0, 1, 2, 0, 1, 0]
        return SnakeNode(transitions, 6)
    else:
        return None


def get_snake_for_dimension(dimension: int) -> SnakeNode:
    """Get snake for dimension."""
    # Try known snake first
    if dimension >= 9:
        known_seq = get_known_snake(dimension)
        if known_seq:
            try:
                return SnakeNode(known_seq, dimension)
            except:
                pass
    
    # Try simple generation for small dimensions
    if dimension <= 6:
        try:
            return generate_simple_snake(dimension)
        except:
            pass
    
    # For dimensions 7-8, try to create from known records
    # Use a pattern based on lower dimensions
    if dimension == 7:
        # Create a reasonable snake for 7D
        base = [0, 1, 2, 3, 4, 5, 6]
        # Extend with pattern
        transitions = base + [0, 1, 2, 3, 4, 5] + [0, 1, 2, 3, 4] + [0, 1, 2, 3] + [0, 1, 2] + [0, 1] + [0]
        # Limit to reasonable length
        transitions = transitions[:50]
        try:
            return SnakeNode(transitions, 7)
        except:
            pass
    
    if dimension == 8:
        base = [0, 1, 2, 3, 4, 5, 6, 7]
        transitions = base + [0, 1, 2, 3, 4, 5, 6] + [0, 1, 2, 3, 4, 5] + [0, 1, 2, 3, 4] + [0, 1, 2, 3] + [0, 1, 2] + [0, 1] + [0]
        transitions = transitions[:97]
        try:
            return SnakeNode(transitions, 8)
        except:
            pass
    
    return None


def main():
    """Generate snakes for all dimensions."""
    print("Generating snakes for dimensions 1-16...")
    
    snake_nodes = {}
    
    for dim in range(1, 17):
        print(f"Dimension {dim}...", end=" ")
        node = get_snake_for_dimension(dim)
        if node:
            snake_nodes[dim] = node
            print(f"✓ Length: {node.get_length()}")
        else:
            print("✗ Failed")
    
    print(f"\nGenerated {len(snake_nodes)} snakes")
    return snake_nodes


if __name__ == "__main__":
    main()

