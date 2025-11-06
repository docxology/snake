"""SnakeNode class for search tree representation."""

from typing import List
from .hypercube import HypercubeBitmap
from .transitions import compute_current_vertex


class SnakeNode:
    """Node in the search tree representing a snake.
    
    Each node maintains:
    - The transition sequence representing the snake path
    - A bitmap marking occupied and prohibited vertices
    - Fitness score (count of unmarked vertices)
    
    Attributes
    ----------
    transition_sequence : List[int]
        Sequence of bit positions that define the snake path
    dimension : int
        Dimension of the hypercube
    vertices_bitmap : HypercubeBitmap
        Bitmap tracking vertex states
    fitness : int
        Count of unmarked (available) vertices
    """
    
    def __init__(self, transition_sequence: List[int], dimension: int):
        """Initialize snake node."""
        if dimension < 1:
            raise ValueError(f"Dimension must be >= 1, got {dimension}")
        
        self.transition_sequence = transition_sequence
        self.dimension = dimension
        
        # Validate transitions are in range
        for trans in transition_sequence:
            if trans < 0 or trans >= dimension:
                raise ValueError(
                    f"Transition {trans} out of range [0, {dimension})"
                )
        
        # Initialize bitmap and calculate fitness
        self.vertices_bitmap = self._initialize_bitmap()
        self.fitness = self._calculate_fitness()
    
    def _get_used_dimensions(self) -> set:
        """Get set of dimensions used in the transition sequence."""
        if not self.transition_sequence:
            return set()
        return set(self.transition_sequence)
    
    def _initialize_bitmap(self) -> HypercubeBitmap:
        """Initialize bitmap marking occupied and prohibited vertices."""
        bitmap = HypercubeBitmap(self.dimension)
        used_dimensions = self._get_used_dimensions()
        
        # Start at origin (vertex 0)
        current_vertex = 0
        self._mark_vertex(current_vertex, bitmap)
        self._mark_adjacent(current_vertex, bitmap, used_dimensions)
        
        # Follow transition sequence to build snake path
        for transition in self.transition_sequence:
            # Move to next vertex by flipping bit at transition position
            current_vertex ^= (1 << transition)
            
            # Mark this vertex as occupied
            self._mark_vertex(current_vertex, bitmap)
            
            # Mark all adjacent vertices as prohibited (only in used dimensions)
            self._mark_adjacent(current_vertex, bitmap, used_dimensions)
        
        return bitmap
    
    def _mark_vertex(self, vertex: int, bitmap: HypercubeBitmap) -> None:
        """Mark vertex as occupied."""
        bitmap.set_bit(vertex)
    
    def _mark_adjacent(self, vertex: int, bitmap: HypercubeBitmap, used_dimensions: set = None) -> None:
        """Mark vertices adjacent to given vertex as prohibited.
        
        Only marks neighbors in dimensions that the snake has actually used.
        This allows extension into new dimensions when embedding lower-dimensional
        snakes into higher-dimensional hypercubes.
        
        Parameters
        ----------
        vertex : int
            Vertex to mark neighbors for
        bitmap : HypercubeBitmap
            Bitmap to mark vertices in
        used_dimensions : set, optional
            Set of dimensions used in the snake. If None, marks all dimensions.
        """
        if used_dimensions is None:
            # Default behavior: mark all dimensions (for backward compatibility)
            used_dimensions = set(range(self.dimension))
        
        # Only mark neighbors in dimensions that have been used
        for dim in used_dimensions:
            if dim < self.dimension:
                adjacent = vertex ^ (1 << dim)
                bitmap.set_bit(adjacent)
    
    def _calculate_fitness(self) -> int:
        """Calculate fitness as count of unmarked vertices."""
        return self.vertices_bitmap.count_unmarked()
    
    def _is_marked(self, vertex: int) -> bool:
        """Check if vertex is marked."""
        return self.vertices_bitmap.get_bit(vertex)
    
    def get_current_vertex(self) -> int:
        """Get current vertex (end of snake path)."""
        return compute_current_vertex(self.transition_sequence)
    
    def can_extend(self, new_dimension: int) -> bool:
        """Check if snake can be extended with given dimension."""
        if new_dimension < 0 or new_dimension >= self.dimension:
            return False
        
        # Compute next vertex
        current_vertex = self.get_current_vertex()
        next_vertex = current_vertex ^ (1 << new_dimension)
        
        # Check if next vertex is available (not marked)
        return not self._is_marked(next_vertex)
    
    def create_child(self, new_dimension: int) -> 'SnakeNode':
        """Create child node by extending snake."""
        if not self.can_extend(new_dimension):
            raise ValueError(
                f"Cannot extend snake with dimension {new_dimension} - "
                f"next vertex is already marked"
            )
        
        new_sequence = self.transition_sequence + [new_dimension]
        return SnakeNode(new_sequence, self.dimension)
    
    def get_length(self) -> int:
        """Get snake length (number of edges)."""
        return len(self.transition_sequence)
    
    def __repr__(self) -> str:
        return f"SnakeNode(dim={self.dimension}, len={self.get_length()}, fit={self.fitness})"

