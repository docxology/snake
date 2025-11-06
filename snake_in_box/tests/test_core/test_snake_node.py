"""Tests for SnakeNode class."""

import unittest
from snake_in_box.core.snake_node import SnakeNode


class TestSnakeNode(unittest.TestCase):
    """Test cases for SnakeNode."""
    
    def test_init_empty(self):
        """Test initialization with empty snake."""
        node = SnakeNode([], 3)
        self.assertEqual(node.dimension, 3)
        self.assertEqual(node.get_length(), 0)
        self.assertEqual(node.get_current_vertex(), 0)
    
    def test_init_with_transitions(self):
        """Test initialization with transition sequence."""
        node = SnakeNode([0, 1, 2], 3)
        self.assertEqual(node.get_length(), 3)
        self.assertEqual(node.get_current_vertex(), 7)  # 0 -> 1 -> 3 -> 7
    
    def test_init_invalid_dimension(self):
        """Test initialization with invalid dimension."""
        with self.assertRaises(ValueError):
            SnakeNode([], 0)
    
    def test_init_invalid_transition(self):
        """Test initialization with invalid transition."""
        with self.assertRaises(ValueError):
            SnakeNode([0, 5], 3)  # 5 >= 3
    
    def test_get_current_vertex(self):
        """Test getting current vertex."""
        node = SnakeNode([0, 1, 2, 0], 3)
        self.assertEqual(node.get_current_vertex(), 6)
    
    def test_can_extend(self):
        """Test checking if extension is valid."""
        node = SnakeNode([0, 1], 3)
        
        # Should be able to extend in dimension 2
        self.assertTrue(node.can_extend(2))
        
        # Should not be able to extend back to vertex 0
        self.assertFalse(node.can_extend(0))
    
    def test_create_child(self):
        """Test creating child node."""
        node = SnakeNode([0, 1], 3)
        child = node.create_child(2)
        
        self.assertEqual(child.get_length(), 3)
        self.assertEqual(child.transition_sequence, [0, 1, 2])
        self.assertEqual(child.get_current_vertex(), 7)
    
    def test_create_child_invalid(self):
        """Test creating invalid child."""
        node = SnakeNode([0, 1], 3)
        
        # Try to extend back to already visited vertex
        with self.assertRaises(ValueError):
            node.create_child(0)
    
    def test_fitness(self):
        """Test fitness calculation."""
        node = SnakeNode([], 3)
        # Empty snake: all 8 vertices available initially
        # But origin and its neighbors are marked, so fitness < 8
        self.assertGreater(node.fitness, 0)
        self.assertLessEqual(node.fitness, 8)
    
    def test_bitmap_initialization(self):
        """Test bitmap is properly initialized."""
        node = SnakeNode([0, 1], 3)
        
        # Origin should be marked
        self.assertTrue(node._is_marked(0))
        
        # Vertex 1 should be marked
        self.assertTrue(node._is_marked(1))
        
        # Some vertices should be unmarked
        self.assertGreater(node.fitness, 0)
    
    def test_repr(self):
        """Test string representation."""
        node = SnakeNode([0, 1, 2], 3)
        repr_str = repr(node)
        self.assertIn("SnakeNode", repr_str)
        self.assertIn("dim=3", repr_str)
        self.assertIn("len=3", repr_str)


if __name__ == '__main__':
    unittest.main()

