"""Visualization functions for dimensions 1-16."""

from typing import List, Optional, Tuple
import numpy as np
try:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

from ..core.snake_node import SnakeNode
from ..core.transitions import transition_to_vertex
from .visualization_helpers import (
    get_color_scheme,
    pca_projection,
    pairwise_projection,
    force_directed_layout,
    hypercube_unfolding,
    apply_styling,
)


def visualize_snake_1d(snake_node: SnakeNode, show_plot: bool = True) -> Optional[plt.Figure]:
    """Visualize 1D snake as line plot.
    
    Parameters
    ----------
    snake_node : SnakeNode
        Snake node to visualize (must be dimension 1)
    show_plot : bool, optional
        Show plot immediately (default: True)
    
    Returns
    -------
    Optional[plt.Figure]
        Figure object, or None if matplotlib not available
    """
    if not HAS_MATPLOTLIB:
        raise ImportError("matplotlib required for visualization")
    
    if snake_node.dimension != 1:
        raise ValueError(f"1D visualization only for dimension 1, got {snake_node.dimension}")
    
    vertices = transition_to_vertex(snake_node.transition_sequence, 1)
    x = [(v >> 0) & 1 for v in vertices]
    y = list(range(len(vertices)))
    
    color_scheme = get_color_scheme()
    fig, ax = plt.subplots(figsize=(6, 8))
    
    ax.plot(x, y, color=color_scheme['snake_color'], 
            marker=color_scheme['snake_marker'],
            linewidth=color_scheme['snake_linewidth'],
            markersize=color_scheme['snake_markersize'])
    
    ax.set_xlabel('Bit Value')
    ax.set_ylabel('Position')
    ax.set_title(f'1D Snake (Length {len(vertices) - 1})')
    ax.set_xticks([0, 1])
    ax.grid(True, alpha=color_scheme['grid_alpha'])
    
    if show_plot:
        plt.show()
    
    return fig


def visualize_snake_2d(snake_node: SnakeNode, show_plot: bool = True) -> Optional[plt.Figure]:
    """Visualize 2D snake as grid plot.
    
    Parameters
    ----------
    snake_node : SnakeNode
        Snake node to visualize (must be dimension 2)
    show_plot : bool, optional
        Show plot immediately (default: True)
    
    Returns
    -------
    Optional[plt.Figure]
        Figure object
    """
    if not HAS_MATPLOTLIB:
        raise ImportError("matplotlib required for visualization")
    
    if snake_node.dimension != 2:
        raise ValueError(f"2D visualization only for dimension 2, got {snake_node.dimension}")
    
    vertices = transition_to_vertex(snake_node.transition_sequence, 2)
    x = [(v >> 0) & 1 for v in vertices]
    y = [(v >> 1) & 1 for v in vertices]
    
    color_scheme = get_color_scheme()
    fig, ax = plt.subplots(figsize=(8, 8))
    
    ax.plot(x, y, color=color_scheme['snake_color'],
            marker=color_scheme['snake_marker'],
            linewidth=color_scheme['snake_linewidth'],
            markersize=color_scheme['snake_markersize'])
    
    # Draw grid
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.1, 1.1)
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.grid(True, alpha=color_scheme['grid_alpha'], color=color_scheme['grid_color'])
    ax.set_aspect('equal')
    ax.set_xlabel('Dimension 0')
    ax.set_ylabel('Dimension 1')
    ax.set_title(f'2D Snake (Length {len(vertices) - 1})')
    
    if show_plot:
        plt.show()
    
    return fig


def visualize_snake_3d_advanced(snake_node: SnakeNode, show_plot: bool = True) -> Optional[plt.Figure]:
    """Enhanced 3D visualization.
    
    Parameters
    ----------
    snake_node : SnakeNode
        Snake node to visualize (must be dimension 3)
    show_plot : bool, optional
        Show plot immediately (default: True)
    
    Returns
    -------
    Optional[plt.Figure]
        Figure object
    """
    if not HAS_MATPLOTLIB:
        raise ImportError("matplotlib required for visualization")
    
    if snake_node.dimension != 3:
        raise ValueError(f"3D visualization only for dimension 3, got {snake_node.dimension}")
    
    vertices = transition_to_vertex(snake_node.transition_sequence, 3)
    x = [(v >> 0) & 1 for v in vertices]
    y = [(v >> 1) & 1 for v in vertices]
    z = [(v >> 2) & 1 for v in vertices]
    
    color_scheme = get_color_scheme()
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot(x, y, z, color=color_scheme['snake_color'],
            marker=color_scheme['snake_marker'],
            linewidth=color_scheme['snake_linewidth'],
            markersize=color_scheme['snake_markersize'])
    
    # Draw cube edges
    for i in range(8):
        for dim in range(3):
            neighbor = i ^ (1 << dim)
            if neighbor > i:
                xi, yi, zi = (i >> 0) & 1, (i >> 1) & 1, (i >> 2) & 1
                xn, yn, zn = (neighbor >> 0) & 1, (neighbor >> 1) & 1, (neighbor >> 2) & 1
                ax.plot([xi, xn], [yi, yn], [zi, zn], 'k-', alpha=0.3, linewidth=0.5)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'3D Snake (Length {len(vertices) - 1})')
    ax.set_box_aspect([1, 1, 1])
    
    if show_plot:
        plt.show()
    
    return fig


