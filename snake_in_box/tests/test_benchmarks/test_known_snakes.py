"""Tests for known snakes database."""

import unittest
from snake_in_box.benchmarks.known_snakes import (
    get_known_record,
    get_known_snake,
    validate_known_snake,
    KNOWN_RECORDS,
)


class TestKnownSnakes(unittest.TestCase):
    """Test cases for known snakes."""
    
    def test_get_known_record(self):
        """Test getting known records."""
        self.assertEqual(get_known_record(3), 4)
        self.assertEqual(get_known_record(7), 50)
        self.assertEqual(get_known_record(13), 2854)
        self.assertIsNone(get_known_record(20))
    
    def test_get_known_snake(self):
        """Test getting known snake sequences."""
        snake_9d = get_known_snake(9)
        self.assertIsNotNone(snake_9d)
        self.assertEqual(len(snake_9d), 190)
        
        snake_13d = get_known_snake(13)
        self.assertIsNotNone(snake_13d)
        self.assertEqual(len(snake_13d), 2854)
    
    def test_get_known_snake_unsupported(self):
        """Test getting snake for unsupported dimension."""
        self.assertIsNone(get_known_snake(8))
        self.assertIsNone(get_known_snake(20))
    
    def test_validate_known_snake(self):
        """Test validating known snakes."""
        is_valid, msg = validate_known_snake(9)
        self.assertTrue(is_valid, msg)
        
        is_valid, msg = validate_known_snake(13)
        self.assertTrue(is_valid, msg)
    
    def test_known_records_completeness(self):
        """Test that known records are complete."""
        for dim in range(3, 14):
            if dim in KNOWN_RECORDS:
                record = get_known_record(dim)
                self.assertIsNotNone(record)
                self.assertGreater(record, 0)


if __name__ == '__main__':
    unittest.main()

