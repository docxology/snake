# Snake Constraints

This document formalizes the constraints that define a valid snake-in-the-box.

## Definition

A **snake** in an n-dimensional hypercube is an **induced path** P = (v_0, v_1, ..., v_k) such that:

1. **Consecutive vertices** are adjacent: Hamming distance = 1
2. **Non-consecutive vertices** are not adjacent: Hamming distance > 1

## Constraint 1: Consecutive Adjacency

For all i ∈ {0, 1, ..., k-1}:
```
hamming_distance(v_i, v_{i+1}) = 1
```

This means consecutive vertices in the path must differ in exactly one bit position.

### Example

Valid consecutive pairs:
- (0b000, 0b001): Hamming distance = 1 ✓
- (0b001, 0b011): Hamming distance = 1 ✓
- (0b011, 0b111): Hamming distance = 1 ✓

Invalid consecutive pairs:
- (0b000, 0b011): Hamming distance = 2 ✗
- (0b000, 0b111): Hamming distance = 3 ✗

## Constraint 2: Non-Consecutive Non-Adjacency

For all i, j such that |i - j| > 1:
```
hamming_distance(v_i, v_j) > 1
```

This means non-consecutive vertices must differ in more than one bit position.

### Example

Valid non-consecutive pairs:
- (0b000, 0b011): Hamming distance = 2 > 1 ✓
- (0b000, 0b111): Hamming distance = 3 > 1 ✓

Invalid non-consecutive pairs:
- (0b000, 0b001): Hamming distance = 1, but not consecutive ✗

## Induced Path Property

The "induced path" property means:
- The path uses only edges that exist in the hypercube
- No "shortcuts" between non-consecutive vertices
- The path is "tight" - no vertex can be skipped

## Validation Algorithm

To validate a snake:

```python
def validate_snake(vertex_sequence):
    n = len(vertex_sequence)
    
    # Check consecutive pairs
    for i in range(n - 1):
        if hamming_distance(vertex_sequence[i], vertex_sequence[i+1]) != 1:
            return False, f"Consecutive vertices {i} and {i+1} not adjacent"
    
    # Check non-consecutive pairs
    for i in range(n):
        for j in range(i + 2, n):
            if hamming_distance(vertex_sequence[i], vertex_sequence[j]) <= 1:
                return False, f"Non-consecutive vertices {i} and {j} too close"
    
    return True, "Valid snake"
```

## Transition Sequence Representation

Instead of vertex sequences, we often use **transition sequences**:
- Each transition indicates which bit to flip
- Transition sequence [0, 1, 2] means: flip bit 0, then bit 1, then bit 2
- Starting from vertex 0: 0 → 1 → 3 → 7

## Prohibited Vertices

When building a snake, certain vertices become **prohibited**:
- Vertices already in the snake path
- Vertices adjacent to vertices in the snake path

This ensures the induced path constraint is maintained.

## Maximum Length

The Snake-in-the-Box problem seeks the **maximum length** snake in Q_n.

Known results:
- Dimension 3: Maximum length = 4 (optimal)
- Dimension 4: Maximum length = 7 (optimal)
- Dimension 5: Maximum length = 13 (optimal)
- Dimension 6: Maximum length = 26 (optimal)
- Dimension 7: Known lower bound = 50
- Dimension 8: Known lower bound = 97
- Dimension 9: Known lower bound = 188
- Dimension 10: Known lower bound = 373
- Dimension 11: Known lower bound = 732
- Dimension 12: Known lower bound = 1439
- Dimension 13: Known lower bound = 2854

## Related Documentation

- [Hypercube Graphs](hypercube-graphs.md) - Hypercube properties
- [Hamming Distance](hamming-distance.md) - Hamming distance details
- [Complexity Analysis](complexity-analysis.md) - Computational complexity

