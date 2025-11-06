# Feasibility Analysis: Dimensions 14-16 and Beyond

## Executive Summary

This report analyzes the computational feasibility of extending
snake-in-the-box search to dimensions 14-16 and beyond.

## Current Status

| Dimension | Status | Length | Method |
|-----------|--------|--------|--------|
| 1 | ❌ | - | Not available |
| 2 | ❌ | - | Not available |
| 3 | ✅ | 4 | Known (Literature) |
| 4 | ✅ | 7 | Known (Literature) |
| 5 | ✅ | 13 | Known (Literature) |
| 6 | ✅ | 26 | Known (Literature) |
| 7 | ✅ | 50 | Known (Literature) |
| 8 | ✅ | 97 | Known (Literature) |
| 9 | ✅ | 188 | Known (Ace 2025) |
| 10 | ✅ | 373 | Known (Ace 2025) |
| 11 | ✅ | 732 | Known (Ace 2025) |
| 12 | ✅ | 1439 | Known (Ace 2025) |
| 13 | ✅ | 2854 | Known (Ace 2025) |
| 14 | ❌ | - | Not available |
| 15 | ❌ | - | Not available |
| 16 | ❌ | - | Not available |

## Computational Complexity Analysis

| Dimension | Vertices | Bitmap (GB) | Est. Nodes | Est. Memory (GB) | Est. Time (hrs) | Feasible |
|-----------|----------|-------------|------------|------------------|------------------|----------|
| 10 | 1,024 | 0.0000 | 1.00e+07 | 2.12 | 0.83 | ✅ |
| 11 | 2,048 | 0.0000 | 2.56e+05 | 0.08 | 0.50 | ✅ |
| 12 | 4,096 | 0.0000 | 5.12e+05 | 0.29 | 1.00 | ✅ |
| 13 | 8,192 | 0.0000 | 1.02e+06 | 1.07 | 2.00 | ✅ |
| 14 | 16,384 | 0.0000 | 2.05e+06 | 4.10 | 5.00 | ✅ |
| 15 | 32,768 | 0.0000 | 4.10e+06 | 16.01 | 12.50 | ✅ |
| 16 | 65,536 | 0.0000 | 8.19e+06 | 63.26 | 31.25 | ✅ |

## Why Dimensions 14-16 Are Challenging

### 1. Exponential Growth

- **Vertices**: 2^n grows exponentially
  - Dimension 13: 8,192 vertices
  - Dimension 14: 16,384 vertices
  - Dimension 15: 32,768 vertices
  - Dimension 16: 65,536 vertices

- **Search Space**: Super-exponential growth
  - Number of possible paths grows combinatorially
  - Even with pruning, search space is enormous

### 2. Memory Requirements

- **Bitmap Storage**: O(2^n) bits per node
- **Node Count**: Exponential growth in search tree
- **Example**: Dimension 16 requires ~2GB bitmap per node
  - With 1 million nodes: 2TB memory
  - Even with pruning, memory becomes prohibitive

### 3. Computational Time

- **From Paper**: Dimension 13 took 2 hours with 19GB
- **Extrapolation**: Dimension 16 would take ~50-100 hours
- **With Pruning**: Still requires extensive computation

### 4. Search Tree Explosion

- **Branching Factor**: Decreases but still large
- **Depth**: Snake length grows with dimension
- **Total Nodes**: Exponential in both dimension and depth

## Strategies for Dimension 16

### Recommended Approach

- **Strategy**: incremental + priming + parallel
- **Optimized Memory**: 9.49 GB
- **Optimized Time**: 19.69 hours
- **Feasible**: ✅ Yes

### Strategy Details

#### Priming
- **Description**: Extend known snake from dimension 13
- **Feasible**: ✅

#### Parallel
- **Description**: Use 10+ parallel workers
- **Feasible**: ✅

#### Aggressive Pruning
- **Description**: More aggressive fitness-based pruning
- **Feasible**: ✅
- **Risk**: May miss optimal solutions

#### Incremental
- **Description**: Extend dimension by dimension (14->15->16)
- **Feasible**: ✅

## Why Not Beyond Dimension 16?

### Fundamental Limits

1. **Memory**: Even with aggressive pruning, memory requirements
   become prohibitive beyond dimension 16

2. **Time**: Computational time grows exponentially
   - Dimension 17: ~200-500 hours estimated
   - Dimension 18: ~1000+ hours estimated

3. **Search Space**: Combinatorial explosion makes exhaustive
   search impossible even with heuristics

4. **NP-Hardness**: Problem is fundamentally NP-hard
   - No polynomial-time algorithm exists
   - Heuristics become less effective at higher dimensions

### Alternative Approaches

For dimensions beyond 16, alternative approaches may be needed:

1. **Stochastic Methods**: Monte Carlo, genetic algorithms
2. **Approximation**: Accept suboptimal solutions
3. **Theoretical Bounds**: Focus on upper/lower bounds
4. **Specialized Hardware**: GPU acceleration, distributed computing

## Recommendations

### For Dimensions 14-16

1. ✅ **Use Incremental Priming**: Extend dimension by dimension
2. ✅ **Parallel Processing**: Use 10+ workers
3. ✅ **Aggressive Pruning**: Accept risk of suboptimal solutions
4. ✅ **High-Memory System**: 50-100GB RAM recommended
5. ✅ **Long Runtime**: Allow 50-100 hours per dimension

### For Dimensions Beyond 16

1. ⚠️ **Consider Alternative Algorithms**: Stochastic methods
2. ⚠️ **Focus on Bounds**: Upper/lower bounds rather than exact
3. ⚠️ **Specialized Hardware**: GPU clusters, distributed systems
4. ⚠️ **Theoretical Research**: New algorithmic approaches needed
