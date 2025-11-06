# Advanced Usage Guide

This guide covers advanced usage patterns including priming, parallel search, and custom fitness functions.

## Priming Strategy

Extend known snakes to higher dimensions using the priming strategy:

```python
from snake_in_box import prime_search, get_known_snake

# Extend 9D snake to 10D
snake_9d = get_known_snake(9)
snake_10d = prime_search(
    snake_9d,
    target_dimension=10,
    memory_limit_gb=18.0,
    verbose=True
)

if snake_10d:
    print(f"Extended to length {len(snake_10d)}")
```

## Parallel Search

Use parallel processing to speed up search:

```python
from snake_in_box.search import parallel_search

# Search with 10 parallel workers
result = parallel_search(
    dimension=7,
    memory_limit_gb=2.0,
    num_workers=10,
    verbose=True
)
```

## Custom Fitness Functions

Use advanced fitness evaluators for experimentation:

```python
from snake_in_box.search import AdvancedFitnessEvaluator
from snake_in_box import SnakeNode

# Create a node
node = SnakeNode([0, 1, 2], dimension=3)

# Use advanced evaluator
evaluator = AdvancedFitnessEvaluator(node)

# Get individual measures
unmarked = evaluator.count_unmarked_vertices()
dead_ends = evaluator.count_dead_ends()
unreachable = evaluator.count_unreachable_vertices()

# Combined fitness with custom weights
fitness = evaluator.combined_fitness({
    'unmarked': 1.0,
    'dead_ends': -0.5,
    'unreachable': -0.3
})
```

## Batch Analysis

Analyze multiple dimensions at once:

```python
from snake_in_box.analysis import analyze_dimensions, generate_analysis_report
from snake_in_box.utils import export_analysis_data

# Analyze dimensions 1-13
results = analyze_dimensions(
    dimensions=list(range(1, 14)),
    use_known=True,
    memory_limit_gb=2.0,
    verbose=True
)

# Generate comprehensive report
generate_analysis_report(
    results,
    output_file="output/reports/analysis_report.md",
    format="markdown"
)

# Export data in multiple formats
exported = export_analysis_data(
    results,
    output_dir="output/data",
    include_sequences=True
)
# Creates: analysis_results_comprehensive.json, analysis_summary.csv, statistics.json
```

## Working with Bitmaps

Directly manipulate hypercube bitmaps:

```python
from snake_in_box.core import HypercubeBitmap

# Create bitmap for 3D hypercube
bitmap = HypercubeBitmap(3)

# Mark vertices
bitmap.set_bit(0)
bitmap.set_bit(1)
bitmap.set_bit(2)

# Check if marked
is_marked = bitmap.get_bit(0)  # Returns True

# Count unmarked
unmarked = bitmap.count_unmarked()  # Returns 5
```

## Parsing Hex Strings

Parse hex string representations of snakes:

```python
from snake_in_box.core import parse_hex_transition_string

# Parse hex string
hex_str = "0120314021"
transitions = parse_hex_transition_string(hex_str)
# Returns [0, 1, 2, 0, 3, 1, 4, 0, 2, 1]

# Also supports comma-separated
comma_str = "0,1,2,0,3"
transitions = parse_hex_transition_string(comma_str)
```

## Performance Profiling

Profile memory and CPU usage:

```python
from snake_in_box.benchmarks import profile_performance, profile_memory_usage

# CPU profiling
result = profile_performance(
    dimension=7,
    output_file="profile_stats.txt",
    sort_by='cumulative',
    num_stats=20
)

# Memory profiling (requires memory_profiler)
# result = profile_memory_usage(dimension=7, memory_limit_gb=1.0)
```

## Custom Search Strategies

Implement custom search strategies by extending the base classes:

```python
from snake_in_box.core import SnakeNode
from snake_in_box.search import SimpleFitnessEvaluator

class CustomFitnessEvaluator(SimpleFitnessEvaluator):
    def evaluate(self):
        # Custom fitness calculation
        base_fitness = super().evaluate()
        # Add custom logic
        return base_fitness * 1.1  # Example: boost fitness
```

## Error Handling

Handle errors gracefully:

```python
from snake_in_box import pruned_bfs_search
from snake_in_box.core import SnakeNode

try:
    result = pruned_bfs_search(dimension=7, memory_limit_gb=2.0)
    if result:
        print(f"Success: length {result.get_length()}")
    else:
        print("Search completed but no snake found")
except ValueError as e:
    print(f"Invalid input: {e}")
except MemoryError:
    print("Memory limit exceeded")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Working with Large Dimensions

For high dimensions, use priming and adjust memory limits:

```python
from snake_in_box import prime_search, get_known_snake

# For dimension 13, use priming
snake_12d = get_known_snake(12)
snake_13d = prime_search(
    snake_12d,
    target_dimension=13,
    memory_limit_gb=19.0,  # Higher memory for high dimensions
    verbose=True
)
```

## Related Documentation

- [Basic Usage](basic-usage.md) - Basic patterns
- [Priming Strategy](../algorithm/priming-strategy.md) - Priming details
- [Performance Tuning](performance-tuning.md) - Performance optimization
- [API Reference](../api/search.md) - Complete API documentation

