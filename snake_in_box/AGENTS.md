# Snake-in-the-Box Package: Agent Documentation

## Package Overview

The `snake_in_box` package implements the N-dimensional snake-in-the-box algorithm based on the heuristically-pruned breadth-first search method from Ace (2025). This package provides a complete solution for finding long induced paths in hypercube graphs.

## Architecture

### Core Components

1. **Core Module** (`core/`)
   - Data structures: `HypercubeBitmap`, `SnakeNode`
   - Conversion utilities: transition/vertex sequences
   - Validation functions

2. **Search Module** (`search/`)
   - Pruned BFS algorithm
   - Fitness evaluators
   - Priming strategies
   - Parallel processing

3. **Utilities Module** (`utils/`)
   - Canonical form utilities
   - Export functions
   - Visualization tools

4. **Benchmarks Module** (`benchmarks/`)
   - Known snake records
   - Performance profiling

5. **Analysis Module** (`analysis/`)
   - Dimension analysis (N=1-16)
   - Report generation
   - Validation reports

## Key Design Principles

1. **Modularity**: Each module is self-contained with clear interfaces
2. **Memory Efficiency**: Bitmap-based vertex tracking for large hypercubes
3. **Extensibility**: Easy to add new search strategies or fitness functions
4. **Testability**: Comprehensive test coverage for all components
5. **Documentation**: AGENTS.md at every level for clarity

## Usage Patterns

### Modular Calculation (Recommended)
All calculation methods accept dimension N as a parameter:
```python
from snake_in_box import calculate_snake_for_dimension

# Calculate snake for any dimension N
result = calculate_snake_for_dimension(N=7, memory_limit_gb=18.0)
print(f"Length: {result['length']}, Time: {result['computation_time_seconds']:.2f}s")
```

### Basic Search
```python
from snake_in_box import pruned_bfs_search
result = pruned_bfs_search(dimension=7)
```

### Priming Strategy
```python
from snake_in_box import prime_search, get_known_snake
snake_9d = get_known_snake(9)
snake_10d = prime_search(snake_9d, target_dimension=10)
```

### Analysis with Exponential Tracking
```python
from snake_in_box.analysis import analyze_dimensions, generate_exponential_analysis_report
results = analyze_dimensions(range(1, 17))
generate_exponential_analysis_report(results, "exponential_analysis.md")
```

## Dependencies

- **Core**: numpy (bitmap operations)
- **Visualization**: matplotlib (optional)
- **Profiling**: memory-profiler (optional)
- **Testing**: pytest

## Performance Characteristics

- Memory: O(2^n) for n-dimensional hypercube
- Time: Exponential in worst case, pruned by heuristics
- Parallel: Supports multiprocessing for speedup
- Computation Time Tracking: All methods track computation time with metadata
- Exponential Analysis: Built-in analysis of computation complexity and slowdown points

## Module Dependencies

```
core/ → (no dependencies)
search/ → core/, utils/
utils/ → core/
benchmarks/ → core/
analysis/ → core/, search/, utils/, benchmarks/
```

## Extension Points

1. **Fitness Functions**: Add new evaluators in `search/fitness.py`
2. **Search Strategies**: Add new algorithms in `search/`
3. **Visualization**: Add new methods in `utils/visualize_advanced.py`
4. **Projections**: Add projection methods in `utils/visualization_helpers.py`

## Testing Strategy

- Unit tests for each module
- Integration tests for workflows
- Performance benchmarks
- Validation against known records

## References

- Ace, Thomas E. "New Lower Bounds for Snake-in-the-Box in 11-, 12-, and 13-dimensional Hypercubes." (2025) doi:10.5281/zenodo.17538015