def visualize_snake_nd(
    snake_node: SnakeNode,
    method: str = 'pca',
    show_plot: bool = True,
    dim1: Optional[int] = None,
    dim2: Optional[int] = None
) -> Optional[plt.Figure]:
    """Visualize snake in N dimensions using projection.
    
    Parameters
    ----------
    snake_node : SnakeNode
        Snake node to visualize
    method : str, optional
        Projection method: 'pca', 'pairwise', 'force', 'unfolding' (default: 'pca')
    show_plot : bool, optional
        Show plot immediately (default: True)
    dim1 : Optional[int], optional
        First dimension for pairwise projection
    dim2 : Optional[int], optional
        Second dimension for pairwise projection
    
    Returns
    -------
    Optional[plt.Figure]
        Figure object
    """
    if not HAS_MATPLOTLIB:
        raise ImportError("matplotlib required for visualization")
    
    if snake_node.dimension <= 3:
        raise ValueError(f"Use dimension-specific visualization for dim <= 3")
    
    vertices = transition_to_vertex(snake_node.transition_sequence, snake_node.dimension)
    color_scheme = get_color_scheme()
    
    # Get projection coordinates
    if method == 'pairwise':
        if dim1 is None or dim2 is None:
            dim1, dim2 = 0, 1
        x, y = pairwise_projection(vertices, snake_node.dimension, dim1, dim2)
        coords = np.array([[xi, yi] for xi, yi in zip(x, y)])
    elif method == 'pca':
        coords = pca_projection(vertices, snake_node.dimension, n_components=2)
    elif method == 'force':
        coords = force_directed_layout(vertices, snake_node.dimension)
    elif method == 'unfolding':
        coords = hypercube_unfolding(vertices, snake_node.dimension)
    else:
        coords = pca_projection(vertices, snake_node.dimension, n_components=2)
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    ax.plot(coords[:, 0], coords[:, 1],
            color=color_scheme['snake_color'],
            marker=color_scheme['snake_marker'],
            linewidth=color_scheme['snake_linewidth'],
            markersize=color_scheme['snake_markersize'])
    
    ax.set_xlabel(f'Projection 1 ({method})')
    ax.set_ylabel(f'Projection 2 ({method})')
    ax.set_title(f'{snake_node.dimension}D Snake (Length {len(vertices) - 1}, {method} projection)')
    ax.grid(True, alpha=color_scheme['grid_alpha'])
    ax.set_aspect('equal')
    
    if show_plot:
        plt.show()
    
    return fig


def visualize_snake_auto(snake_node: SnakeNode, show_plot: bool = True) -> Optional[plt.Figure]:
    """Automatically choose appropriate visualization method.
    
    Parameters
    ----------
    snake_node : SnakeNode
        Snake node to visualize
    show_plot : bool, optional
        Show plot immediately (default: True)
    
    Returns
    -------
    Optional[plt.Figure]
        Figure object
    """
    dim = snake_node.dimension
    
    if dim == 1:
        return visualize_snake_1d(snake_node, show_plot)
    elif dim == 2:
        return visualize_snake_2d(snake_node, show_plot)
    elif dim == 3:
        return visualize_snake_3d_advanced(snake_node, show_plot)
    else:
        return visualize_snake_nd(snake_node, method='pca', show_plot=show_plot)


