"""Visualization helper functions."""

from typing import List, Tuple, Dict, Optional
import numpy as np
try:
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


def get_color_scheme(scheme: str = 'default') -> Dict[str, any]:
    """Get color scheme for visualization.
    
    Parameters
    ----------
    scheme : str, optional
        Color scheme name (default: 'default')
    
    Returns
    -------
    Dict[str, any]
        Color scheme dictionary
    """
    schemes = {
        'default': {
            'snake_color': 'red',
            'snake_marker': 'o',
            'snake_linewidth': 2,
            'snake_markersize': 8,
            'background_color': 'white',
            'grid_color': 'gray',
            'grid_alpha': 0.3,
        },
        'blue': {
            'snake_color': 'blue',
            'snake_marker': 's',
            'snake_linewidth': 2,
            'snake_markersize': 6,
            'background_color': 'white',
            'grid_color': 'lightblue',
            'grid_alpha': 0.2,
        },
        'green': {
            'snake_color': 'green',
            'snake_marker': '^',
            'snake_linewidth': 2,
            'snake_markersize': 6,
            'background_color': 'white',
            'grid_color': 'lightgreen',
            'grid_alpha': 0.2,
        },
    }
    return schemes.get(scheme, schemes['default'])


def pca_projection(vertices: List[int], dimension: int, n_components: int = 2) -> np.ndarray:
    """Project vertices to lower dimension using PCA.
    
    Parameters
    ----------
    vertices : List[int]
        Vertex sequence
    dimension : int
        Original dimension
    n_components : int, optional
        Number of components (default: 2)
    
    Returns
    -------
    np.ndarray
        Projected coordinates (n_vertices, n_components)
    """
    if not HAS_MATPLOTLIB:
        raise ImportError("matplotlib required for PCA projection")
    
    # Convert vertices to binary matrix
    n_vertices = len(vertices)
    binary_matrix = np.zeros((n_vertices, dimension))
    
    for i, vertex in enumerate(vertices):
        for j in range(dimension):
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
    
    # Project to n_components
    projection = centered @ eigenvectors[:, :n_components]
    
    return projection


def pairwise_projection(vertices: List[int], dimension: int, dim1: int, dim2: int) -> Tuple[List[float], List[float]]:
    """Project vertices to 2D using two specific dimensions.
    
    Parameters
    ----------
    vertices : List[int]
        Vertex sequence
    dimension : int
        Hypercube dimension
    dim1 : int
        First dimension to project
    dim2 : int
        Second dimension to project
    
    Returns
    -------
    Tuple[List[float], List[float]]
        (x_coordinates, y_coordinates)
    """
    x = [(v >> dim1) & 1 for v in vertices]
    y = [(v >> dim2) & 1 for v in vertices]
    return x, y


def force_directed_layout(vertices: List[int], dimension: int, iterations: int = 100) -> np.ndarray:
    """Force-directed graph layout for visualization.
    
    Parameters
    ----------
    vertices : List[int]
        Vertex sequence
    dimension : int
        Hypercube dimension
    iterations : int, optional
        Number of iterations (default: 100)
    
    Returns
    -------
    np.ndarray
        Coordinates (n_vertices, 2)
    """
    n_vertices = len(vertices)
    
    # Initialize positions randomly
    pos = np.random.rand(n_vertices, 2) * 10
    
    # Compute adjacency (consecutive vertices are adjacent)
    adj = np.zeros((n_vertices, n_vertices), dtype=bool)
    for i in range(n_vertices - 1):
        adj[i, i + 1] = True
        adj[i + 1, i] = True
    
    # Force-directed algorithm
    k = np.sqrt(100.0 / n_vertices)  # Optimal distance
    dt = 0.1  # Time step
    
    for _ in range(iterations):
        # Repulsive forces
        forces = np.zeros((n_vertices, 2))
        for i in range(n_vertices):
            for j in range(n_vertices):
                if i != j:
                    diff = pos[i] - pos[j]
                    dist = np.linalg.norm(diff)
                    if dist > 0:
                        forces[i] += k * k / dist * diff / dist
        
        # Attractive forces (for adjacent vertices)
        for i in range(n_vertices):
            for j in range(n_vertices):
                if adj[i, j]:
                    diff = pos[j] - pos[i]
                    dist = np.linalg.norm(diff)
                    if dist > 0:
                        forces[i] += dist / k * diff / dist
        
        # Update positions
        pos += dt * forces
        
        # Center the layout
        pos -= np.mean(pos, axis=0)
    
    return pos


