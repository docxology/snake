"""Tests for transition/vertex conversion functions."""

import unittest
from snake_in_box.core.transitions import (
    vertex_to_transition,
    transition_to_vertex,
    compute_current_vertex,
    parse_hex_transition_string,
)


class TestTransitions(unittest.TestCase):
    """Test cases for transition functions."""
    
    def test_vertex_to_transition(self):
        """Test vertex to transition conversion."""
        # Example from paper: 000, 001, 011, 111, 110 -> 0, 1, 2, 0
        vertices = [0, 1, 3, 7, 6]
        transitions = vertex_to_transition(vertices)
        self.assertEqual(transitions, [0, 1, 2, 0])
    
    def test_vertex_to_transition_empty(self):
        """Test with empty sequence."""
        self.assertEqual(vertex_to_transition([]), [])
        self.assertEqual(vertex_to_transition([0]), [])
    
    def test_vertex_to_transition_invalid(self):
        """Test with invalid vertex sequences."""
        # Identical consecutive vertices
        with self.assertRaises(ValueError):
            vertex_to_transition([0, 0, 1])
        
        # Multiple bit differences
        with self.assertRaises(ValueError):
            vertex_to_transition([0, 3])  # 0b000 vs 0b011
    
    def test_transition_to_vertex(self):
        """Test transition to vertex conversion."""
        transitions = [0, 1, 2, 0]
        vertices = transition_to_vertex(transitions, 3)
        self.assertEqual(vertices, [0, 1, 3, 7, 6])
    
    def test_transition_to_vertex_start(self):
        """Test with custom start vertex."""
        transitions = [0, 1]
        vertices = transition_to_vertex(transitions, 3, start_vertex=0)
        self.assertEqual(vertices, [0, 1, 3])
    
    def test_transition_to_vertex_invalid(self):
        """Test with invalid transitions."""
        with self.assertRaises(ValueError):
            transition_to_vertex([0, 5], 3)  # 5 >= 3
    
    def test_compute_current_vertex(self):
        """Test computing current vertex."""
        transitions = [0, 1, 2, 0]
        vertex = compute_current_vertex(transitions)
        self.assertEqual(vertex, 6)
    
    def test_compute_current_vertex_empty(self):
        """Test with empty sequence."""
        self.assertEqual(compute_current_vertex([]), 0)
    
    def test_round_trip(self):
        """Test round-trip conversion."""
        original_transitions = [0, 1, 2, 0, 1, 2, 0]
        vertices = transition_to_vertex(original_transitions, 3)
        converted_back = vertex_to_transition(vertices)
        self.assertEqual(converted_back, original_transitions)
    
    def test_parse_hex_string(self):
        """Test parsing hex string."""
        hex_str = "0120"
        transitions = parse_hex_transition_string(hex_str)
        self.assertEqual(transitions, [0, 1, 2, 0])
    
    def test_parse_hex_string_with_commas(self):
        """Test parsing hex string with commas."""
        hex_str = "0,1,2,0"
        transitions = parse_hex_transition_string(hex_str)
        self.assertEqual(transitions, [0, 1, 2, 0])
    
    def test_parse_hex_string_hex_digits(self):
        """Test parsing hex digits a-f."""
        hex_str = "012a"
        transitions = parse_hex_transition_string(hex_str)
        self.assertEqual(transitions, [0, 1, 2, 10])
    
    def test_parse_hex_string_whitespace(self):
        """Test parsing with whitespace."""
        hex_str = "0 1 2 0"
        transitions = parse_hex_transition_string(hex_str)
        self.assertEqual(transitions, [0, 1, 2, 0])


if __name__ == '__main__':
    unittest.main()

