# Hypercube Graphs

This document covers the mathematical foundations of hypercube graphs.

## Definition

An **n-dimensional hypercube graph** Q_n is a regular graph with:
- **2^n vertices**, each represented by a unique n-bit binary string
- **n·2^(n-1) edges** connecting vertices that differ in exactly one bit
- **Regular graph**: Each vertex has degree n
- **Distance metric**: Hamming distance (number of differing bits)

## Properties

### Vertex Representation

Vertices are labeled with binary numbers from 0 to 2^n - 1:
- Dimension 1: 0, 1
- Dimension 2: 00, 01, 10, 11 (or 0, 1, 2, 3)
- Dimension 3: 000, 001, 010, 011, 100, 101, 110, 111 (or 0-7)

### Edge Structure

An edge exists between two vertices if and only if their binary labels differ in exactly one bit position.

### Hamming Distance

The **Hamming distance** between two vertices is the number of bit positions where they differ:
- `hamming_distance(0b000, 0b001) = 1`
- `hamming_distance(0b000, 0b111) = 3`
- `hamming_distance(0b010, 0b101) = 3`

### Graph Properties

- **Bipartite**: Yes (can be 2-colored)
- **Connected**: Yes
- **Regular**: All vertices have degree n
- **Symmetric**: Highly symmetric under rotations and reflections

## Examples

### 1-Dimensional Hypercube (Line)

```
0 ---- 1
```

2 vertices, 1 edge

### 2-Dimensional Hypercube (Square)

```
10 ---- 11
 |       |
 |       |
00 ---- 01
```

4 vertices, 4 edges

### 3-Dimensional Hypercube (Cube)

```
    110 ---- 111
    /|       /|
   / |      / |
010 ---- 011  |
  |  100 --|- 101
  | /      | /
  |/       |/
000 ---- 001
```

8 vertices, 12 edges

## Growth Characteristics

As dimension increases:
- **Vertices**: 2^n (exponential)
- **Edges**: n·2^(n-1) (exponential)
- **Diameter**: n (maximum distance between any two vertices)
- **Average distance**: Approximately n/2

## Applications

Hypercube graphs have applications in:
- **Coding theory**: Error-correcting codes
- **Parallel computing**: Interconnection networks
- **Combinatorial optimization**: Various graph problems
- **Snake-in-the-Box**: Finding long induced paths

## Related Documentation

- [Snake Constraints](snake-constraints.md) - Snake-in-the-box constraints
- [Hamming Distance](hamming-distance.md) - Hamming distance properties
- [Complexity Analysis](complexity-analysis.md) - Computational complexity

