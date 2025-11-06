# Basic Usage Guide

This guide covers basic usage patterns for the Snake-in-the-Box package.

## Basic Search

The simplest way to use the package is to search for a snake in a given dimension:

```python
from snake_in_box import pruned_bfs_search, export_snake

# Search for snake in 7-dimensional hypercube
result = pruned_bfs_search(dimension=7, memory_limit_gb=2.0)

if result:
    print(f"Found snake of length {result.get_length()}")
    export_snake(result, "snake_7d")
```

## Using Known Snakes

For dimensions with known records, you can retrieve them directly:

```python
from snake_in_box import get_known_snake, get_known_record
from snake_in_box.benchmarks import validate_known_snake

# Get known record for dimension 13
record = get_known_record(13)  # Returns 2854

# Get the actual snake sequence
snake_13d = get_known_snake(13)

# Validate it
is_valid, msg = validate_known_snake(13)
print(f"Valid: {is_valid}")
```

## Working with SnakeNodes

A `SnakeNode` represents a snake and provides useful methods:

```python
from snake_in_box import SnakeNode

# Create a snake node
node = SnakeNode([0, 1, 2, 0], dimension=3)

# Get snake properties
length = node.get_length()  # Returns 4
fitness = node.fitness  # Count of unmarked vertices
current_vertex = node.get_current_vertex()  # Current vertex

# Check if can extend
can_extend = node.can_extend(dimension=1)

# Create child node
if can_extend:
    child = node.create_child(dimension=1)
```

## Converting Between Formats

Convert between transition sequences and vertex sequences:

```python
from snake_in_box import transition_to_vertex, vertex_to_transition

# Transition sequence to vertices
transitions = [0, 1, 2, 0]
vertices = transition_to_vertex(transitions, dimension=3)
# Returns [0, 1, 3, 7, 6]

# Vertices to transitions
transitions_back = vertex_to_transition(vertices)
# Returns [0, 1, 2, 0]
```

## Validating Snakes

Validate that a sequence represents a valid snake:

```python
from snake_in_box import validate_snake, validate_transition_sequence

# Validate vertex sequence
vertices = [0, 1, 3, 7, 6]
is_valid, msg = validate_snake(vertices)
if is_valid:
    print("Valid snake!")
else:
    print(f"Invalid: {msg}")

# Validate transition sequence
transitions = [0, 1, 2, 0]
is_valid, msg = validate_transition_sequence(transitions, dimension=3)
```

## Exporting Results

Export snakes to multiple formats:

```python
from snake_in_box import pruned_bfs_search, export_snake

result = pruned_bfs_search(dimension=7)

if result:
    # Export to JSON, text, and CSV
    export_snake(result, "snake_7d")
    # Creates:
    # - snake_7d.json (full metadata)
    # - snake_7d.txt (hex string)
    # - snake_7d_comma.txt (CSV format)
```

## Canonical Form

Check and work with canonical form:

```python
from snake_in_box import is_canonical, get_legal_next_dimensions

# Check if sequence is canonical
seq = [0, 1, 2, 0, 1]
is_canon = is_canonical(seq)  # Returns True

# Get legal next dimensions
legal = get_legal_next_dimensions([0, 1, 2])
# Returns [0, 1, 2, 3]
```

## Next Steps

- See [Advanced Usage](advanced-usage.md) for more complex patterns
- Check [Visualization Guide](visualization.md) for visualization examples
- Read [Performance Tuning](performance-tuning.md) for optimization tips

## Related Documentation

- [Getting Started](../getting-started.md) - Quick start guide
- [API Reference](../api/core.md) - Complete API documentation
- [Algorithm Overview](../algorithm/overview.md) - Algorithm details

