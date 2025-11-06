# Fitness Evaluation

Fitness evaluation determines which nodes to keep when pruning the search tree. The package provides both simple and advanced fitness evaluators.

## Simple Fitness Evaluator

The **SimpleFitnessEvaluator** uses the unmarked vertex count, which was sufficient for record-breaking results in dimensions 11-13.

### Implementation

```python
class SimpleFitnessEvaluator:
    """Simple fitness evaluator using unmarked vertex count."""
    
    def evaluate(self) -> int:
        """Evaluate fitness as count of unmarked vertices."""
        return self.node.fitness
```

### Why It Works

Despite its simplicity, counting unmarked vertices is effective because:
- **More unmarked vertices** = more potential for extension
- **Simple to compute** = fast evaluation
- **Effective heuristic** = sufficient for good results

The paper notes: "Yet a simple count of remaining unmarked (zero-bit) vertices was sufficient to achieve the results presented here."

## Advanced Fitness Evaluator

The **AdvancedFitnessEvaluator** provides additional measures for experimentation:

### Available Measures

1. **Unmarked Vertices**: Count of available vertices (same as simple)
2. **Dead Ends**: Vertices with only one unmarked neighbor
3. **Unreachable Vertices**: Vertices unreachable from current position

### Implementation

```python
class AdvancedFitnessEvaluator:
    """Advanced fitness evaluator with multiple measures."""
    
    def count_unmarked_vertices(self) -> int:
        """Count unmarked vertices (original simple fitness)."""
        return self.node.fitness
    
    def count_dead_ends(self) -> int:
        """Count unmarked vertices with only one unmarked neighbor."""
        # ... implementation ...
    
    def count_unreachable_vertices(self) -> int:
        """Count vertices unreachable from current position."""
        # Uses flood fill (BFS) to find reachable vertices
        # ... implementation ...
    
    def combined_fitness(self, weights: Dict[str, float] = None) -> float:
        """Weighted combination of multiple fitness measures."""
        if weights is None:
            weights = {'unmarked': 1.0, 'dead_ends': -0.5}
        
        fitness = 0.0
        fitness += weights.get('unmarked', 0.0) * self.count_unmarked_vertices()
        fitness += weights.get('dead_ends', 0.0) * self.count_dead_ends()
        fitness += weights.get('unreachable', 0.0) * self.count_unreachable_vertices()
        
        return fitness
```

### Dead Ends

Dead ends are vertices with only one unmarked neighbor. They limit future growth because they can only be entered from one direction.

```python
def count_dead_ends(self) -> int:
    """Count unmarked vertices with only one unmarked neighbor."""
    dead_ends = 0
    
    for vertex in range(1 << self.dimension):
        if self.node._is_marked(vertex):
            continue
        
        # Count unmarked neighbors
        unmarked_neighbors = 0
        for dim in range(self.dimension):
            neighbor = vertex ^ (1 << dim)
            if not self.node._is_marked(neighbor):
                unmarked_neighbors += 1
        
        if unmarked_neighbors == 1:
            dead_ends += 1
    
    return dead_ends
```

### Unreachable Vertices

Unreachable vertices are unmarked but cannot be reached from the current snake position. They represent wasted potential.

```python
def count_unreachable_vertices(self) -> int:
    """Count vertices unreachable from current position."""
    current_vertex = compute_current_vertex(self.node.transition_sequence)
    reachable = self._flood_fill_reachable(current_vertex)
    total_unmarked = self.count_unmarked_vertices()
    return total_unmarked - len(reachable)
```

The flood fill uses BFS to find all reachable unmarked vertices from the current position.

## Combined Fitness

The advanced evaluator allows combining multiple measures with weights:

```python
evaluator = AdvancedFitnessEvaluator(node)
fitness = evaluator.combined_fitness({
    'unmarked': 1.0,      # Favor more unmarked vertices
    'dead_ends': -0.5,    # Penalize dead ends
    'unreachable': -0.3   # Penalize unreachable vertices
})
```

## Usage in Pruning

During pruning, nodes are sorted by fitness:

```python
# Sort by fitness descending
nodes.sort(key=lambda n: n.fitness, reverse=True)

# Keep top nodes within memory limit
return nodes[:max_nodes]
```

The default uses `SimpleFitnessEvaluator`, but you can customize the fitness function.

## Alternative Fitness Measures

Meyerson (2015) proposes additional measures:
- Unreachable vertices
- Dead ends
- Blind alleys

These can be implemented using the `AdvancedFitnessEvaluator` framework.

## References

- Ace, Thomas E. "New Lower Bounds for Snake-in-the-Box in 11-, 12-, and 13-dimensional Hypercubes." (2025)
- Meyerson, S. J. "Finding Longest Paths in Hypercubes: 11 New Lower Bounds for Snakes, Coils, and Symmetrical Coils." MSc Thesis, Athens, Georgia (2015)

## Related Documentation

- [Pruned BFS Algorithm](pruned-bfs.md) - How fitness is used in pruning
- [Algorithm Overview](overview.md) - Algorithm overview
- [Search Module API](../api/search.md) - API reference