def hypercube_unfolding(vertices: List[int], dimension: int) -> np.ndarray:
    """Unfold hypercube to show structure.
    
    For high dimensions, this creates a 2D layout that preserves
    some structural properties of the hypercube.
    
    Parameters
    ----------
    vertices : List[int]
        Vertex sequence
    dimension : int
        Hypercube dimension
    
    Returns
    -------
    np.ndarray
        Coordinates (n_vertices, 2)
    """
    n_vertices = len(vertices)
    pos = np.zeros((n_vertices, 2))
    
    # Simple unfolding: use Gray code ordering
    for i, vertex in enumerate(vertices):
        # Convert to binary and use as coordinates
        x = 0
        y = 0
        for j in range(min(dimension, 16)):  # Limit to avoid overflow
            bit = (vertex >> j) & 1
            if j % 2 == 0:
                x += bit * (2 ** (j // 2))
            else:
                y += bit * (2 ** (j // 2))
        
        pos[i] = [x, y]
    
    # Normalize
    if np.max(pos) > 0:
        pos = pos / np.max(pos) * 10
    
    return pos


def get_projection_method(method: str = 'pca'):
    """Get projection method function.
    
    Parameters
    ----------
    method : str, optional
        Method name: 'pca', 'pairwise', 'force', 'unfolding' (default: 'pca')
    
    Returns
    -------
    callable
        Projection function
    """
    methods = {
        'pca': pca_projection,
        'pairwise': pairwise_projection,
        'force': force_directed_layout,
        'unfolding': hypercube_unfolding,
    }
    return methods.get(method, pca_projection)


def create_figure_layout(n_plots: int, figsize: Tuple[int, int] = (16, 16)) -> Tuple[plt.Figure, List]:
    """Create figure with subplot layout.
    
    Parameters
    ----------
    n_plots : int
        Number of subplots
    figsize : Tuple[int, int], optional
        Figure size (default: (16, 16))
    
    Returns
    -------
    Tuple[plt.Figure, List]
        (figure, axes_list)
    """
    if not HAS_MATPLOTLIB:
        raise ImportError("matplotlib required")
    
    # Calculate grid dimensions
    n_cols = int(np.ceil(np.sqrt(n_plots)))
    n_rows = int(np.ceil(n_plots / n_cols))
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    
    # Flatten axes if needed
    if n_plots == 1:
        axes = [axes]
    elif n_rows == 1 or n_cols == 1:
        axes = axes.flatten() if hasattr(axes, 'flatten') else [axes]
    else:
        axes = axes.flatten()
    
    # Hide unused subplots
    for i in range(n_plots, len(axes)):
        axes[i].axis('off')
    
    return fig, axes[:n_plots]


def apply_styling(ax, dimension: int, length: int, color_scheme: Dict = None):
    """Apply consistent styling to axes.
    
    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes to style
    dimension : int
        Dimension number
    length : int
        Snake length
    color_scheme : Dict, optional
        Color scheme (default: None, uses default)
    """
    if color_scheme is None:
        color_scheme = get_color_scheme()
    
    ax.set_title(f'Dimension {dimension} (Length {length})', fontsize=10)
    ax.grid(True, alpha=color_scheme['grid_alpha'], color=color_scheme['grid_color'])
    ax.set_facecolor(color_scheme['background_color'])

