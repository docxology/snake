# Search Module: Agent Documentation

## Purpose

The `search` module implements the heuristically-pruned breadth-first search algorithm from Ace (2025). It provides multiple search strategies including basic BFS, priming, and parallel processing.

## Key Functions

### pruned_bfs_search

**Purpose**: Main search algorithm using heuristically-pruned BFS.

**Algorithm**:
1. Level-by-level expansion of search tree
2. Generate all valid children for current level
3. Prune by fitness when memory limit exceeded
4. Maintain only two levels in memory
5. Track best snake found

**Parameters**:
- `dimension`: int - Hypercube dimension
- `memory_limit_gb`: float - Memory limit (default: 18.0)
- `verbose`: bool - Print progress (default: True)

**Returns**: `SnakeNode` or `None`

**Usage**:
```python
from snake_in_box.search import pruned_bfs_search
result = pruned_bfs_search(dimension=7, memory_limit_gb=2.0)
```

**Performance**: 
- Time: Exponential, pruned by heuristics
- Memory: O(beam_width × node_size)
- Typical: 50 min for dim 10, 2 hours for dim 13 (from paper)

### prime_search

**Purpose**: Extend known snake from lower to higher dimension.

**Strategy**: Start search from seed snake rather than empty snake.

**Parameters**:
- `lower_dimension_snake`: List[int] - Known snake transitions
- `target_dimension`: int - Target dimension
- `memory_limit_gb`: float - Memory limit
- `verbose`: bool - Print progress

**Returns**: `List[int]` or `None` - Extended transition sequence

**Usage**:
```python
from snake_in_box.search import prime_search, get_known_snake
snake_9d = get_known_snake(9)
snake_10d = prime_search(snake_9d, target_dimension=10)
```

**Note**: All record-breaking snakes for dim 11-13 were found using priming.

### parallel_search

**Purpose**: Parallel search using multiprocessing.

**Parameters**:
- `dimension`: int - Hypercube dimension
- `memory_limit_gb`: float - Memory limit
- `num_workers`: int - Number of workers (default: 10)
- `verbose`: bool - Print progress

**Returns**: `SnakeNode` or `None`

**Usage**:
```python
from snake_in_box.search import parallel_search
result = parallel_search(dimension=7, num_workers=4)
```

## Fitness Evaluators

### SimpleFitnessEvaluator

**Purpose**: Simple unmarked vertex count (paper's method).

**Method**: `evaluate()` returns count of unmarked vertices.

**Note**: Despite simplicity, this was sufficient for record-breaking results.

### AdvancedFitnessEvaluator

**Purpose**: Advanced fitness measures for experimentation.

**Methods**:
- `count_unmarked_vertices()`: Basic count
- `count_dead_ends()`: Vertices with only one neighbor
- `count_unreachable_vertices()`: Unreachable from current position
- `combined_fitness(weights)`: Weighted combination

**Usage**:
```python
from snake_in_box.search import AdvancedFitnessEvaluator
evaluator = AdvancedFitnessEvaluator(node)
fitness = evaluator.combined_fitness({'unmarked': 1.0, 'dead_ends': -0.5})
```

## Dependencies

- `core/`: SnakeNode, canonical utilities
- `utils/`: Canonical form functions
- `multiprocessing`: For parallel search

## Algorithm Details

### Pruning Strategy

When memory limit exceeded:
1. Sort nodes by fitness (descending)
2. Keep top nodes within memory limit
3. Discard lower-fitness nodes

### Memory Management

- Estimate memory before expansion
- Prune proactively if needed
- Explicitly free previous level
- Use efficient bitmap storage

### Canonical Form

Uses Kochut's canonical form to reduce search space:
- First transition must be 0
- Subsequent transitions ≤ max_dimension_used + 1

## Testing

See `tests/test_search/`:
- `test_bfs_pruned.py`: Main algorithm
- `test_fitness.py`: Fitness evaluators
- `test_priming.py`: Priming strategy

## Performance Optimization

1. **Memory**: Bitmap-based vertex tracking
2. **Pruning**: Fitness-based node selection
3. **Parallel**: Multiprocessing for speedup
4. **Canonical**: Symmetry reduction

## Known Results

From Ace (2025):
- Dimension 7: 50
- Dimension 8: 97
- Dimension 9: 188 (Wynn)
- Dimension 10: 373
- Dimension 11: 732 (new lower bound)
- Dimension 12: 1439 (new lower bound)
- Dimension 13: 2854 (new lower bound)

