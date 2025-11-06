"""Hypercube bitmap representation for vertex tracking."""

import array
from typing import List


class HypercubeBitmap:
    """Memory-efficient bitmap for tracking hypercube vertices.
    
    Uses an array of 64-bit unsigned integers to represent vertex states.
    Each bit represents one vertex in the hypercube, where:
    - 0 = unmarked (available)
    - 1 = marked (occupied or prohibited)
    
    Attributes
    ----------
    dimension : int
        Dimension of the hypercube (n in Q_n)
    num_vertices : int
        Total number of vertices (2^n)
    num_words : int
        Number of 64-bit words needed to represent all vertices
    bitmap : array.array
        Array of 64-bit unsigned integers ('Q' type)
    
    Examples
    --------
    >>> bitmap = HypercubeBitmap(3)
    >>> bitmap.set_bit(0)
    >>> bitmap.get_bit(0)
    True
    >>> bitmap.count_unmarked()
    7
    """
    
    def __init__(self, dimension: int):
        """Initialize bitmap for n-dimensional hypercube."""
        if dimension < 1:
            raise ValueError(f"Dimension must be >= 1, got {dimension}")
        
        self.dimension = dimension
        self.num_vertices = 1 << dimension  # 2^n
        # Use 64-bit words, calculate number needed
        self.num_words = (self.num_vertices + 63) // 64
        # Initialize all bits to 0 (unmarked)
        self.bitmap = array.array('Q', [0] * self.num_words)
    
    def set_bit(self, vertex: int) -> None:
        """Mark vertex as occupied/prohibited."""
        if vertex < 0 or vertex >= self.num_vertices:
            raise IndexError(
                f"Vertex {vertex} out of range [0, {self.num_vertices})"
            )
        
        word_idx = vertex >> 6  # Divide by 64
        bit_idx = vertex & 63   # Modulo 64
        self.bitmap[word_idx] |= (1 << bit_idx)
    
    def get_bit(self, vertex: int) -> bool:
        """Check if vertex is marked."""
        if vertex < 0 or vertex >= self.num_vertices:
            raise IndexError(
                f"Vertex {vertex} out of range [0, {self.num_vertices})"
            )
        
        word_idx = vertex >> 6
        bit_idx = vertex & 63
        return bool(self.bitmap[word_idx] & (1 << bit_idx))
    
    def clear_bit(self, vertex: int) -> None:
        """Unmark vertex."""
        if vertex < 0 or vertex >= self.num_vertices:
            raise IndexError(
                f"Vertex {vertex} out of range [0, {self.num_vertices})"
            )
        
        word_idx = vertex >> 6
        bit_idx = vertex & 63
        self.bitmap[word_idx] &= ~(1 << bit_idx)
    
    def count_unmarked(self) -> int:
        """Count unmarked vertices (fitness function)."""
        count = 0
        for vertex in range(self.num_vertices):
            if not self.get_bit(vertex):
                count += 1
        return count
    
    def count_unmarked_fast(self) -> int:
        """Count unmarked vertices using popcount."""
        marked_bits = sum(bin(word).count('1') for word in self.bitmap)
        return self.num_vertices - marked_bits
    
    def clear_all(self) -> None:
        """Clear all bits."""
        for i in range(self.num_words):
            self.bitmap[i] = 0
    
    def copy(self) -> 'HypercubeBitmap':
        """Create a copy of this bitmap."""
        new_bitmap = HypercubeBitmap(self.dimension)
        new_bitmap.bitmap = array.array('Q', self.bitmap)
        return new_bitmap

