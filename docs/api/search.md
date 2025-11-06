# Search Module API

The `search` module implements the heuristically-pruned breadth-first search algorithm and related search strategies.

## Functions

### `pruned_bfs_search(dimension: int, memory_limit_gb: float = 18.0, verbose: bool = True) -> Optional[SnakeNode]`

Execute heuristically-pruned breadth-first search for snake-in-the-box.

This implements the algorithm from Ace (2025) that discovered record-breaking snakes in dimensions 11-13.

**Parameters:**
- `dimension` (int): Dimension of hypercube to search (n in Q_n)
- `memory_limit_gb` (float, optional): Maximum memory usage in gigabytes (default: 18.0)
- `verbose` (bool, optional): Print progress information (default: True)

**Returns:**
- `Optional[SnakeNode]`: Best snake found, or None if search fails

**Example:**
```python
from snake_in_box import pruned_bfs_search
result = pruned_bfs_search(dimension=7, memory_limit_gb=2.0)
if result:
    print(f"Found snake of length {result.get_length()}")
```

### `prime_search(lower_dimension_snake: List[int], target_dimension: int, memory_limit_gb: float = 18.0, verbose: bool = True) -> Optional[List[int]]`

Extend a snake from dimension n to dimension n+1 or higher using priming strategy.

**Parameters:**
- `lower_dimension_snake` (List[int]): Known good snake transition sequence in lower dimension
- `target_dimension` (int): Target dimension to extend to
- `memory_limit_gb` (float, optional): Maximum memory in gigabytes (default: 18.0)
- `verbose` (bool, optional): Print progress (default: True)

**Returns:**
- `Optional[List[int]]`: Extended snake transition sequence, or None if search fails

**Example:**
```python
from snake_in_box import prime_search, get_known_snake
snake_9d = get_known_snake(9)
snake_10d = prime_search(snake_9d, target_dimension=10)
```

### `pruned_bfs_search_from_seed(seed_node: SnakeNode, dimension: int, memory_limit_gb: float = 18.0, max_levels: int = 10000, verbose: bool = True) -> Optional[SnakeNode]`

Modified BFS that starts from a seed snake instead of origin.

**Parameters:**
- `seed_node` (SnakeNode): Seed snake node to start from
- `dimension` (int): Target dimension
- `memory_limit_gb` (float, optional): Maximum memory in gigabytes (default: 18.0)
- `max_levels` (int, optional): Maximum levels to search (default: 10000)
- `verbose` (bool, optional): Print progress (default: True)

**Returns:**
- `Optional[SnakeNode]`: Best snake found, or None if search fails

### `detect_dimension(transition_sequence: List[int]) -> int`

Determine dimension from transition sequence.

The dimension is one more than the maximum transition value, since transitions are 0-indexed.

**Parameters:**
- `transition_sequence` (List[int]): Transition sequence

**Returns:**
- `int`: Detected dimension

**Example:**
```python
from snake_in_box.search import detect_dimension
dim = detect_dimension([0, 1, 2, 3])  # Returns 4
```

### `parallel_search(dimension: int, memory_limit_gb: float = 18.0, num_workers: int = 10, verbose: bool = True) -> Optional[SnakeNode]`

Parallel search using multiprocessing.

**Parameters:**
- `dimension` (int): Dimension of hypercube
- `memory_limit_gb` (float, optional): Maximum memory in gigabytes (default: 18.0)
- `num_workers` (int, optional): Number of worker processes (default: 10)
- `verbose` (bool, optional): Print progress (default: True)

**Returns:**
- `Optional[SnakeNode]`: Best snake found, or None if search fails

**Example:**
```python
from snake_in_box.search import parallel_search
result = parallel_search(dimension=7, num_workers=4)
```

## Classes

### `SimpleFitnessEvaluator`

Simple fitness evaluator using unmarked vertex count (paper's method).

```python
from snake_in_box.search import SimpleFitnessEvaluator

evaluator = SimpleFitnessEvaluator(node: SnakeNode)
fitness = evaluator.evaluate()
```

#### Methods

##### `evaluate() -> int`
Evaluate fitness as count of unmarked vertices.

### `AdvancedFitnessEvaluator`

Advanced fitness evaluator with multiple measures.

```python
from snake_in_box.search import AdvancedFitnessEvaluator

evaluator = AdvancedFitnessEvaluator(node: SnakeNode)
```

#### Methods

##### `count_unmarked_vertices() -> int`
Count unmarked vertices (original simple fitness).

##### `count_dead_ends() -> int`
Count unmarked vertices with only one unmarked neighbor.

##### `count_unreachable_vertices() -> int`
Count vertices unreachable from current position.

##### `combined_fitness(weights: Dict[str, float] = None) -> float`
Weighted combination of multiple fitness measures.

**Parameters:**
- `weights` (Dict[str, float], optional): Weights for each measure. Default: `{'unmarked': 1.0, 'dead_ends': -0.5}`

**Returns:**
- `float`: Combined fitness score

**Example:**
```python
evaluator = AdvancedFitnessEvaluator(node)
fitness = evaluator.combined_fitness({
    'unmarked': 1.0,
    'dead_ends': -0.5,
    'unreachable': -0.3
})
```

## Related Documentation

- [Pruned BFS Algorithm](../algorithm/pruned-bfs.md) - Detailed algorithm description
- [Priming Strategy](../algorithm/priming-strategy.md) - Priming strategy
- [Fitness Evaluation](../algorithm/fitness-evaluation.md) - Fitness functions
- [Search Module AGENTS](../../snake_in_box/search/AGENTS.md) - Module documentation

