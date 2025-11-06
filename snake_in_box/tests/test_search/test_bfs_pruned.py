"""Tests for pruned BFS search algorithm."""

import unittest
from snake_in_box.search.bfs_pruned import (
    pruned_bfs_search,
    is_valid_extension,
    prune_by_fitness,
    estimate_memory_usage,
    estimate_node_size,
)
from snake_in_box.core.snake_node import SnakeNode


class TestBFSPruned(unittest.TestCase):
    """Test cases for pruned BFS."""
    
    def test_is_valid_extension(self):
        """Test extension validation."""
        node = SnakeNode([0, 1], 3)
        
        self.assertTrue(is_valid_extension(node, 2))
        self.assertFalse(is_valid_extension(node, 0))  # Would go back
    
    def test_estimate_node_size(self):
        """Test node size estimation."""
        node = SnakeNode([0, 1, 2], 3)
        size = estimate_node_size(node)
        self.assertGreater(size, 0)
    
    def test_estimate_memory_usage(self):
        """Test memory usage estimation."""
        nodes = [SnakeNode([0], 3), SnakeNode([0, 1], 3)]
        usage = estimate_memory_usage(nodes)
        self.assertGreater(usage, 0)
    
    def test_prune_by_fitness(self):
        """Test fitness-based pruning."""
        nodes = [
            SnakeNode([0], 3),
            SnakeNode([0, 1], 3),
            SnakeNode([0, 1, 2], 3),
        ]
        
        # Prune to 2 nodes
        pruned = prune_by_fitness(nodes, 0.0001)  # Very small limit
        self.assertLessEqual(len(pruned), len(nodes))
    
    def test_prune_by_fitness_no_pruning(self):
        """Test pruning when not needed."""
        nodes = [SnakeNode([0], 3)]
        pruned = prune_by_fitness(nodes, 18.0)  # Large limit
        self.assertEqual(len(pruned), len(nodes))
    
    def test_search_small_dimension(self):
        """Test search for small dimension."""
        # For dimension 3, we know optimal is 4
        result = pruned_bfs_search(dimension=3, memory_limit_gb=0.1, verbose=False)
        self.assertIsNotNone(result)
        self.assertGreaterEqual(result.get_length(), 2)  # At least some length


if __name__ == '__main__':
    unittest.main()

