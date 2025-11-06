"""Visualization tools for snake-in-the-box."""

from typing import List
from ..core.snake_node import SnakeNode
from ..core.transitions import transition_to_vertex


def visualize_snake_3d(snake_node: SnakeNode, show_hypercube: bool = True) -> None:
    """Visualize 3D snake using matplotlib.
    
    Creates a 3D plot showing the snake path through the hypercube.
    Only works for dimension 3 (cube).
    
    Parameters
    ----------
    snake_node : SnakeNode
        Snake node to visualize (must be dimension 3)
    show_hypercube : bool, optional
        Show hypercube edges (default: True)
    
    Raises
    ------
    ValueError
        If dimension is not 3
    ImportError
        If matplotlib is not installed
    
    Examples
    --------
    >>> result = pruned_bfs_search(dimension=3)
    >>> visualize_snake_3d(result)
    """
    if snake_node.dimension != 3:
        raise ValueError(
            f"3D visualization only for dimension 3, got {snake_node.dimension}"
        )
    
    try:
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
    except ImportError:
        raise ImportError(
            "matplotlib is required for visualization. "
            "Install with: pip install matplotlib"
        )
    
    # Get vertex sequence
    vertices = transition_to_vertex(
        snake_node.transition_sequence,
        snake_node.dimension
    )
    
    # Extract coordinates
    x = [(v >> 0) & 1 for v in vertices]
    y = [(v >> 1) & 1 for v in vertices]
    z = [(v >> 2) & 1 for v in vertices]
    
    # Create figure
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Draw snake path
    ax.plot(x, y, z, 'r-o', linewidth=2, markersize=8, label='Snake path')
    
    # Draw cube edges if requested
    if show_hypercube:
        for i in range(8):
            for dim in range(3):
                neighbor = i ^ (1 << dim)
                if neighbor > i:  # Draw each edge once
                    xi, yi, zi = (i >> 0) & 1, (i >> 1) & 1, (i >> 2) & 1
                    xn, yn, zn = (
                        (neighbor >> 0) & 1,
                        (neighbor >> 1) & 1,
                        (neighbor >> 2) & 1
                    )
                    ax.plot([xi, xn], [yi, yn], [zi, zn], 'k-', alpha=0.3, linewidth=0.5)
    
    # Labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'Snake in 3D Cube (Length {len(vertices) - 1})')
    ax.legend()
    
    # Set equal aspect ratio
    ax.set_box_aspect([1, 1, 1])
    
    plt.show()



