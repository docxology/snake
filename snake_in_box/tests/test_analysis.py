"""Tests for analysis modules."""

import unittest
from snake_in_box.analysis.analyze_dimensions import (
    analyze_single_dimension,
    analyze_dimensions,
    generate_statistics,
)
from snake_in_box.analysis.reporting import (
    generate_analysis_report,
    generate_validation_report,
    generate_performance_report,
)


class TestAnalysis(unittest.TestCase):
    """Test cases for analysis modules."""
    
    def test_analyze_single_dimension_known(self):
        """Test analyzing single dimension with known snake."""
        result = analyze_single_dimension(3, use_known=True, memory_limit_gb=0.1, verbose=False)
        
        self.assertEqual(result['dimension'], 3)
        self.assertIn('length', result)
        self.assertIn('is_valid', result)
        self.assertIn('method', result)
        self.assertIn('search_time', result)
    
    def test_analyze_single_dimension_search(self):
        """Test analyzing single dimension with search."""
        result = analyze_single_dimension(3, use_known=False, memory_limit_gb=0.1, verbose=False)
        
        self.assertEqual(result['dimension'], 3)
        self.assertIn('length', result)
        self.assertIn('method', result)
    
    def test_analyze_dimensions(self):
        """Test analyzing multiple dimensions."""
        results = analyze_dimensions([1, 2, 3], use_known=True, memory_limit_gb=0.1, verbose=False)
        
        self.assertEqual(len(results), 3)
        self.assertIn(1, results)
        self.assertIn(2, results)
        self.assertIn(3, results)
    
    def test_generate_statistics(self):
        """Test statistics generation."""
        results = {
            1: {
                'length': 1, 
                'is_valid': True, 
                'method': 'known', 
                'search_time': 0.1,
                'matches_known': False,
            },
            2: {
                'length': 2, 
                'is_valid': True, 
                'method': 'known', 
                'search_time': 0.2,
                'matches_known': False,
            },
        }
        
        stats = generate_statistics(results)
        
        self.assertEqual(stats['total_dimensions'], 2)
        self.assertEqual(stats['valid_snakes'], 2)
        self.assertEqual(stats['total_length'], 3)
        self.assertIn('average_time', stats)
    
    def test_generate_analysis_report(self):
        """Test analysis report generation."""
        results = {
            1: {
                'dimension': 1,
                'length': 1,
                'is_valid': True,
                'method': 'known',
                'search_time': 0.1,
                'known_record': None,
                'matches_known': False,
                'validation_message': 'Valid',
            },
        }
        
        try:
            content = generate_analysis_report(results, "test_report.md", format="markdown")
            self.assertIsInstance(content, str)
            self.assertIn("Analysis Report", content)
            
            import os
            if os.path.exists("test_report.md"):
                os.remove("test_report.md")
        except Exception as e:
            self.fail(f"Report generation failed: {e}")
    
    def test_generate_validation_report(self):
        """Test validation report generation."""
        results = {
            1: {
                'dimension': 1,
                'length': 1,
                'is_valid': True,
                'validation_message': 'Valid',
            },
        }
        
        try:
            content = generate_validation_report(results, "test_validation.md")
            self.assertIsInstance(content, str)
            self.assertIn("Validation Report", content)
            
            import os
            if os.path.exists("test_validation.md"):
                os.remove("test_validation.md")
        except Exception as e:
            self.fail(f"Validation report generation failed: {e}")
    
    def test_generate_performance_report(self):
        """Test performance report generation."""
        results = {
            1: {
                'dimension': 1,
                'length': 1,
                'method': 'known',
                'search_time': 0.1,
                'is_valid': True,
                'matches_known': False,
            },
        }
        
        try:
            content = generate_performance_report(results, "test_performance.md")
            self.assertIsInstance(content, str)
            self.assertIn("Performance Report", content)
            
            import os
            if os.path.exists("test_performance.md"):
                os.remove("test_performance.md")
        except Exception as e:
            self.fail(f"Performance report generation failed: {e}")


if __name__ == '__main__':
    unittest.main()

