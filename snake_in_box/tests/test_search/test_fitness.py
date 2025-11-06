"""Tests for fitness evaluators."""

import unittest
from snake_in_box.core.snake_node import SnakeNode
from snake_in_box.search.fitness import (
    SimpleFitnessEvaluator,
    AdvancedFitnessEvaluator,
)


class TestFitness(unittest.TestCase):
    """Test cases for fitness evaluators."""
    
    def test_simple_fitness(self):
        """Test simple fitness evaluator."""
        node = SnakeNode([0, 1], 3)
        evaluator = SimpleFitnessEvaluator(node)
        fitness = evaluator.evaluate()
        
        self.assertEqual(fitness, node.fitness)
        self.assertGreater(fitness, 0)
    
    def test_advanced_fitness_unmarked(self):
        """Test advanced fitness - unmarked count."""
        node = SnakeNode([0, 1], 3)
        evaluator = AdvancedFitnessEvaluator(node)
        
        unmarked = evaluator.count_unmarked_vertices()
        self.assertEqual(unmarked, node.fitness)
    
    def test_advanced_fitness_dead_ends(self):
        """Test advanced fitness - dead ends."""
        node = SnakeNode([0, 1], 3)
        evaluator = AdvancedFitnessEvaluator(node)
        
        dead_ends = evaluator.count_dead_ends()
        self.assertGreaterEqual(dead_ends, 0)
    
    def test_advanced_fitness_unreachable(self):
        """Test advanced fitness - unreachable vertices."""
        node = SnakeNode([0, 1], 3)
        evaluator = AdvancedFitnessEvaluator(node)
        
        unreachable = evaluator.count_unreachable_vertices()
        self.assertGreaterEqual(unreachable, 0)
    
    def test_advanced_fitness_combined(self):
        """Test combined fitness."""
        node = SnakeNode([0, 1], 3)
        evaluator = AdvancedFitnessEvaluator(node)
        
        combined = evaluator.combined_fitness()
        self.assertIsInstance(combined, (int, float))


if __name__ == '__main__':
    unittest.main()

