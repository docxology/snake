# Complexity Analysis

This document analyzes the computational complexity of the Snake-in-the-Box problem and the pruned BFS algorithm.

## Problem Complexity

The Snake-in-the-Box problem is **NP-hard**, meaning:
- No known polynomial-time algorithm exists
- Exact solutions require exponential time in worst case
- Heuristic approaches are necessary for high dimensions

## Search Space Size

### Total Possible Snakes

For an n-dimensional hypercube:
- **Vertices**: 2^n
- **Possible paths**: Exponential in length
- **Search space**: Super-exponential

### With Canonical Form

Canonical form reduces search space by eliminating symmetric solutions:
- **Reduction factor**: Approximately n! (factorial of dimension)
- **Still exponential**: But significantly smaller

## Algorithm Complexity

### Time Complexity

**Worst case**: O(b^d) where:
- b = branching factor (average children per node)
- d = depth (snake length)

**With pruning**: O(beam_width × d) where:
- beam_width = number of nodes kept per level (determined by memory)

**Typical performance** (from paper):
- Dimension 10: 50 minutes
- Dimension 13: 2 hours

### Space Complexity

**Per node**: O(2^n) for n-dimensional hypercube bitmap

**Total memory**: O(beam_width × 2^n) where:
- beam_width = number of nodes kept per level

**Typical memory** (from paper):
- Dimension 10: 18GB
- Dimension 13: 19GB

## Growth Characteristics

### Exponential Growth

As dimension increases:
- **Vertices**: 2^n (exponential)
- **Memory per node**: O(2^n) (exponential)
- **Search space**: Super-exponential
- **Computation time**: Exponential (with pruning)

### Dimension Scaling

| Dimension | Vertices | Memory/Node | Typical Time |
|-----------|----------|-------------|--------------|
| 7 | 128 | ~2KB | Seconds |
| 8 | 256 | ~4KB | Minutes |
| 9 | 512 | ~8KB | Minutes |
| 10 | 1,024 | ~16KB | 50 min |
| 11 | 2,048 | ~32KB | Hours |
| 12 | 4,096 | ~64KB | Hours |
| 13 | 8,192 | ~128KB | 2 hours |

## Pruning Impact

Pruning reduces both time and space:
- **Time**: Reduces nodes explored
- **Space**: Limits memory usage
- **Quality**: May miss optimal solutions (heuristic)

## Priming Impact

Priming significantly reduces search time:
- **Without priming**: Search from empty snake (very slow)
- **With priming**: Start from known good snake (much faster)
- **Speedup**: Orders of magnitude for high dimensions

## Parallel Processing

Parallel search provides linear speedup (up to number of cores):
- **10 workers**: ~10x speedup (theoretical)
- **Practical**: Less due to overhead and memory contention

## Feasibility Limits

### Current Feasibility

- **Dimensions 1-9**: Feasible with standard hardware
- **Dimensions 10-13**: Feasible with high-memory systems and priming
- **Dimensions 14+**: Challenging, requires specialized approaches

### Memory Limits

For dimension n:
- **Bitmap per node**: 2^n bits = 2^n / 8 bytes
- **With 1M nodes**: ~2^n / 8 × 10^6 bytes
- **Dimension 16**: ~2^16 / 8 × 10^6 = ~8GB per million nodes

### Time Limits

Extrapolating from paper:
- **Dimension 14**: ~4-8 hours (estimated)
- **Dimension 15**: ~16-32 hours (estimated)
- **Dimension 16**: ~64-128 hours (estimated)

## Optimization Strategies

1. **Canonical form**: Reduces search space
2. **Pruning**: Limits memory and time
3. **Priming**: Starts from good solutions
4. **Parallel processing**: Utilizes multiple cores
5. **Memory management**: Only keeps two levels

## Related Documentation

- [Memory Management](../architecture/memory-management.md) - Memory optimization
- [Performance Tuning](../guides/performance-tuning.md) - Performance tips
- [Pruned BFS Algorithm](../algorithm/pruned-bfs.md) - Algorithm details

