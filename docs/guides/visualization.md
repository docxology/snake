# Visualization Guide

This guide covers visualization options for snakes of various dimensions.

## Automatic Visualization

For most cases, use automatic visualization which chooses the appropriate method:

```python
from snake_in_box import pruned_bfs_search, visualize_snake_auto

result = pruned_bfs_search(dimension=3)
if result:
    visualize_snake_auto(result, show_plot=True)
```

## 3D Visualization

For dimension 3, use specialized 3D visualization:

```python
from snake_in_box import pruned_bfs_search, visualize_snake_3d

result = pruned_bfs_search(dimension=3)
if result:
    visualize_snake_3d(result, show_hypercube=True)
```

## High-Dimensional Visualization

For dimensions 4+, automatic visualization uses projection methods:

```python
from snake_in_box import get_known_snake, SnakeNode, visualize_snake_auto

# Get known snake for dimension 7
transitions = get_known_snake(7)
node = SnakeNode(transitions, dimension=7)

# Visualize with automatic projection
visualize_snake_auto(node, show_plot=True)
```

## Graphical Abstract Panel

Generate a 4x4 panel showing all dimensions 1-16:

```python
from snake_in_box import get_known_snake, SnakeNode, generate_16d_panel

# Collect snakes for dimensions 1-13
snake_nodes = {}
for dim in range(1, 14):
    transitions = get_known_snake(dim)
    if transitions:
        snake_nodes[dim] = SnakeNode(transitions, dim)

# Generate panel
generate_16d_panel(
    snake_nodes,
    output_file="output/graphical_abstracts/panel.png",
    figsize=(20, 20),
    dpi=300
)
```

## Advanced Visualization Methods

### Heatmap Visualization

Visualize bit patterns as a heatmap:

```python
from snake_in_box.utils import visualize_snake_heatmap

result = pruned_bfs_search(dimension=7)
if result:
    visualize_snake_heatmap(result, show_plot=True)
```

### 3D Projection

For high dimensions (4+), use 3D PCA projection:

```python
from snake_in_box.utils import visualize_snake_3d_projection

result = pruned_bfs_search(dimension=7)
if result:
    visualize_snake_3d_projection(result, show_plot=True)
```

### Transition Matrix

Visualize dimension usage over the sequence:

```python
from snake_in_box.utils import visualize_snake_transition_matrix

result = pruned_bfs_search(dimension=7)
if result:
    visualize_snake_transition_matrix(result, show_plot=True)
```

## Custom Visualization

Access visualization functions directly for custom plots:

```python
from snake_in_box.utils.visualize_advanced import (
    visualize_snake_1d,
    visualize_snake_2d,
    visualize_snake_3d_advanced,
    visualize_snake_nd
)

# For dimension 1
node_1d = SnakeNode([0], dimension=1)
visualize_snake_1d(node_1d)

# For dimension 2
node_2d = SnakeNode([0, 1, 0], dimension=2)
visualize_snake_2d(node_2d)

# For dimension 3
node_3d = SnakeNode([0, 1, 2, 0], dimension=3)
visualize_snake_3d_advanced(node_3d)

# For dimension 4+
node_4d = SnakeNode([0, 1, 2, 3, 0], dimension=4)
visualize_snake_nd(node_4d, method='pca')
```

## Projection Methods

For high dimensions, choose projection method:

```python
from snake_in_box.utils.visualize_advanced import visualize_snake_nd

# PCA projection
visualize_snake_nd(node, method='pca')

# Pairwise projection
visualize_snake_nd(node, method='pairwise')

# Force-directed layout
visualize_snake_nd(node, method='force_directed')

# Hypercube unfolding
visualize_snake_nd(node, method='unfolding')
```

## Saving Figures

Save visualizations to files:

```python
from snake_in_box import visualize_snake_auto
import matplotlib.pyplot as plt

result = pruned_bfs_search(dimension=3)
if result:
    fig = visualize_snake_auto(result, show_plot=False)
    if fig:
        fig.savefig("snake_3d.png", dpi=300, bbox_inches='tight')
        plt.close(fig)
```

## Color Schemes

Customize color schemes (if supported):

```python
from snake_in_box.utils.visualization_helpers import get_color_scheme

# Get default color scheme
colors = get_color_scheme('default')

# Use in visualization
# (Implementation depends on visualization function)
```

## Related Documentation

- [Utils Module API](../api/utils.md) - Visualization API reference
- [Basic Usage](basic-usage.md) - Basic usage patterns
- [Advanced Usage](advanced-usage.md) - Advanced patterns

