# Core Module: Agent Documentation

## Purpose

The `core` module provides fundamental data structures and utilities for the snake-in-the-box problem. It implements the mathematical foundations including hypercube representation, vertex/transition conversions, and validation.

## Key Classes

### HypercubeBitmap

**Purpose**: Memory-efficient bitmap representation of hypercube vertices.

**Key Methods**:
- `set_bit(vertex)`: Mark vertex as occupied/prohibited
- `get_bit(vertex)`: Check if vertex is marked
- `count_unmarked()`: Count available vertices (fitness function)

**Memory**: Uses `array.array('Q')` for 64-bit words, O(2^n/64) space.

**Usage**:
```python
from snake_in_box.core import HypercubeBitmap
bitmap = HypercubeBitmap(3)  # 3D hypercube
bitmap.set_bit(0)
count = bitmap.count_unmarked()
```

### SnakeNode

**Purpose**: Represents a node in the search tree, containing a snake and its hypercube state.

**Key Attributes**:
- `transition_sequence`: List[int] - Snake path
- `dimension`: int - Hypercube dimension
- `vertices_bitmap`: HypercubeBitmap - Vertex state
- `fitness`: int - Unmarked vertex count

**Key Methods**:
- `can_extend(dim)`: Check if extension is valid
- `create_child(dim)`: Create child node
- `get_current_vertex()`: Get end vertex of snake

**Usage**:
```python
from snake_in_box.core import SnakeNode
node = SnakeNode([0, 1, 2], 3)
child = node.create_child(0)
```

## Key Functions

### Transition/Vertex Conversions

**`vertex_to_transition(vertex_sequence)`**
- Converts vertex sequence to transition sequence
- Computes bit position changes using XOR

**`transition_to_vertex(transition_sequence, dimension, start_vertex=0)`**
- Converts transition sequence to vertex sequence
- Applies bit flips sequentially

**`compute_current_vertex(transition_sequence)`**
- Computes final vertex from transitions
- Starting from origin (0)

**`parse_hex_transition_string(hex_string)`**
- Parses hex string representation of transition sequence
- Supports both hex digits and comma-separated formats
- Returns transition sequence as list of integers

### Validation

**`validate_snake(vertex_sequence)`**
- Validates snake constraints:
  - Consecutive vertices: Hamming distance = 1
  - Non-consecutive vertices: Hamming distance > 1
- Returns: `(bool, str)` - (is_valid, error_message)

**`validate_transition_sequence(transition_sequence, dimension)`**
- Validates transition sequence format
- Converts to vertices and validates

**`hamming_distance(a, b)`**
- Calculates Hamming distance between integers
- Counts differing bits

## Dependencies

- `array` (standard library): For bitmap storage
- No external dependencies

## Performance

- Bitmap operations: O(1) for set/get
- Fitness calculation: O(2^n) for full count, O(n_words) for fast version
- Validation: O(n²) for n vertices

## Testing

See `tests/test_core/` for comprehensive tests:
- `test_hypercube.py`: Bitmap operations
- `test_transitions.py`: Conversion functions
- `test_validation.py`: Validation logic
- `test_snake_node.py`: Node operations

## Mathematical Foundations

### Hypercube Properties
- Vertices: 2^n
- Edges: n·2^(n-1)
- Degree: n (regular graph)
- Distance: Hamming distance

### Snake Constraints
- Induced path: No shortcuts between non-consecutive vertices
- Hamming distance: Consecutive = 1, Non-consecutive > 1

