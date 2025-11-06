# Hamming Distance

This document covers Hamming distance properties and their role in the Snake-in-the-Box problem.

## Definition

The **Hamming distance** between two binary strings (or integers) is the number of positions where they differ.

For integers represented in binary:
```
hamming_distance(a, b) = popcount(a XOR b)
```

Where `popcount` counts the number of set bits.

## Properties

### Symmetry
```
hamming_distance(a, b) = hamming_distance(b, a)
```

### Triangle Inequality
```
hamming_distance(a, c) ≤ hamming_distance(a, b) + hamming_distance(b, c)
```

### Zero Distance
```
hamming_distance(a, a) = 0
```

## In Hypercube Graphs

In an n-dimensional hypercube:
- **Adjacent vertices**: Hamming distance = 1
- **Maximum distance**: Hamming distance = n (opposite corners)
- **Average distance**: Approximately n/2

## Snake Constraints

### Consecutive Vertices

For consecutive vertices in a snake:
```
hamming_distance(v_i, v_{i+1}) = 1
```

This ensures the path follows hypercube edges.

### Non-Consecutive Vertices

For non-consecutive vertices in a snake:
```
hamming_distance(v_i, v_j) > 1  (when |i - j| > 1)
```

This ensures the induced path property (no shortcuts).

## Computation

### Bitwise XOR Method

```python
def hamming_distance(a: int, b: int) -> int:
    """Calculate Hamming distance using XOR."""
    xor = a ^ b
    count = 0
    while xor:
        count += xor & 1
        xor >>= 1
    return count
```

### Built-in Method

```python
def hamming_distance(a: int, b: int) -> int:
    """Calculate Hamming distance using popcount."""
    return bin(a ^ b).count('1')
```

## Examples

```python
# Adjacent vertices (distance 1)
hamming_distance(0b000, 0b001)  # Returns 1
hamming_distance(0b001, 0b011)  # Returns 1

# Non-adjacent vertices (distance > 1)
hamming_distance(0b000, 0b011)  # Returns 2
hamming_distance(0b000, 0b111)  # Returns 3

# Same vertex (distance 0)
hamming_distance(0b000, 0b000)  # Returns 0
```

## Validation Use

Hamming distance is used extensively in snake validation:

1. **Check consecutive pairs**: Must have distance 1
2. **Check non-consecutive pairs**: Must have distance > 1
3. **Find adjacent vertices**: For marking prohibited vertices

## Related Documentation

- [Snake Constraints](snake-constraints.md) - Snake constraints
- [Hypercube Graphs](hypercube-graphs.md) - Hypercube properties
- [Core Module API](../api/core.md) - Implementation details

