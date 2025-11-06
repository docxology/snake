# Snake-in-the-Box

A Python implementation of the N-dimensional snake-in-the-box algorithm based on the heuristically-pruned breadth-first search method from Ace (2025).

## Overview

The Snake-in-the-Box problem is the challenge of finding the longest possible induced path in the edge graph of an n-dimensional hypercube. This package implements the algorithm that discovered new lower bounds of 732, 1439, and 2854 in 11, 12, and 13 dimensions, respectively.

**Reference:** Ace, Thomas E. "New Lower Bounds for Snake-in-the-Box in 11-, 12-, and 13-dimensional Hypercubes." (2025) doi:10.5281/zenodo.17538015

## Installation

### From Source

```bash
git clone https://github.com/yourusername/snake.git
cd snake
pip install -e .
```

### Dependencies

Core dependencies:
- Python 3.8+
- numpy >= 1.20.0

Optional dependencies:
- matplotlib >= 3.3.0 (for visualization)
- memory-profiler >= 0.60.0 (for profiling)
- pytest >= 7.0.0 (for testing)

Install with optional dependencies:
```bash
pip install -e ".[dev]"
```

## Quick Start

### Basic Search

```python
from snake_in_box import pruned_bfs_search, export_snake

# Search for snake in 7-dimensional hypercube
result = pruned_bfs_search(dimension=7, memory_limit_gb=2.0)

if result:
    print(f"Found snake of length {result.get_length()}")
    export_snake(result, "snake_7d")
```

### Using Known Snakes

```python
from snake_in_box import get_known_snake, get_known_record
from snake_in_box.benchmarks import validate_known_snake

# Get known record for dimension 13
record = get_known_record(13)  # Returns 2854

# Get the actual snake sequence
snake_13d = get_known_snake(13)

# Validate it
is_valid, msg = validate_known_snake(13)
print(f"Valid: {is_valid}")
```

### Priming Strategy

```python
from snake_in_box import prime_search, get_known_snake

# Extend 9D snake to 10D
snake_9d = get_known_snake(9)
snake_10d = prime_search(snake_9d, target_dimension=10)
```

### Visualization

```python
from snake_in_box import pruned_bfs_search, visualize_snake_3d

# For 3D only
result = pruned_bfs_search(dimension=3)
if result:
    visualize_snake_3d(result)
```

## Mathematical Foundations

### Hypercube Graph Structure

An n-dimensional hypercube graph Q_n has:
- **2^n vertices**, each represented by a unique n-bit binary string
- **n·2^(n-1) edges** connecting vertices that differ in exactly one bit
- **Regular graph**: Each vertex has degree n
- **Distance metric**: Hamming distance (number of differing bits)

### Induced Path Constraints

A valid snake must satisfy:
1. **Consecutive vertices** differ by exactly one bit (Hamming distance = 1)
2. **Non-consecutive vertices** differ by more than one bit (Hamming distance > 1)

This constraint distinguishes snake-in-the-box from simpler longest path problems.

### Canonical Form

Kochut's canonical form reduces the search space by eliminating symmetric solutions:
- First transition must be 0
- Each subsequent transition must be ≤ max_dimension_used + 1

## Package Structure

```
snake_in_box/
├── core/              # Core data structures
│   ├── hypercube.py   # HypercubeBitmap class
│   ├── snake_node.py   # SnakeNode class
│   ├── transitions.py  # Conversion utilities
│   └── validation.py   # Validation functions
├── search/            # Search algorithms
│   ├── bfs_pruned.py   # Main pruned BFS
│   ├── fitness.py      # Fitness evaluators
│   ├── priming.py      # Priming strategies
│   └── parallel.py     # Parallel search
├── utils/             # Utilities
│   ├── canonical.py   # Canonical form
│   ├── export.py       # Export functions
│   └── visualize.py    # Visualization
├── benchmarks/        # Benchmarks
│   ├── known_snakes.py # Known records
│   └── performance.py  # Profiling tools
└── analysis/          # Analysis and reporting
    ├── analyze_dimensions.py  # Dimension analysis
    ├── reporting.py   # Report generation
    └── dimension_feasibility.py  # Feasibility analysis
```

