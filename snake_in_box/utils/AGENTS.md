# Utils Module: Agent Documentation

## Purpose

The `utils` module provides utility functions including canonical form utilities, export functions, and visualization tools for snakes of various dimensions.

## Canonical Form Utilities

### is_canonical(transition_sequence)

**Purpose**: Check if transition sequence follows Kochut's canonical form.

**Rules**:
1. First digit must be 0
2. Each subsequent digit ≤ max_dimension_used + 1

**Returns**: `bool`

**Usage**:
```python
from snake_in_box.utils import is_canonical
valid = is_canonical([0, 1, 2, 0, 1])  # True
invalid = is_canonical([1, 0, 2])  # False
```

### get_legal_next_dimensions(transition_sequence)

**Purpose**: Get legal next dimensions for canonical extension.

**Returns**: `List[int]` - Legal dimension values

**Usage**:
```python
from snake_in_box.utils import get_legal_next_dimensions
legal = get_legal_next_dimensions([0, 1, 2])  # [0, 1, 2, 3]
```

## Export Functions

### export_snake(snake_node, filename, include_vertices=True)

**Purpose**: Export snake to multiple formats.

**Formats**:
- JSON: Full metadata including transitions and vertices
- Text: Hex string format (paper format)
- CSV: Comma-separated transitions

**Usage**:
```python
from snake_in_box.utils import export_snake
export_snake(result, "snake_7d")
# Creates: snake_7d.json, snake_7d.txt, snake_7d_comma.txt
```

## Visualization Functions

### visualize_snake_3d(snake_node, show_hypercube=True)

**Purpose**: 3D visualization for dimension 3 only.

**Features**:
- Snake path in red
- Hypercube edges (optional)
- 3D plot with matplotlib

**Usage**:
```python
from snake_in_box.utils import visualize_snake_3d
visualize_snake_3d(result)
```

### Advanced Visualization (see visualize_advanced.py)

**Functions**:
- `visualize_snake_1d()`: Line plot for 1D
- `visualize_snake_2d()`: 2D grid plot
- `visualize_snake_3d_advanced()`: Enhanced 3D visualization
- `visualize_snake_nd()`: Projection methods for N>3
- `visualize_snake_auto()`: Automatically choose visualization method
- `visualize_snake_heatmap()`: Bit pattern heatmap visualization
- `visualize_snake_3d_projection()`: 3D PCA projection for dimensions >= 4
- `visualize_snake_transition_matrix()`: Transition sequence matrix visualization

**Projection Methods**:
- PCA: Principal component analysis
- Pairwise: Dimension pair projections
- Force-directed: Graph layout
- Unfolding: Hypercube unfolding

### Export Functions

**export_snake()**: Export individual snake to JSON, text, CSV formats

**export_analysis_data()**: Export comprehensive analysis data in multiple formats:
- JSON: Full metadata and results
- CSV: Tabular summary
- Statistics: Aggregated statistics

## Dependencies

- `core/`: SnakeNode, transitions
- `matplotlib`: For visualization (optional)
- `json`: For export (standard library)

## Visualization Strategies

### Low Dimensions (1-3)
- Direct visualization in native space
- 1D: Line plot
- 2D: Grid plot
- 3D: 3D scatter/line plot

### High Dimensions (4+)
- Projection to 2D/3D
- Multiple projection methods
- Interactive exploration
- Dimension pair grids

## Export Formats

### JSON Format
```json
{
  "dimension": 7,
  "length": 50,
  "transition_sequence": [0, 1, 2, ...],
  "vertex_sequence": [0, 1, 3, ...],
  "fitness": 1234
}
```

### Text Format
Hex string: `"0120314021..."` (paper format)

### CSV Format
Comma-separated: `"0,1,2,0,1,2,..."`

## Testing

See `tests/test_utils/`:
- `test_canonical.py`: Canonical form utilities
- `test_visualize_advanced.py`: Visualization functions
- `test_graphical_abstract.py`: Panel generation

## Performance

- Export: O(n) for n transitions
- Visualization: O(n) for plotting, O(n²) for some projections
- Canonical check: O(n) for n transitions

