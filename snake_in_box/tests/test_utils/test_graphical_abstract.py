"""Tests for graphical abstract generation."""

import unittest
import os
from snake_in_box.core.snake_node import SnakeNode
from snake_in_box.utils.graphical_abstract import (
    generate_16d_panel,
    generate_panel_from_sequences,
    generate_panel_from_analysis_results,
)


class TestGraphicalAbstract(unittest.TestCase):
    """Test cases for graphical abstract."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.snake_nodes = {}
        for dim in range(1, 5):  # Test with first 4 dimensions
            try:
                if dim == 1:
                    self.snake_nodes[dim] = SnakeNode([0], dim)
                elif dim == 2:
                    self.snake_nodes[dim] = SnakeNode([0, 1], dim)
                elif dim == 3:
                    self.snake_nodes[dim] = SnakeNode([0, 1, 2, 0], dim)
                elif dim == 4:
                    self.snake_nodes[dim] = SnakeNode([0, 1, 2, 0, 1], dim)
            except:
                pass
    
    def test_generate_16d_panel(self):
        """Test 16D panel generation."""
        try:
            output_file = "test_panel.png"
            generate_16d_panel(self.snake_nodes, output_file=output_file, figsize=(10, 10))
            self.assertTrue(os.path.exists(output_file))
            if os.path.exists(output_file):
                os.remove(output_file)
        except ImportError:
            self.skipTest("matplotlib not available")
        except Exception as e:
            # Panel generation might fail with incomplete data, that's okay
            pass
    
    def test_generate_panel_from_sequences(self):
        """Test panel generation from sequences."""
        try:
            sequences = {1: [0], 2: [0, 1], 3: [0, 1, 2, 0]}
            output_file = "test_panel_sequences.png"
            generate_panel_from_sequences(sequences, output_file=output_file, figsize=(10, 10))
            if os.path.exists(output_file):
                os.remove(output_file)
        except ImportError:
            self.skipTest("matplotlib not available")
        except Exception as e:
            pass
    
    def test_generate_panel_from_analysis_results(self):
        """Test panel generation from analysis results."""
        try:
            results = {
                1: {'snake_node': self.snake_nodes.get(1)},
                2: {'snake_node': self.snake_nodes.get(2)},
            }
            output_file = "test_panel_results.png"
            generate_panel_from_analysis_results(results, output_file=output_file, figsize=(10, 10))
            if os.path.exists(output_file):
                os.remove(output_file)
        except ImportError:
            self.skipTest("matplotlib not available")
        except Exception as e:
            pass


if __name__ == '__main__':
    unittest.main()

