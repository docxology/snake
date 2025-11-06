# Utils Module API

The `utils` module provides utility functions including canonical form, export, and visualization.

## Canonical Form Functions

### `is_canonical(transition_sequence: List[int]) -> bool`

Check if transition sequence follows Kochut's canonical form.

**Parameters:**
- `transition_sequence` (List[int]): Transition sequence to check

**Returns:**
- `bool`: True if sequence is in canonical form

**Example:**
```python
from snake_in_box.utils import is_canonical
valid = is_canonical([0, 1, 2, 0, 1])  # Returns True
invalid = is_canonical([1, 0, 2])  # Returns False
```

### `get_legal_next_dimensions(transition_sequence: List[int]) -> List[int]`

Get legal next dimensions for canonical extension.

**Parameters:**
- `transition_sequence` (List[int]): Current transition sequence (may be empty)

**Returns:**
- `List[int]`: List of legal next dimension values

**Example:**
```python
from snake_in_box.utils import get_legal_next_dimensions
legal = get_legal_next_dimensions([0, 1, 2])  # Returns [0, 1, 2, 3]
```

## Export Functions

### `export_snake(snake_node: SnakeNode, filename: str, include_vertices: bool = True) -> None`

Export snake to multiple formats (JSON, text, CSV).

**Parameters:**
- `snake_node` (SnakeNode): Snake node to export
- `filename` (str): Base filename (without extension)
- `include_vertices` (bool, optional): Include vertex sequence in JSON (default: True)

**Formats:**
- JSON: `{filename}.json` - Full metadata
- Text: `{filename}.txt` - Hex string format
- CSV: `{filename}_comma.txt` - Comma-separated transitions

**Example:**
```python
from snake_in_box.utils import export_snake
export_snake(result, "snake_7d")
# Creates: snake_7d.json, snake_7d.txt, snake_7d_comma.txt
```

### `export_analysis_data(results: Dict[int, Dict], output_dir: str = "output/data", include_sequences: bool = True) -> Dict[str, str]`

Export comprehensive analysis data in multiple formats (JSON, CSV, statistics).

**Parameters:**
- `results` (Dict[int, Dict]): Analysis results dictionary mapping dimension to result data
- `output_dir` (str, optional): Output directory (default: "output/data")
- `include_sequences` (bool, optional): Include transition sequences in exports (default: True)

**Returns:**
- `Dict[str, str]`: Dictionary mapping format name to file path

**Formats:**
- JSON: `analysis_results_comprehensive.json` - Full metadata and results
- CSV: `analysis_summary.csv` - Tabular summary
- Statistics: `statistics.json` - Aggregated statistics

**Example:**
```python
from snake_in_box.utils import export_analysis_data
from snake_in_box.analysis import analyze_dimensions

results = analyze_dimensions([1, 2, 3, 4, 5])
exported = export_analysis_data(results, output_dir="output/data")
# Creates: analysis_results_comprehensive.json, analysis_summary.csv, statistics.json
```

## Visualization Functions

### `visualize_snake_3d(snake_node: SnakeNode, show_hypercube: bool = True) -> None`

3D visualization for dimension 3 only.

**Parameters:**
- `snake_node` (SnakeNode): Snake node to visualize
- `show_hypercube` (bool, optional): Show hypercube edges (default: True)

**Example:**
```python
from snake_in_box.utils import visualize_snake_3d
visualize_snake_3d(result)
```

### `visualize_snake_auto(snake_node: SnakeNode, show_plot: bool = True) -> Optional[matplotlib.Figure]`

Automatically choose appropriate visualization method based on dimension.

**Parameters:**
- `snake_node` (SnakeNode): Snake node to visualize
- `show_plot` (bool, optional): Show plot immediately (default: True)

**Returns:**
- `Optional[matplotlib.Figure]`: Figure object or None

**Example:**
```python
from snake_in_box import visualize_snake_auto
fig = visualize_snake_auto(result, show_plot=True)
```

### `generate_16d_panel(snake_nodes: Dict[int, SnakeNode], output_file: Optional[str] = None, figsize: Tuple[int, int] = (20, 20), dpi: int = 300) -> Optional[matplotlib.Figure]`

Generate 4x4 panel graphical abstract for dimensions 1-16.

**Parameters:**
- `snake_nodes` (Dict[int, SnakeNode]): Dictionary mapping dimension to snake
- `output_file` (Optional[str]): File to save figure (default: None)
- `figsize` (Tuple[int, int]): Figure size (default: (20, 20))
- `dpi` (int): Resolution (default: 300)

**Returns:**
- `Optional[matplotlib.Figure]`: Figure object or None

**Example:**
```python
from snake_in_box import generate_16d_panel
snake_nodes = {1: node1, 2: node2, ..., 16: node16}
generate_16d_panel(snake_nodes, output_file="abstract.png")
```

### `visualize_snake_heatmap(snake_node: SnakeNode, show_plot: bool = True) -> Optional[matplotlib.Figure]`

Visualize snake as heatmap showing bit patterns across vertices.

**Parameters:**
- `snake_node` (SnakeNode): Snake node to visualize
- `show_plot` (bool, optional): Show plot immediately (default: True)

**Returns:**
- `Optional[matplotlib.Figure]`: Figure object

**Example:**
```python
from snake_in_box.utils import visualize_snake_heatmap
fig = visualize_snake_heatmap(result, show_plot=True)
```

### `visualize_snake_3d_projection(snake_node: SnakeNode, show_plot: bool = True) -> Optional[matplotlib.Figure]`

Visualize high-dimensional snake using 3D PCA projection (for dimensions >= 4).

**Parameters:**
- `snake_node` (SnakeNode): Snake node to visualize (dimension >= 4)
- `show_plot` (bool, optional): Show plot immediately (default: True)

**Returns:**
- `Optional[matplotlib.Figure]`: Figure object

**Example:**
```python
from snake_in_box.utils import visualize_snake_3d_projection
fig = visualize_snake_3d_projection(result, show_plot=True)
```

### `visualize_snake_transition_matrix(snake_node: SnakeNode, show_plot: bool = True) -> Optional[matplotlib.Figure]`

Visualize transition sequence as matrix showing dimension usage over time.

**Parameters:**
- `snake_node` (SnakeNode): Snake node to visualize
- `show_plot` (bool, optional): Show plot immediately (default: True)

**Returns:**
- `Optional[matplotlib.Figure]`: Figure object

**Example:**
```python
from snake_in_box.utils import visualize_snake_transition_matrix
fig = visualize_snake_transition_matrix(result, show_plot=True)
```

## Performance Plotting Functions

### `plot_computation_time_vs_dimension(...)`

Plot computation time vs dimension.

### `plot_exponential_fit(...)`

Plot exponential fit to computation times.

### `plot_slowdown_analysis(...)`

Plot slowdown analysis.

### `plot_memory_vs_dimension(...)`

Plot memory usage vs dimension.

## Related Documentation

- [Canonical Form](../algorithm/canonical-form.md) - Canonical form explanation
- [Visualization Guide](../guides/visualization.md) - Visualization guide
- [Utils Module AGENTS](../../snake_in_box/utils/AGENTS.md) - Module documentation

