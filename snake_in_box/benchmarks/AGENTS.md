# Benchmarks Module: Agent Documentation

## Purpose

The `benchmarks` module provides known snake records, performance profiling tools, and validation functions for comparing results against literature.

## Known Snakes Database

### get_known_record(dimension)

**Purpose**: Get known record length for a dimension.

**Returns**: `int` or `None`

**Usage**:
```python
from snake_in_box.benchmarks import get_known_record
record = get_known_record(13)  # Returns 2854
```

### get_known_snake(dimension)

**Purpose**: Get known snake transition sequence.

**Supported Dimensions**: 9-13 (from Ace 2025)

**Returns**: `List[int]` or `None`

**Usage**:
```python
from snake_in_box.benchmarks import get_known_snake
snake_13d = get_known_snake(13)  # Length 2854
```

### KNOWN_RECORDS

**Purpose**: Dictionary of known record lengths.

**Contents**:
```python
{
    3: 4,    # Optimal
    4: 7,    # Optimal
    5: 13,   # Optimal
    6: 26,   # Optimal
    7: 50,   # Ace (2025)
    8: 97,   # Ace (2025)
    9: 188,  # Wynn (2012)
    10: 373, # Ace (2025)
    11: 732, # Ace (2025) - new lower bound
    12: 1439,# Ace (2025) - new lower bound
    13: 2854 # Ace (2025) - new lower bound
}
```

### SNAKE_13D_HEX_STRING

**Purpose**: Full 13D snake transition sequence in hex format.

**Source**: Ace (2025) appendix

**Truncation Points**:
- 190: Dimension 9
- 373: Dimension 10
- 732: Dimension 11
- 1439: Dimension 12
- 2854: Dimension 13 (full)

## Performance Profiling

### profile_memory_usage(dimension, memory_limit_gb=1.0)

**Purpose**: Profile memory usage during search.

**Usage**: Requires `@profile` decorator or `python -m memory_profiler`

**Returns**: `SnakeNode` or `None`

### profile_performance(dimension, output_file=None, sort_by='cumulative', num_stats=20)

**Purpose**: Profile CPU performance using cProfile.

**Parameters**:
- `dimension`: int - Dimension to profile
- `output_file`: str - Save stats to file
- `sort_by`: str - Sort key
- `num_stats`: int - Number of top functions

**Returns**: `SnakeNode` or `None`

**Usage**:
```python
from snake_in_box.benchmarks import profile_performance
result = profile_performance(7, 'profile_stats.txt')
```

### benchmark_known_snakes()

**Purpose**: Benchmark search against known records.

**Usage**:
```python
from snake_in_box.benchmarks import benchmark_known_snakes
benchmark_known_snakes()
```

## Validation

### validate_known_snake(dimension)

**Purpose**: Validate a known snake from database.

**Returns**: `(bool, str)` - (is_valid, message)

**Usage**:
```python
from snake_in_box.benchmarks import validate_known_snake
is_valid, msg = validate_known_snake(13)
```

## Dependencies

- `core/`: Validation, transitions
- `search/`: Search algorithms
- `cProfile`: For performance profiling (standard library)
- `memory_profiler`: For memory profiling (optional)

## Data Sources

1. **Ace (2025)**: Dimensions 7-13, new lower bounds
2. **Wynn (2012)**: Dimension 9, length 190
3. **Literature**: Optimal results for dimensions 3-6

## Performance Benchmarks

From Ace (2025) paper:
- Dimension 10: 50 minutes (Intel i5-12600K, 18GB, 10 threads)
- Dimension 13: 2 hours (19GB memory)

Python implementation will vary based on:
- System specifications
- Python version
- Optimization level

## Testing

See `tests/test_benchmarks/`:
- `test_known_snakes.py`: Database and validation

## Usage Patterns

### Compare Results
```python
from snake_in_box import pruned_bfs_search, get_known_record
result = pruned_bfs_search(dimension=7)
expected = get_known_record(7)
print(f"Found: {result.get_length()}, Expected: {expected}")
```

### Validate Known Snakes
```python
from snake_in_box.benchmarks import validate_known_snake
for dim in range(9, 14):
    is_valid, msg = validate_known_snake(dim)
    print(f"Dim {dim}: {is_valid}")
```

