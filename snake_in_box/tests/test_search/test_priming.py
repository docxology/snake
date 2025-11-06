"""Tests for priming strategy."""

import unittest
from snake_in_box.search.priming import (
    detect_dimension,
    pruned_bfs_search_from_seed,
)
from snake_in_box.core.snake_node import SnakeNode


class TestPriming(unittest.TestCase):
    """Test cases for priming."""
    
    def test_detect_dimension(self):
        """Test dimension detection."""
        self.assertEqual(detect_dimension([]), 1)
        self.assertEqual(detect_dimension([0]), 1)
        self.assertEqual(detect_dimension([0, 1, 2]), 3)
        self.assertEqual(detect_dimension([0, 1, 0, 2]), 3)
    
    def test_pruned_bfs_search_from_seed(self):
        """Test BFS from seed node."""
        seed = SnakeNode([0, 1], 3)
        result = pruned_bfs_search_from_seed(
            seed,
            dimension=3,
            memory_limit_gb=0.1,
            verbose=False
        )
        
        self.assertIsNotNone(result)
        self.assertGreaterEqual(result.get_length(), seed.get_length())
    
    def test_pruned_bfs_search_from_seed_dimension_mismatch(self):
        """Test BFS from seed with dimension mismatch."""
        seed = SnakeNode([0, 1], 3)
        
        with self.assertRaises(ValueError):
            pruned_bfs_search_from_seed(seed, dimension=4, verbose=False)


if __name__ == '__main__':
    unittest.main()

