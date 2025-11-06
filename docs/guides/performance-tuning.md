# Performance Tuning Guide

This guide covers performance optimization strategies for the Snake-in-the-Box package.

## Memory Management

### Adjusting Memory Limits

Increase memory limits for higher dimensions:

```python
from snake_in_box import pruned_bfs_search

# For dimension 10
result = pruned_bfs_search(dimension=10, memory_limit_gb=18.0)

# For dimension 13
result = pruned_bfs_search(dimension=13, memory_limit_gb=19.0)
```

### Memory Estimation

Estimate memory usage before search:

```python
from snake_in_box.core import SnakeNode
from snake_in_box.search.bfs_pruned import estimate_memory_usage

# Create sample node
node = SnakeNode([0, 1, 2], dimension=7)
nodes = [node] * 1000

# Estimate memory
memory_gb = estimate_memory_usage(nodes)
print(f"Estimated memory: {memory_gb:.2f} GB")
```

## Parallel Processing

Use parallel search for speedup:

```python
from snake_in_box.search import parallel_search

# Use 10 workers (from paper)
result = parallel_search(
    dimension=7,
    memory_limit_gb=2.0,
    num_workers=10,
    verbose=True
)
```

## Priming Strategy

Use priming for high dimensions to reduce search time:

```python
from snake_in_box import prime_search, get_known_snake

# Extend from lower dimension (much faster)
snake_9d = get_known_snake(9)
snake_10d = prime_search(
    snake_9d,
    target_dimension=10,
    memory_limit_gb=18.0
)
```

## Fitness Function Selection

Choose appropriate fitness function:

```python
from snake_in_box.search import SimpleFitnessEvaluator, AdvancedFitnessEvaluator

# Simple (default, fastest)
evaluator = SimpleFitnessEvaluator(node)
fitness = evaluator.evaluate()

# Advanced (more accurate but slower)
evaluator = AdvancedFitnessEvaluator(node)
fitness = evaluator.combined_fitness({
    'unmarked': 1.0,
    'dead_ends': -0.5
})
```

## Profiling Performance

Profile to identify bottlenecks:

```python
from snake_in_box.benchmarks import profile_performance

# CPU profiling
result = profile_performance(
    dimension=7,
    output_file="profile_stats.txt",
    sort_by='cumulative',
    num_stats=20
)

# Check profile_stats.txt for top functions
```

## Dimension-Specific Strategies

### Low Dimensions (1-6)

- Use default settings
- No priming needed
- Fast execution

```python
result = pruned_bfs_search(dimension=5, memory_limit_gb=1.0)
```

### Medium Dimensions (7-9)

- Moderate memory limits
- Consider parallel processing

```python
result = parallel_search(dimension=8, num_workers=4, memory_limit_gb=4.0)
```

### High Dimensions (10-13)

- Use priming strategy
- Higher memory limits
- Parallel processing recommended

```python
snake_9d = get_known_snake(9)
snake_13d = prime_search(
    snake_9d,
    target_dimension=13,
    memory_limit_gb=19.0
)
```

## System Requirements

From the paper (C++ implementation):
- **Dimension 10**: 50 minutes (Intel i5-12600K, 18GB, 10 threads)
- **Dimension 13**: 2 hours (19GB memory)

Python implementation will vary based on:
- System specifications
- Python version
- Available memory

## Optimization Tips

1. **Use Known Snakes**: Retrieve known snakes instead of searching when available
2. **Priming**: Always use priming for dimensions 10+
3. **Memory Limits**: Set appropriate memory limits based on dimension
4. **Parallel Processing**: Use parallel search for speedup
5. **Profiling**: Profile to identify bottlenecks

## Expected Performance

- **Dimension 7**: Seconds to minutes
- **Dimension 8**: Minutes
- **Dimension 9**: Minutes to tens of minutes
- **Dimension 10**: 50+ minutes (with priming)
- **Dimension 11-13**: Hours (with priming)

## Related Documentation

- [Performance Benchmarks](../api/benchmarks.md) - Known performance data
- [Memory Management](../architecture/memory-management.md) - Memory optimization
- [Priming Strategy](../algorithm/priming-strategy.md) - Priming details
- [Complexity Analysis](../theory/complexity-analysis.md) - Computational complexity

