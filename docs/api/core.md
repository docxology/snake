# Core Module API

The `core` module provides fundamental data structures and utilities for the snake-in-the-box problem.

## Classes

### HypercubeBitmap

Memory-efficient bitmap representation of hypercube vertices.

```python
from snake_in_box.core import HypercubeBitmap

bitmap = HypercubeBitmap(dimension: int)
```

#### Parameters
- `dimension` (int): Dimension of hypercube (n in Q_n)

#### Attributes
- `dimension` (int): Dimension of hypercube
- `num_vertices` (int): Total number of vertices (2^n)
- `num_words` (int): Number of 64-bit words needed
- `bitmap` (array.array): Array of 64-bit unsigned integers

#### Methods

##### `set_bit(vertex: int) -> None`
Mark vertex as occupied/prohibited.

##### `get_bit(vertex: int) -> bool`
Check if vertex is marked.

##### `clear_bit(vertex: int) -> None`
Unmark vertex.

##### `count_unmarked() -> int`
Count available (unmarked) vertices.

#### Example
```python
bitmap = HypercubeBitmap(3)  # 3D hypercube
bitmap.set_bit(0)
count = bitmap.count_unmarked()  # Returns 7
```

### SnakeNode

Represents a node in the search tree, containing a snake and its hypercube state.

```python
from snake_in_box.core import SnakeNode

node = SnakeNode(transition_sequence: List[int], dimension: int)
```

#### Parameters
- `transition_sequence` (List[int]): Sequence of bit positions defining snake path
- `dimension` (int): Dimension of hypercube

#### Attributes
- `transition_sequence` (List[int]): Snake path
- `dimension` (int): Hypercube dimension
- `vertices_bitmap` (HypercubeBitmap): Vertex state
- `fitness` (int): Count of unmarked vertices

#### Methods

##### `can_extend(new_dimension: int) -> bool`
Check if snake can be extended with given dimension.

##### `create_child(new_dimension: int) -> SnakeNode`
Create child node by extending snake.

##### `get_current_vertex() -> int`
Get current vertex (end of snake path).

##### `get_length() -> int`
Get snake length (number of edges).

#### Example
```python
node = SnakeNode([0, 1, 2], 3)
child = node.create_child(0)
length = node.get_length()  # Returns 3
```

## Functions

### Transition/Vertex Conversions

#### `vertex_to_transition(vertex_sequence: List[int]) -> List[int]`

Convert vertex sequence to transition sequence.

**Parameters:**
- `vertex_sequence` (List[int]): List of vertex labels

**Returns:**
- `List[int]`: Transition sequence

**Example:**
```python
from snake_in_box.core import vertex_to_transition
transitions = vertex_to_transition([0, 1, 3, 7])  # Returns [0, 1, 2]
```

#### `transition_to_vertex(transition_sequence: List[int], dimension: int, start_vertex: int = 0) -> List[int]`

Convert transition sequence to vertex sequence.

**Parameters:**
- `transition_sequence` (List[int]): Sequence of bit positions
- `dimension` (int): Dimension of hypercube
- `start_vertex` (int, optional): Starting vertex (default: 0)

**Returns:**
- `List[int]`: Vertex sequence

**Example:**
```python
from snake_in_box.core import transition_to_vertex
vertices = transition_to_vertex([0, 1, 2, 0], 3)  # Returns [0, 1, 3, 7, 6]
```

#### `compute_current_vertex(transition_sequence: List[int]) -> int`

Compute final vertex from transitions, starting from origin (0).

**Parameters:**
- `transition_sequence` (List[int]): Transition sequence

**Returns:**
- `int`: Final vertex

**Example:**
```python
from snake_in_box.core import compute_current_vertex
vertex = compute_current_vertex([0, 1, 2])  # Returns 7
```

#### `parse_hex_transition_string(hex_string: str) -> List[int]`

Parse hex string representation of transition sequence.

**Parameters:**
- `hex_string` (str): Hex string (e.g., "0120" or "0,1,2,0")

**Returns:**
- `List[int]`: Transition sequence

**Example:**
```python
from snake_in_box.core import parse_hex_transition_string
transitions = parse_hex_transition_string("0120")  # Returns [0, 1, 2, 0]
```

### Validation Functions

#### `validate_snake(vertex_sequence: List[int]) -> Tuple[bool, str]`

Validate that a vertex sequence represents a valid snake.

**Parameters:**
- `vertex_sequence` (List[int]): List of vertex labels

**Returns:**
- `Tuple[bool, str]`: (is_valid, error_message)

**Example:**
```python
from snake_in_box.core import validate_snake
is_valid, msg = validate_snake([0, 1, 3, 7, 6])
```

#### `validate_transition_sequence(transition_sequence: List[int], dimension: int) -> Tuple[bool, str]`

Validate transition sequence format and convert to vertices for validation.

**Parameters:**
- `transition_sequence` (List[int]): Transition sequence
- `dimension` (int): Dimension of hypercube

**Returns:**
- `Tuple[bool, str]`: (is_valid, error_message)

**Example:**
```python
from snake_in_box.core import validate_transition_sequence
is_valid, msg = validate_transition_sequence([0, 1, 2, 0], 3)
```

#### `hamming_distance(a: int, b: int) -> int`

Calculate Hamming distance between two integers (count of differing bits).

**Parameters:**
- `a` (int): First integer
- `b` (int): Second integer

**Returns:**
- `int`: Hamming distance

**Example:**
```python
from snake_in_box.core import hamming_distance
dist = hamming_distance(0b000, 0b111)  # Returns 3
```

### Calculation Functions

#### `calculate_snake_for_dimension(dimension: int) -> Optional[SnakeNode]`

Calculate snake for a given dimension using search or known records.

**Parameters:**
- `dimension` (int): Dimension to calculate

**Returns:**
- `Optional[SnakeNode]`: Snake node or None

## Related Documentation

- [Data Structures](../architecture/data-structures.md) - Detailed data structure documentation
- [Core Module AGENTS](../../snake_in_box/core/AGENTS.md) - Module documentation
- [Algorithm Overview](../algorithm/overview.md) - Algorithm overview

