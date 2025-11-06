# Benchmarks Module API

The `benchmarks` module provides known snake records, performance profiling tools, and validation functions.

## Known Records

### `KNOWN_RECORDS`

Dictionary of known record lengths.

```python
from snake_in_box.benchmarks import KNOWN_RECORDS

KNOWN_RECORDS = {
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

## Functions

### `get_known_record(dimension: int) -> Optional[int]`

Get known record length for a dimension.

**Parameters:**
- `dimension` (int): Dimension to query

**Returns:**
- `Optional[int]`: Known record length, or None if not available

**Example:**
```python
from snake_in_box.benchmarks import get_known_record
record = get_known_record(13)  # Returns 2854
```

### `get_known_snake(dimension: int) -> Optional[List[int]]`

Get known snake transition sequence.

**Supported Dimensions**: 9-13 (from Ace 2025)

**Parameters:**
- `dimension` (int): Dimension to query

**Returns:**
- `Optional[List[int]]`: Transition sequence, or None if not available

**Example:**
```python
from snake_in_box.benchmarks import get_known_snake
snake_13d = get_known_snake(13)  # Returns list of length 2854
```

### `validate_known_snake(dimension: int) -> Tuple[bool, str]`

Validate a known snake from database.

**Parameters:**
- `dimension` (int): Dimension to validate

**Returns:**
- `Tuple[bool, str]`: (is_valid, message)

**Example:**
```python
from snake_in_box.benchmarks import validate_known_snake
is_valid, msg = validate_known_snake(13)
print(f"Valid: {is_valid}")
```

### `profile_memory_usage(dimension: int, memory_limit_gb: float = 1.0) -> Optional[SnakeNode]`

Profile memory usage during search.

**Parameters:**
- `dimension` (int): Dimension to profile
- `memory_limit_gb` (float, optional): Memory limit (default: 1.0)

**Returns:**
- `Optional[SnakeNode]`: Snake node or None

**Note:** Requires `@profile` decorator or `python -m memory_profiler`

### `profile_performance(dimension: int, output_file: Optional[str] = None, sort_by: str = 'cumulative', num_stats: int = 20) -> Optional[SnakeNode]`

Profile CPU performance using cProfile.

**Parameters:**
- `dimension` (int): Dimension to profile
- `output_file` (Optional[str]): Save stats to file (default: None)
- `sort_by` (str): Sort key (default: 'cumulative')
- `num_stats` (int): Number of top functions (default: 20)

**Returns:**
- `Optional[SnakeNode]`: Snake node or None

**Example:**
```python
from snake_in_box.benchmarks import profile_performance
result = profile_performance(7, 'profile_stats.txt')
```

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

## Related Documentation

- [Known Records](../theory/hypercube-graphs.md#known-records) - Known bounds
- [Performance Tuning](../guides/performance-tuning.md) - Performance optimization
- [Benchmarks Module AGENTS](../../snake_in_box/benchmarks/AGENTS.md) - Module documentation

