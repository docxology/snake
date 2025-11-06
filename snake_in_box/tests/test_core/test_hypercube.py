"""Tests for HypercubeBitmap class."""

import unittest
from snake_in_box.core.hypercube import HypercubeBitmap


class TestHypercubeBitmap(unittest.TestCase):
    """Test cases for HypercubeBitmap."""
    
    def test_init(self):
        """Test bitmap initialization."""
        bitmap = HypercubeBitmap(3)
        self.assertEqual(bitmap.dimension, 3)
        self.assertEqual(bitmap.num_vertices, 8)
        self.assertEqual(bitmap.num_words, 1)
    
    def test_init_invalid_dimension(self):
        """Test initialization with invalid dimension."""
        with self.assertRaises(ValueError):
            HypercubeBitmap(0)
        with self.assertRaises(ValueError):
            HypercubeBitmap(-1)
    
    def test_set_get_bit(self):
        """Test setting and getting bits."""
        bitmap = HypercubeBitmap(3)
        
        # Initially all bits should be unmarked
        self.assertFalse(bitmap.get_bit(0))
        self.assertFalse(bitmap.get_bit(7))
        
        # Mark some vertices
        bitmap.set_bit(0)
        bitmap.set_bit(5)
        
        self.assertTrue(bitmap.get_bit(0))
        self.assertTrue(bitmap.get_bit(5))
        self.assertFalse(bitmap.get_bit(1))
        self.assertFalse(bitmap.get_bit(7))
    
    def test_set_bit_out_of_range(self):
        """Test setting bit out of range."""
        bitmap = HypercubeBitmap(3)
        with self.assertRaises(IndexError):
            bitmap.set_bit(8)
        with self.assertRaises(IndexError):
            bitmap.set_bit(-1)
    
    def test_clear_bit(self):
        """Test clearing bits."""
        bitmap = HypercubeBitmap(3)
        bitmap.set_bit(0)
        self.assertTrue(bitmap.get_bit(0))
        
        bitmap.clear_bit(0)
        self.assertFalse(bitmap.get_bit(0))
    
    def test_count_unmarked(self):
        """Test counting unmarked vertices."""
        bitmap = HypercubeBitmap(3)
        self.assertEqual(bitmap.count_unmarked(), 8)
        
        bitmap.set_bit(0)
        self.assertEqual(bitmap.count_unmarked(), 7)
        
        bitmap.set_bit(1)
        bitmap.set_bit(2)
        self.assertEqual(bitmap.count_unmarked(), 5)
    
    def test_count_unmarked_fast(self):
        """Test fast unmarked count."""
        bitmap = HypercubeBitmap(3)
        self.assertEqual(bitmap.count_unmarked_fast(), 8)
        
        bitmap.set_bit(0)
        self.assertEqual(bitmap.count_unmarked_fast(), 7)
    
    def test_clear_all(self):
        """Test clearing all bits."""
        bitmap = HypercubeBitmap(3)
        bitmap.set_bit(0)
        bitmap.set_bit(1)
        bitmap.set_bit(2)
        
        bitmap.clear_all()
        self.assertEqual(bitmap.count_unmarked(), 8)
    
    def test_copy(self):
        """Test copying bitmap."""
        bitmap = HypercubeBitmap(3)
        bitmap.set_bit(0)
        bitmap.set_bit(5)
        
        copy = bitmap.copy()
        self.assertEqual(copy.count_unmarked(), bitmap.count_unmarked())
        self.assertTrue(copy.get_bit(0))
        self.assertTrue(copy.get_bit(5))
        
        # Modify copy, original should be unchanged
        copy.set_bit(1)
        self.assertFalse(bitmap.get_bit(1))
        self.assertTrue(copy.get_bit(1))
    
    def test_large_dimension(self):
        """Test with larger dimension."""
        bitmap = HypercubeBitmap(10)
        self.assertEqual(bitmap.num_vertices, 1024)
        self.assertEqual(bitmap.count_unmarked(), 1024)


if __name__ == '__main__':
    unittest.main()

