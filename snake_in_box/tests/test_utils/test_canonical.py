"""Tests for canonical form utilities."""

import unittest
from snake_in_box.utils.canonical import (
    is_canonical,
    get_legal_next_dimensions,
)


class TestCanonical(unittest.TestCase):
    """Test cases for canonical form."""
    
    def test_is_canonical_valid(self):
        """Test valid canonical sequences."""
        self.assertTrue(is_canonical([]))
        self.assertTrue(is_canonical([0]))
        self.assertTrue(is_canonical([0, 1, 2, 0, 1]))
        self.assertTrue(is_canonical([0, 1, 0, 2, 1]))
    
    def test_is_canonical_invalid_first_digit(self):
        """Test invalid - doesn't start with 0."""
        self.assertFalse(is_canonical([1, 0, 2]))
        self.assertFalse(is_canonical([2, 1, 0]))
    
    def test_is_canonical_invalid_jump(self):
        """Test invalid - jumps too far."""
        self.assertFalse(is_canonical([0, 1, 3]))  # 3 > max(0,1) + 1 = 2
        self.assertFalse(is_canonical([0, 2]))  # 2 > max(0) + 1 = 1
    
    def test_get_legal_next_dimensions_empty(self):
        """Test legal dimensions for empty sequence."""
        legal = get_legal_next_dimensions([])
        self.assertEqual(legal, [0])
    
    def test_get_legal_next_dimensions_single(self):
        """Test legal dimensions for single transition."""
        legal = get_legal_next_dimensions([0])
        self.assertEqual(set(legal), {0, 1})
    
    def test_get_legal_next_dimensions_multiple(self):
        """Test legal dimensions for multiple transitions."""
        legal = get_legal_next_dimensions([0, 1, 2])
        self.assertEqual(set(legal), {0, 1, 2, 3})
    
    def test_get_legal_next_dimensions_repeated(self):
        """Test legal dimensions with repeated transitions."""
        legal = get_legal_next_dimensions([0, 1, 0, 2])
        self.assertEqual(set(legal), {0, 1, 2, 3})


if __name__ == '__main__':
    unittest.main()

