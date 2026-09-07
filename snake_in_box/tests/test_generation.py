"""Tests for baseline snake generation (snake_in_box.benchmarks.generation)."""

import unittest

from snake_in_box.benchmarks.generation import (
    generate_all,
    generate_simple_snake,
    get_snake_for_dimension,
)
from snake_in_box.core.snake_node import SnakeNode


class TestGeneration(unittest.TestCase):
    """Test cases for pattern-based snake generation."""

    def test_generate_simple_snake_small_dimensions(self):
        """Dims 1-6 produce SnakeNodes with one edge per transition."""
        expected_lengths = {1: 1, 2: 3, 3: 4, 4: 7, 5: 12, 6: 21}
        for dim, expected in expected_lengths.items():
            node = generate_simple_snake(dim)
            self.assertIsInstance(node, SnakeNode)
            self.assertEqual(node.dimension, dim)
            self.assertEqual(node.get_length(), expected)

    def test_generate_simple_snake_rejects_unpatterned_dimension(self):
        """Dimensions beyond the pattern table return None."""
        self.assertIsNone(generate_simple_snake(7))
        self.assertIsNone(generate_simple_snake(16))

    def test_get_snake_for_dimension_known_dimensions(self):
        """Dims with database entries (9-13) resolve to known snakes."""
        known_lengths = {9: 190, 10: 373, 11: 732, 12: 1439, 13: 2854}
        for dim, expected in known_lengths.items():
            node = get_snake_for_dimension(dim)
            self.assertIsInstance(node, SnakeNode)
            self.assertEqual(node.dimension, dim)
            self.assertEqual(node.get_length(), expected)

    def test_get_snake_for_dimension_constructed_dimensions(self):
        """Every dimension 1-13 yields a snake (generated or known)."""
        for dim in range(1, 14):
            node = get_snake_for_dimension(dim)
            self.assertIsInstance(node, SnakeNode, f"dim {dim} returned None")
            self.assertGreater(node.get_length(), 0)

    def test_get_snake_for_dimension_beyond_records(self):
        """Dims without records or patterns return None."""
        self.assertIsNone(get_snake_for_dimension(14))
        self.assertIsNone(get_snake_for_dimension(16))

    def test_generate_all_covers_all_producible_dimensions(self):
        """generate_all returns nodes for exactly dims 1-13."""
        nodes = generate_all()
        self.assertEqual(sorted(nodes.keys()), list(range(1, 14)))


if __name__ == "__main__":
    unittest.main()
