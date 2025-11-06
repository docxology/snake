"""Tests for advanced visualization modules."""

import unittest
import os
from snake_in_box.core.snake_node import SnakeNode
from snake_in_box.utils.visualize_advanced import (
    visualize_snake_1d,
    visualize_snake_2d,
    visualize_snake_3d_advanced,
    visualize_snake_nd,
    visualize_snake_auto,
)


class TestVisualizeAdvanced(unittest.TestCase):
    """Test cases for advanced visualization."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.node_1d = SnakeNode([0], 1)
        self.node_2d = SnakeNode([0, 1], 2)
        self.node_3d = SnakeNode([0, 1, 2, 0], 3)
        self.node_4d = SnakeNode([0, 1, 2, 0, 1], 4)
    
    def test_visualize_snake_1d(self):
        """Test 1D visualization."""
        try:
            fig = visualize_snake_1d(self.node_1d, show_plot=False)
            self.assertIsNotNone(fig)
            if fig:
                import matplotlib.pyplot as plt
                plt.close(fig)
        except ImportError:
            self.skipTest("matplotlib not available")
    
    def test_visualize_snake_1d_wrong_dimension(self):
        """Test 1D visualization with wrong dimension."""
        try:
            with self.assertRaises(ValueError):
                visualize_snake_1d(self.node_2d, show_plot=False)
        except ImportError:
            self.skipTest("matplotlib not available")
    
    def test_visualize_snake_2d(self):
        """Test 2D visualization."""
        try:
            fig = visualize_snake_2d(self.node_2d, show_plot=False)
            self.assertIsNotNone(fig)
            if fig:
                import matplotlib.pyplot as plt
                plt.close(fig)
        except ImportError:
            self.skipTest("matplotlib not available")
    
    def test_visualize_snake_3d_advanced(self):
        """Test 3D visualization."""
        try:
            fig = visualize_snake_3d_advanced(self.node_3d, show_plot=False)
            self.assertIsNotNone(fig)
            if fig:
                import matplotlib.pyplot as plt
                plt.close(fig)
        except ImportError:
            self.skipTest("matplotlib not available")
    
    def test_visualize_snake_nd(self):
        """Test N-dimensional visualization."""
        try:
            fig = visualize_snake_nd(self.node_4d, method='pca', show_plot=False)
            self.assertIsNotNone(fig)
            if fig:
                import matplotlib.pyplot as plt
                plt.close(fig)
        except ImportError:
            self.skipTest("matplotlib not available")
    
    def test_visualize_snake_nd_pairwise(self):
        """Test N-dimensional visualization with pairwise projection."""
        try:
            fig = visualize_snake_nd(
                self.node_4d, method='pairwise', 
                dim1=0, dim2=1, show_plot=False
            )
            self.assertIsNotNone(fig)
            if fig:
                import matplotlib.pyplot as plt
                plt.close(fig)
        except ImportError:
            self.skipTest("matplotlib not available")
    
    def test_visualize_snake_auto(self):
        """Test automatic visualization selection."""
        try:
            fig = visualize_snake_auto(self.node_2d, show_plot=False)
            self.assertIsNotNone(fig)
            if fig:
                import matplotlib.pyplot as plt
                plt.close(fig)
        except ImportError:
            self.skipTest("matplotlib not available")


if __name__ == '__main__':
    unittest.main()

