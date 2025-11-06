# Memory Management

This document describes memory management strategies in the Snake-in-the-Box package.

## Memory Constraints

### Per-Node Memory

For an n-dimensional hypercube:
- **Bitmap**: 2^n bits = 2^n / 8 bytes
- **Transition sequence**: ~length × 8 bytes
- **Object overhead**: ~200 bytes
- **Total**: ~2^n / 8 + length × 8 + 200 bytes

### Scaling

| Dimension | Bitmap Size | Node Size (length=100) |
|-----------|-------------|------------------------|
| 7 | 16 bytes | ~200 bytes |
| 10 | 128 bytes | ~1KB |
| 13 | 1KB | ~2KB |
| 16 | 8KB | ~10KB |

## Memory Management Strategy

### Two-Level Memory

The algorithm maintains only **two levels** in memory:
1. **Current level**: Nodes being expanded
2. **Next level**: Children being generated

After generating children, the previous level is explicitly freed:

```python
del current_level  # Free memory
current_level = next_level
```

### Pruning Strategy

When memory limit is exceeded:
1. **Estimate**: Calculate memory per node
2. **Calculate**: Determine max nodes that fit
3. **Sort**: Sort nodes by fitness (descending)
4. **Select**: Keep top nodes within limit
5. **Discard**: Remove lower-fitness nodes

### Memory Estimation

Before expansion, estimate memory usage:

```python
def estimate_memory_usage(nodes: List[SnakeNode]) -> float:
    if not nodes:
        return 0.0
    
    bytes_per_node = estimate_node_size(nodes[0])
    total_bytes = len(nodes) * bytes_per_node
    return total_bytes / (1024**3)  # Convert to GB
```

## Optimization Techniques

### Bitmap Efficiency

- Uses `array.array('Q')` for 64-bit words
- Minimal overhead compared to Python lists
- Efficient bit operations

### Lazy Evaluation

- Bitmap is built only when needed
- Fitness calculated once per node
- No redundant computations

### Explicit Memory Freeing

- Explicitly delete previous level
- Python garbage collection handles cleanup
- Reduces peak memory usage

## Memory Limits

### Default Limits

- **Low dimensions (1-6)**: 1GB
- **Medium dimensions (7-9)**: 2-4GB
- **High dimensions (10-13)**: 18-19GB

### Adjusting Limits

```python
# For dimension 10
result = pruned_bfs_search(dimension=10, memory_limit_gb=18.0)

# For dimension 13
result = pruned_bfs_search(dimension=13, memory_limit_gb=19.0)
```

## Memory Profiling

Profile memory usage:

```python
from snake_in_box.benchmarks import profile_memory_usage

# Requires memory_profiler
result = profile_memory_usage(dimension=7, memory_limit_gb=1.0)
```

## Best Practices

1. **Set appropriate limits**: Based on dimension and available memory
2. **Monitor usage**: Use profiling to identify bottlenecks
3. **Use priming**: Reduces search space and memory needs
4. **Free explicitly**: Let Python GC handle cleanup
5. **Estimate first**: Check memory before expansion

## Related Documentation

- [Data Structures](data-structures.md) - Data structure details
- [Performance Tuning](../guides/performance-tuning.md) - Performance optimization
- [Complexity Analysis](../theory/complexity-analysis.md) - Complexity details