## API Reference

### Core Functions

#### `pruned_bfs_search(dimension, memory_limit_gb=18.0, verbose=True)`

Execute heuristically-pruned breadth-first search.

**Parameters:**
- `dimension` (int): Dimension of hypercube
- `memory_limit_gb` (float): Maximum memory in gigabytes
- `verbose` (bool): Print progress information

**Returns:** `SnakeNode` or `None`

**Example:**
```python
from snake_in_box import pruned_bfs_search
result = pruned_bfs_search(dimension=7, memory_limit_gb=2.0)
if result:
    print(f"Found snake of length {result.get_length()}")
```

#### `validate_snake(vertex_sequence)`

Validate that a vertex sequence represents a valid snake.

**Parameters:**
- `vertex_sequence` (List[int]): List of vertex labels

**Returns:** `(bool, str)` - (is_valid, error_message)

**Example:**
```python
from snake_in_box import validate_snake
is_valid, msg = validate_snake([0, 1, 3, 7, 6])
```

#### `transition_to_vertex(transition_sequence, dimension, start_vertex=0)`

Convert transition sequence to vertex sequence.

**Parameters:**
- `transition_sequence` (List[int]): Sequence of bit positions
- `dimension` (int): Dimension of hypercube
- `start_vertex` (int): Starting vertex (default: 0)

**Returns:** `List[int]` - Vertex sequence

**Example:**
```python
from snake_in_box import transition_to_vertex
vertices = transition_to_vertex([0, 1, 2, 0], 3)  # Returns [0, 1, 3, 7, 6]
```

### Analysis Functions

#### `analyze_dimensions(dimensions, use_known=True, memory_limit_gb=2.0, verbose=False)`

Analyze multiple dimensions and generate comprehensive results.

**Parameters:**
- `dimensions` (List[int]): List of dimensions to analyze
- `use_known` (bool): Use known snakes if available
- `memory_limit_gb` (float): Memory limit for search
- `verbose` (bool): Print progress

**Returns:** `Dict[int, Dict]` - Analysis results

**Example:**
```python
from snake_in_box import analyze_dimensions
results = analyze_dimensions([1, 2, 3, 4, 5])
```

#### `generate_analysis_report(results, output_file="analysis_report.md", format="markdown")`

Generate comprehensive analysis report.

**Parameters:**
- `results` (Dict[int, Dict]): Analysis results
- `output_file` (str): Output file path
- `format` (str): 'markdown' or 'html'

**Returns:** `str` - Report content

#### `export_analysis_data(results, output_dir="output/data", include_sequences=True)`

Export comprehensive analysis data in multiple formats (JSON, CSV, statistics).

**Parameters:**
- `results` (Dict[int, Dict]): Analysis results
- `output_dir` (str): Output directory
- `include_sequences` (bool): Include transition sequences

**Returns:** `Dict[str, str]` - Dictionary mapping format to file path

**Example:**
```python
from snake_in_box.utils import export_analysis_data
from snake_in_box import analyze_dimensions

results = analyze_dimensions([1, 2, 3, 4, 5])
exported = export_analysis_data(results, output_dir="output/data")
# Creates: analysis_results_comprehensive.json, analysis_summary.csv, statistics.json
```

### Visualization Functions

#### `visualize_snake_auto(snake_node, show_plot=True)`

Automatically choose appropriate visualization method.

**Parameters:**
- `snake_node` (SnakeNode): Snake node to visualize
- `show_plot` (bool): Show plot immediately

**Returns:** `matplotlib.Figure` or `None`

**Example:**
```python
from snake_in_box import visualize_snake_auto
fig = visualize_snake_auto(result, show_plot=True)
```

#### `generate_16d_panel(snake_nodes, output_file=None, figsize=(20, 20), dpi=300)`

Generate 4x4 panel graphical abstract for dimensions 1-16.

