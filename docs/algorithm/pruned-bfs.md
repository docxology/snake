# Pruned BFS Algorithm

This document describes the heuristically-pruned breadth-first search algorithm in detail, as implemented in the Snake-in-the-Box package.

## Algorithm Description

The pruned BFS algorithm performs level-by-level expansion of a search tree, pruning nodes when memory constraints are exceeded based on a fitness heuristic.

## Step-by-Step Algorithm

### Initialization

```python
current_level = [SnakeNode([], dimension)]  # Start with empty snake at origin
best_snake = None
max_length = 0
level_count = 0
```

### Main Loop

For each level in the search tree:

1. **Generate Children**: For each node in current level:
   - Get legal next dimensions (canonical form)
   - For each legal dimension:
     - Check if extension is valid (next vertex not marked)
     - If valid, create child node
     - Track best snake found

2. **Prune if Needed**: If estimated memory usage exceeds limit:
   - Sort nodes by fitness (unmarked vertex count)
   - Keep top nodes within memory limit
   - Discard lower-fitness nodes

3. **Memory Management**: 
   - Free previous level from memory
   - Move to next level

4. **Termination**: Stop when no more nodes to expand

## Key Functions

### Node Extension

```python
def is_valid_extension(node: SnakeNode, new_dimension: int) -> bool:
    """Check if snake can be extended with given dimension."""
    return node.can_extend(new_dimension)
```

### Pruning

```python
def prune_by_fitness(nodes: List[SnakeNode], memory_limit_gb: float) -> List[SnakeNode]:
    """Prune nodes by fitness to fit within memory limit."""
    # Sort by fitness descending
    nodes.sort(key=lambda n: n.fitness, reverse=True)
    
    # Calculate max nodes that fit in memory
    bytes_per_node = estimate_node_size(nodes[0])
    max_nodes = int((memory_limit_gb * 1024**3) / bytes_per_node)
    
    # Keep top nodes
    return nodes[:max_nodes]
```

### Memory Estimation

```python
def estimate_memory_usage(nodes: List[SnakeNode]) -> float:
    """Estimate memory usage for a list of nodes."""
    if not nodes:
        return 0.0
    
    bytes_per_node = estimate_node_size(nodes[0])
    total_bytes = len(nodes) * bytes_per_node
    return total_bytes / (1024**3)  # Convert to GB
```

## Memory Management

The algorithm maintains only **two levels** in memory at any time:
- Current level (being expanded)
- Next level (children being generated)

After generating all children, the previous level is explicitly freed:

```python
del current_level  # Free memory
current_level = next_level
```

## Pruning Strategy

When memory limit is exceeded:

1. **Estimate**: Calculate how many nodes fit in memory
2. **Sort**: Sort nodes by fitness (unmarked vertex count) descending
3. **Select**: Keep top nodes within memory limit
4. **Discard**: Remove lower-fitness nodes

This heuristic assumes nodes with more unmarked vertices are more likely to lead to longer snakes.

## Fitness Function

The default fitness function is simple but effective:

```python
fitness = count_unmarked_vertices()
```

Despite its simplicity, this was sufficient for record-breaking results in dimensions 11-13.

## Algorithm Pseudocode

```
function PRUNED_BFS(dimension, memory_limit):
    current_level = [empty_snake]
    best_snake = None
    max_length = 0
    
    while current_level is not empty:
        next_level = []
        
        // Generate children
        for each node in current_level:
            for each legal_dimension:
                if can_extend(node, legal_dimension):
                    child = create_child(node, legal_dimension)
                    next_level.append(child)
                    
                    if child.length > max_length:
                        max_length = child.length
                        best_snake = child
        
        // Prune if needed
        if estimate_memory(next_level) > memory_limit:
            next_level = prune_by_fitness(next_level, memory_limit)
        
        // Move to next level
        free(current_level)
        current_level = next_level
    
    return best_snake
```

## Performance Characteristics

- **Time**: Exponential in worst case, pruned by heuristics
- **Memory**: O(beam_width × node_size) where beam_width is determined by memory limits
- **Space**: O(2^n) for n-dimensional hypercube bitmap per node

## Implementation Details

See the actual implementation in `snake_in_box/search/bfs_pruned.py`.

## Related Documentation

- [Algorithm Overview](overview.md) - High-level overview
- [Fitness Evaluation](fitness-evaluation.md) - Fitness functions
- [Canonical Form](canonical-form.md) - Symmetry reduction
- [Memory Management](../architecture/memory-management.md) - Memory optimization
- [Algorithm Flow Diagram](../diagrams/algorithm-flow.md) - Visual flowchart

