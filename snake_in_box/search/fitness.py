"""Fitness evaluation functions."""

from typing import Dict, Set
from ..core.snake_node import SnakeNode
from ..core.transitions import compute_current_vertex


class SimpleFitnessEvaluator:
    """Simple fitness evaluator using unmarked vertex count.
    
    This is the fitness measure used in Ace (2025) that achieved
    record-breaking results. Despite its simplicity, it was sufficient
    for the results presented in the paper.
    """
    
    def __init__(self, node: SnakeNode):
        """Initialize evaluator for a node.
        
        Parameters
        ----------
        node : SnakeNode
            Node to evaluate
        """
        self.node = node
    
    def evaluate(self) -> int:
        """Evaluate fitness as count of unmarked vertices.
        
        Returns
        -------
        int
            Number of unmarked vertices
        """
        return self.node.fitness


class AdvancedFitnessEvaluator:
    """Advanced fitness evaluator with multiple measures.
    
    Provides alternative fitness measures beyond simple unmarked count,
    including dead ends, unreachable vertices, and combined metrics.
    """
    
    def __init__(self, node: SnakeNode):
        """Initialize evaluator for a node.
        
        Parameters
        ----------
        node : SnakeNode
            Node to evaluate
        """
        self.node = node
        self.bitmap = node.vertices_bitmap
        self.dimension = node.dimension
    
    def count_unmarked_vertices(self) -> int:
        """Count unmarked vertices (original simple fitness).
        
        Returns
        -------
        int
            Number of unmarked vertices
        """
        return self.node.fitness
    
    def count_unreachable_vertices(self) -> int:
        """Count vertices unreachable from current position.
        
        Uses flood fill (BFS) to find all reachable unmarked vertices
        from the current snake position.
        
        Returns
        -------
        int
            Number of unreachable unmarked vertices
        """
        current_vertex = compute_current_vertex(self.node.transition_sequence)
        reachable = self._flood_fill_reachable(current_vertex)
        total_unmarked = self.count_unmarked_vertices()
        return total_unmarked - len(reachable)
    
    def count_dead_ends(self) -> int:
        """Count unmarked vertices with only one unmarked neighbor.
        
        Dead ends limit future growth potential as they can only be
        entered from one direction.
        
        Returns
        -------
        int
            Number of dead end vertices
        """
        dead_ends = 0
        
        for vertex in range(1 << self.dimension):
            if self.node._is_marked(vertex):
                continue
            
            # Count unmarked neighbors
            unmarked_neighbors = 0
            for dim in range(self.dimension):
                neighbor = vertex ^ (1 << dim)
                if not self.node._is_marked(neighbor):
                    unmarked_neighbors += 1
            
            if unmarked_neighbors == 1:
                dead_ends += 1
        
        return dead_ends
    
    def combined_fitness(
        self,
        weights: Dict[str, float] = None
    ) -> float:
        """Weighted combination of multiple fitness measures.
        
        Parameters
        ----------
        weights : Dict[str, float], optional
            Weights for each measure. Default: {'unmarked': 1.0, 'dead_ends': -0.5}
            Negative weights penalize undesirable features.
        
        Returns
        -------
        float
            Combined fitness score
        """
        if weights is None:
            weights = {'unmarked': 1.0, 'dead_ends': -0.5}
        
        fitness = 0.0
        fitness += weights.get('unmarked', 0.0) * self.count_unmarked_vertices()
        fitness += weights.get('dead_ends', 0.0) * self.count_dead_ends()
        fitness += weights.get('unreachable', 0.0) * self.count_unreachable_vertices()
        
        return fitness
    
    def _flood_fill_reachable(self, start_vertex: int) -> Set[int]:
        """Find all reachable unmarked vertices from start using BFS.
        
        Parameters
        ----------
        start_vertex : int
            Starting vertex for flood fill
        
        Returns
        -------
        Set[int]
            Set of reachable unmarked vertex indices
        """
        visited: Set[int] = set()
        queue = [start_vertex]
        
        while queue:
            vertex = queue.pop(0)
            
            if vertex in visited or self.node._is_marked(vertex):
                continue
            
            visited.add(vertex)
            
            # Add unmarked neighbors to queue
            for dim in range(self.dimension):
                neighbor = vertex ^ (1 << dim)
                if neighbor not in visited:
                    queue.append(neighbor)
        
        return visited