**Parameters:**
- `snake_nodes` (Dict[int, SnakeNode]): Dictionary mapping dimension to snake
- `output_file` (str): File to save figure
- `figsize` (Tuple[int, int]): Figure size
- `dpi` (int): Resolution

**Returns:** `matplotlib.Figure` or `None`

**Example:**
```python
from snake_in_box import generate_16d_panel
snake_nodes = {1: node1, 2: node2, ...}  # For dimensions 1-16
generate_16d_panel(snake_nodes, output_file="abstract.png")
```

#### Additional Visualization Functions

Additional visualization methods are available from `snake_in_box.utils`:

- `visualize_snake_heatmap()` - Bit pattern heatmap
- `visualize_snake_3d_projection()` - 3D PCA projection for dimensions >= 4
- `visualize_snake_transition_matrix()` - Transition sequence matrix

**Example:**
```python
from snake_in_box.utils import visualize_snake_heatmap, visualize_snake_3d_projection

# Heatmap visualization
visualize_snake_heatmap(result, show_plot=True)

# 3D projection for high dimensions
visualize_snake_3d_projection(result, show_plot=True)
```

### Known Records

The package includes known record snakes from the literature:

| Dimension | Record Length | Source |
|-----------|---------------|--------|
| 3 | 4 | Optimal |
| 7 | 50 | Ace (2025) |
| 8 | 97 | Ace (2025) |
| 9 | 188 | Wynn (2012) |
| 10 | 373 | Ace (2025) |
| 11 | 732 | Ace (2025) - new lower bound |
| 12 | 1439 | Ace (2025) - new lower bound |
| 13 | 2854 | Ace (2025) - new lower bound |

## Algorithm Details

### Heuristically-Pruned Breadth-First Search

The algorithm performs level-by-level expansion of a search tree:
1. Start with empty snake at origin
2. Generate all valid children for current level
3. Prune nodes when memory limit exceeded (by fitness)
4. Maintain only two levels in memory simultaneously
5. Track best snake found during search

### Fitness Function

The paper uses a simple fitness measure: count of unmarked (available) vertices. Despite its simplicity, this was sufficient for record-breaking results.

### Memory Management

- Uses bit arrays (`array.array('Q')`) for efficient vertex tracking
- Estimates memory usage before expansion
- Prunes nodes by fitness when memory limits are exceeded
- Explicitly frees previous level after expansion

### Priming Strategy

For high dimensions (9+), the algorithm extends known good snakes from lower dimensions. This makes search tractable for high-dimensional spaces.

## Examples

See the `examples/` directory for complete examples:
- `simple_search.py` - Basic search usage
- `primed_search.py` - Priming strategy
- `parallel_search.py` - Parallel processing

## Testing

Run the test suite:

```bash
pytest snake_in_box/tests/
```

Or run specific test modules:

```bash
pytest snake_in_box/tests/test_core/
pytest snake_in_box/tests/test_search/
```

## Performance

The original C++ implementation (from the paper) achieved:
- Dimension 10: 50 minutes on Intel i5-12600K, 18GB memory, 10 threads
- Dimension 13: 2 hours, 19GB memory

Python implementation performance will vary based on system and optimizations.

## Contributing

Contributions are welcome! Please ensure:
- Code follows PEP 8 style guidelines
- Tests are included for new features
- Documentation is updated
- All tests pass

## License

MIT License

## References

1. Ace, Thomas E. "New Lower Bounds for Snake-in-the-Box in 11-, 12-, and 13-dimensional Hypercubes." (2025) doi:10.5281/zenodo.17538015

2. Kautz, W. H. "Unit-distance error-checking codes." IRE Trans. Electronic Computers EC-7 (1958) 179–180.

3. Kochut, K. J. "Snake-In-The-Box codes for dimension 7." Journal of Combinatorial Mathematics and Combinatorial Computing 20 (1996) 175–185.

4. Wynn, E. "Constructing circuit codes by permuting initial sequences." arXiv:1201.1647v1 (2012).

## Acknowledgments

Thanks to Thomas E. Ace for the original algorithm and paper, and to all researchers who have contributed to the snake-in-the-box problem.