def visualize_snake_heatmap(snake_node: SnakeNode, show_plot: bool = True) -> Optional[plt.Figure]:
    """Visualize snake as heatmap showing bit patterns.
    
    Parameters
    ----------
    snake_node : SnakeNode
        Snake node to visualize
    show_plot : bool, optional
        Show plot immediately (default: True)
    
    Returns
    -------
    Optional[plt.Figure]
        Figure object
    """
    if not HAS_MATPLOTLIB:
        raise ImportError("matplotlib required for visualization")
    
    vertices = transition_to_vertex(snake_node.transition_sequence, snake_node.dimension)
    
    # Create binary matrix
    n_vertices = len(vertices)
    binary_matrix = np.zeros((n_vertices, snake_node.dimension))
    
    for i, vertex in enumerate(vertices):
        for j in range(snake_node.dimension):
            binary_matrix[i, j] = (vertex >> j) & 1
    
    fig, ax = plt.subplots(figsize=(max(8, snake_node.dimension), max(6, n_vertices // 10)))
    im = ax.imshow(binary_matrix, aspect='auto', cmap='RdYlBu_r', interpolation='nearest')
    
    ax.set_xlabel('Bit Position')
    ax.set_ylabel('Vertex Index')
    ax.set_title(f'{snake_node.dimension}D Snake Heatmap (Length {n_vertices - 1})')
    ax.set_yticks(range(0, n_vertices, max(1, n_vertices // 20)))
    
    plt.colorbar(im, ax=ax, label='Bit Value')
    
    if show_plot:
        plt.show()
    
    return fig


def visualize_snake_3d_projection(snake_node: SnakeNode, show_plot: bool = True) -> Optional[plt.Figure]:
    """Visualize high-dimensional snake using 3D PCA projection.
    
    Parameters
    ----------
    snake_node : SnakeNode
        Snake node to visualize (dimension >= 4)
    show_plot : bool, optional
        Show plot immediately (default: True)
    
    Returns
    -------
    Optional[plt.Figure]
        Figure object
    """
    if not HAS_MATPLOTLIB:
        raise ImportError("matplotlib required for visualization")
    
    if snake_node.dimension < 4:
        raise ValueError("3D projection requires dimension >= 4")
    
    vertices = transition_to_vertex(snake_node.transition_sequence, snake_node.dimension)
    
    # Convert to binary matrix
    n_vertices = len(vertices)
    binary_matrix = np.zeros((n_vertices, snake_node.dimension))
    
    for i, vertex in enumerate(vertices):
        for j in range(snake_node.dimension):
            binary_matrix[i, j] = (vertex >> j) & 1
    
    # Center the data
    mean = np.mean(binary_matrix, axis=0)
    centered = binary_matrix - mean
    
    # Compute covariance matrix
    cov = np.cov(centered.T)
    
    # Eigenvalue decomposition
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    
    # Sort by eigenvalue (descending)
    idx = eigenvalues.argsort()[::-1]
    eigenvectors = eigenvectors[:, idx]
    
    # Project to 3D
    coords = centered @ eigenvectors[:, :3]
    
    color_scheme = get_color_scheme()
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Color by position in sequence
    colors = plt.cm.viridis(np.linspace(0, 1, n_vertices))
    
    ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2],
               c=colors, s=50, alpha=0.6)
    
    ax.plot(coords[:, 0], coords[:, 1], coords[:, 2],
            color=color_scheme['snake_color'],
            linewidth=color_scheme['snake_linewidth'],
            alpha=0.5)
    
    ax.set_xlabel('PC1')
    ax.set_ylabel('PC2')
    ax.set_zlabel('PC3')
    ax.set_title(f'{snake_node.dimension}D Snake 3D Projection (Length {n_vertices - 1})')
    
    if show_plot:
        plt.show()
    
    return fig


def visualize_snake_transition_matrix(snake_node: SnakeNode, show_plot: bool = True) -> Optional[plt.Figure]:
    """Visualize transition sequence as matrix showing dimension usage.
    
    Parameters
    ----------
    snake_node : SnakeNode
        Snake node to visualize
    show_plot : bool, optional
        Show plot immediately (default: True)
    
    Returns
    -------
    Optional[plt.Figure]
        Figure object
    """
    if not HAS_MATPLOTLIB:
        raise ImportError("matplotlib required for visualization")
    
    transitions = snake_node.transition_sequence
    n_transitions = len(transitions)
    
    # Create transition matrix
    transition_matrix = np.zeros((snake_node.dimension, n_transitions))
    
    for i, trans in enumerate(transitions):
        if 0 <= trans < snake_node.dimension:
            transition_matrix[trans, i] = 1
    
    fig, ax = plt.subplots(figsize=(max(8, n_transitions // 10), max(6, snake_node.dimension)))
    im = ax.imshow(transition_matrix, aspect='auto', cmap='YlOrRd', interpolation='nearest')
    
    ax.set_xlabel('Position in Sequence')
    ax.set_ylabel('Dimension')
    ax.set_title(f'Transition Matrix for {snake_node.dimension}D Snake (Length {n_transitions})')
    ax.set_yticks(range(snake_node.dimension))
    
    plt.colorbar(im, ax=ax, label='Dimension Used')
    
    if show_plot:
        plt.show()
    
    return fig

