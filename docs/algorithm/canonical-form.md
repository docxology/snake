# Canonical Form

Kochut's canonical form is a symmetry reduction technique that eliminates redundant solutions by requiring transition sequences to follow specific ordering rules.

## Problem: Symmetry Explosion

In a hypercube, many snakes are equivalent under symmetry transformations (rotations, reflections). For example, in 3 dimensions, there are 6 equivalent length-4 snakes starting from the origin, but they all represent the same snake shape.

Searching all symmetric variants is wasteful. Canonical form ensures we search only one representative from each equivalence class.

## Kochut's Canonical Form Rules

A transition sequence is in canonical form if:

1. **First transition must be 0**: The first step from the origin must be in dimension 0
2. **Subsequent transitions**: Each subsequent transition must be ≤ max_dimension_used + 1

### Rule 1: First Transition

The first transition must be 0. This fixes the initial direction and eliminates rotational symmetry.

### Rule 2: Dimension Introduction

Each subsequent transition must either:
- Be one of the dimensions already used, OR
- Be exactly one more than the maximum dimension used so far

This ensures dimensions are introduced in ascending order.

## Examples

### Valid Canonical Sequences

```python
[0]              # Valid: starts with 0
[0, 1]           # Valid: 1 = max(0) + 1
[0, 1, 2]        # Valid: 2 = max(0,1) + 1
[0, 1, 0, 2]     # Valid: 0 and 1 already used, 2 = max(0,1) + 1
[0, 1, 2, 0, 1]  # Valid: all dimensions already used
```

### Invalid Sequences

```python
[1, 0, 2]        # Invalid: doesn't start with 0
[0, 1, 3]        # Invalid: 3 > max(0,1) + 1 = 2
[0, 2, 1]        # Invalid: 2 introduced before 1
```

## Implementation

### Checking Canonical Form

```python
def is_canonical(transition_sequence: List[int]) -> bool:
    """Check if transition sequence follows Kochut's canonical form."""
    if not transition_sequence:
        return True
    
    # First digit must be 0
    if transition_sequence[0] != 0:
        return False
    
    # Track maximum dimension used so far
    max_dimension = 0
    
    for dim in transition_sequence:
        # Each digit must be ≤ max_dimension + 1
        if dim > max_dimension + 1:
            return False
        
        # Update max_dimension if we've introduced a new dimension
        if dim == max_dimension + 1:
            max_dimension = dim
    
    return True
```

### Getting Legal Next Dimensions

```python
def get_legal_next_dimensions(transition_sequence: List[int]) -> List[int]:
    """Get legal next dimensions for canonical extension."""
    if not transition_sequence:
        return [0]  # First transition must be 0
    
    # Get maximum dimension used
    max_dim = max(transition_sequence)
    
    # Can use any previously used dimension or introduce max_dim + 1
    legal = list(set(transition_sequence))  # Unique previously used
    legal.append(max_dim + 1)  # Can introduce next dimension
    
    return sorted(legal)
```

## Search Space Reduction

Canonical form dramatically reduces the search space:

- **Without canonical form**: For dimension 3, there are 6 equivalent length-4 snakes
- **With canonical form**: Only 1 representative is searched

The reduction becomes more significant in higher dimensions where symmetry groups are larger.

## Integration with Search

The pruned BFS algorithm uses canonical form by:

1. **Initialization**: Start with empty sequence (canonical)
2. **Child Generation**: Only generate children using `get_legal_next_dimensions()`
3. **Validation**: Ensure all generated sequences are canonical

This ensures the entire search tree contains only canonical sequences.

## Mathematical Justification

Kochut's canonical form is based on the observation that:
- Hypercube symmetries can map any snake to one starting with transition 0
- Dimensions can be relabeled to introduce them in ascending order
- This mapping preserves snake length and validity

Therefore, searching only canonical sequences is complete (no loss of optimality) while being more efficient.

## References

Kochut, K. J. "Snake-In-The-Box codes for dimension 7." Journal of Combinatorial Mathematics and Combinatorial Computing 20 (1996) 175–185.

## Related Documentation

- [Algorithm Overview](overview.md) - Algorithm overview
- [Pruned BFS Algorithm](pruned-bfs.md) - Search algorithm
- [Search Tree Diagram](../diagrams/search-tree.md) - Visual representation

