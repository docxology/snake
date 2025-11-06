# Priming Strategy

The priming strategy extends known good snakes from lower dimensions to higher dimensions, making high-dimensional search tractable.

## Motivation

For high dimensions (9+), exhaustive search from an empty snake becomes computationally infeasible. The priming strategy addresses this by:

1. Starting from a known good snake in dimension n
2. Extending it to dimension n+1 (or higher)
3. Using the extended snake as a seed for further search

This approach was used to discover all record-breaking snakes in dimensions 11-13.

## How Priming Works

### Basic Strategy

1. **Start with Known Snake**: Begin with a validated snake from a lower dimension
2. **Extend to Higher Dimension**: Create a SnakeNode in the higher dimension
3. **Search from Seed**: Run pruned BFS starting from the seed snake
4. **Iterate**: Continue extending dimension by dimension

### Example: Extending 9D to 10D

```python
# Get known 9D snake (length 188 from Wynn 2012)
snake_9d = get_known_snake(9)

# Extend to 10D
snake_10d = prime_search(snake_9d, target_dimension=10)
```

The algorithm:
1. Creates a SnakeNode with the 9D snake in 10D space
2. Runs pruned BFS starting from this seed
3. Allows using the new dimension (9) for extensions
4. Finds extensions beyond the original 9D snake length

## Implementation

### Prime Search Function

```python
def prime_search(
    lower_dimension_snake: List[int],
    target_dimension: int,
    memory_limit_gb: float = 18.0,
    verbose: bool = True
) -> Optional[List[int]]:
    """Extend a snake from dimension n to dimension n+1 or higher."""
    current_snake = lower_dimension_snake
    current_dim = detect_dimension(current_snake)
    
    while current_dim < target_dimension:
        # Create initial node seeded with current snake
        initial_node = SnakeNode(current_snake, current_dim + 1)
        
        # Run pruned BFS starting from this seed
        extended_snake_node = pruned_bfs_search_from_seed(
            initial_node,
            current_dim + 1,
            memory_limit_gb=memory_limit_gb,
            verbose=verbose
        )
        
        if extended_snake_node is None:
            return None
        
        current_snake = extended_snake_node.transition_sequence
        current_dim += 1
    
    return current_snake
```

### Backtracking Strategy

When the seed snake cannot be extended, the algorithm tries shorter prefixes:

```python
# Try shorter prefixes to find extension points
for prefix_ratio in [0.95, 0.9, 0.85, 0.8, 0.75]:
    prefix_len = int(seed_len * prefix_ratio)
    prefix_seq = seed_node.transition_sequence[:prefix_len]
    prefix_node = SnakeNode(prefix_seq, dimension)
    # Check if this prefix can extend
```

This allows finding extension points even if the full seed is stuck.

## Known Results

All record-breaking snakes for dimensions 11-13 were found using priming:

- **Dimension 9**: Length 188 (Wynn 2012) - used as seed
- **Dimension 10**: Length 373 - extended from 9D
- **Dimension 11**: Length 732 - extended from 10D
- **Dimension 12**: Length 1439 - extended from 11D
- **Dimension 13**: Length 2854 - extended from 12D

The 13D snake's transition sequence can be truncated at positions 190, 373, 732, and 1439 to get the snakes for dimensions 9, 10, 11, and 12, respectively.

## Why Priming Works

1. **Good Starting Point**: Known snakes provide a strong starting position
2. **Dimensional Extension**: Higher dimensions provide more space for extension
3. **Tractability**: Makes high-dimensional search feasible
4. **Quality Preservation**: Good snakes in lower dimensions often extend well

## Limitations

As noted by Kinny (2012), "priming is an inherently unsafe method for finding optimal snakes." However, it's a widely-used technique to make search tractable for high dimensions.

## Performance

From the paper:
- **Dimension 10**: 50 minutes to extend 9D snake (Intel i5-12600K, 18GB, 10 threads)
- **Dimension 13**: 2 hours to extend 12D snake (19GB memory)

## References

- Ace, Thomas E. "New Lower Bounds for Snake-in-the-Box in 11-, 12-, and 13-dimensional Hypercubes." (2025)
- Wynn, E. "Constructing circuit codes by permuting initial sequences." arXiv:1201.1647v1 (2012)
- Kinny, D. "A new approach to the Snake-In-The-Box-problem." Proc. ECAI 2012, 462–467

## Related Documentation

- [Algorithm Overview](overview.md) - Algorithm overview
- [Pruned BFS Algorithm](pruned-bfs.md) - Search algorithm
- [Known Records](../api/benchmarks.md) - Known snake records

