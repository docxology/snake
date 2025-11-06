# Getting Started

This guide will help you get started with the Snake-in-the-Box package.

## Installation

### From Source

```bash
git clone https://github.com/yourusername/snake.git
cd snake
pip install -e .
```

### Dependencies

Core dependencies:
- Python 3.8+
- numpy >= 1.20.0

Optional dependencies:
- matplotlib >= 3.3.0 (for visualization)
- memory-profiler >= 0.60.0 (for profiling)
- pytest >= 7.0.0 (for testing)

Install with optional dependencies:
```bash
pip install -e ".[dev]"
```

## Basic Example

### Simple Search

```python
from snake_in_box import pruned_bfs_search, export_snake

# Search for snake in 7-dimensional hypercube
result = pruned_bfs_search(dimension=7, memory_limit_gb=2.0)

if result:
    print(f"Found snake of length {result.get_length()}")
    export_snake(result, "snake_7d")
```

### Using Known Snakes

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

### Priming Strategy

```python
from snake_in_box import prime_search, get_known_snake

# Extend 9D snake to 10D
snake_9d = get_known_snake(9)
snake_10d = prime_search(snake_9d, target_dimension=10)
```

### Visualization

```python
from snake_in_box import pruned_bfs_search, visualize_snake_auto

# For 3D only
result = pruned_bfs_search(dimension=3)
if result:
    visualize_snake_auto(result)
```

## Next Steps

- Read the [Algorithm Overview](algorithm/overview.md) to understand how the search works
- Check out [Basic Usage](guides/basic-usage.md) for more examples
- Explore the [API Reference](api/core.md) for detailed function documentation
- See [Performance Tuning](guides/performance-tuning.md) for optimization tips

