# Data Structures

This document describes the core data structures used in the Snake-in-the-Box package.

## HypercubeBitmap

Memory-efficient bitmap representation of hypercube vertices.

### Structure

```python
class HypercubeBitmap:
    dimension: int          # Dimension of hypercube
    num_vertices: int        # Total vertices (2^n)
    num_words: int          # Number of 64-bit words
    bitmap: array.array     # Array of 64-bit unsigned integers
```

### Memory Layout

- Uses `array.array('Q')` for 64-bit words
- Each bit represents one vertex
- 0 = unmarked (available)
- 1 = marked (occupied or prohibited)

### Memory Efficiency

For n-dimensional hypercube:
- **Total bits**: 2^n
- **Words needed**: (2^n + 63) // 64
- **Memory**: (2^n + 63) // 64 × 8 bytes

Example: Dimension 13
- 2^13 = 8,192 vertices
- 8,192 / 64 = 128 words
- 128 × 8 = 1,024 bytes = 1KB per bitmap

### Operations

- `set_bit(vertex)`: O(1) - Mark vertex
- `get_bit(vertex)`: O(1) - Check if marked
- `count_unmarked()`: O(2^n) - Count available vertices

## SnakeNode

Represents a node in the search tree.

### Structure

```python
class SnakeNode:
    transition_sequence: List[int]  # Snake path
    dimension: int                   # Hypercube dimension
    vertices_bitmap: HypercubeBitmap  # Vertex state
    fitness: int                     # Unmarked vertex count
```

### Components

1. **Transition Sequence**: List of bit positions defining the snake path
2. **Bitmap**: Tracks which vertices are occupied or prohibited
3. **Fitness**: Count of unmarked vertices (used for pruning)

### Memory Per Node

For n-dimensional hypercube:
- **Transition sequence**: ~length × 8 bytes (list overhead + ints)
- **Bitmap**: ~2^n / 8 bytes
- **Object overhead**: ~200 bytes
- **Total**: ~2^n / 8 + length × 8 + 200 bytes

Example: Dimension 13, length 100
- Bitmap: 1KB
- Sequence: ~800 bytes
- Overhead: ~200 bytes
- **Total**: ~2KB per node

### Operations

- `can_extend(dim)`: O(1) - Check if can extend
- `create_child(dim)`: O(2^n) - Create child (rebuilds bitmap)
- `get_length()`: O(1) - Get snake length
- `get_current_vertex()`: O(length) - Compute current vertex

## Search Tree Structure

The search tree is organized as:

```
Level 0: [empty snake]
Level 1: [0], [1], [2], ...
Level 2: [0,1], [0,2], [1,0], ...
...
```

### Memory Management

Only **two levels** are kept in memory:
- Current level (being expanded)
- Next level (children being generated)

After expansion, previous level is freed.

## Data Flow

1. **Initialization**: Create empty SnakeNode
2. **Extension**: Create child nodes by extending snake
3. **Bitmap Update**: Mark new vertex and adjacent vertices
4. **Fitness Calculation**: Count unmarked vertices
5. **Pruning**: Sort by fitness, keep top nodes

## Related Documentation

- [Package Structure](package-structure.md) - Package organization
- [Memory Management](memory-management.md) - Memory optimization
- [Core Module API](../api/core.md) - API reference

