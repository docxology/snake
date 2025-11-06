"""Graphical abstract generator for 4x4 panel visualization."""

from typing import List, Optional, Dict, Tuple
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


def generate_16d_panel(
    snake_nodes: Dict[int, SnakeNode],
    output_file: Optional[str] = None,
    figsize: Tuple[int, int] = (20, 20),
    dpi: int = 300
) -> Optional[plt.Figure]:
    """Generate 4x4 panel graphical abstract for dimensions 1-16.
    
    Parameters
    ----------
    snake_nodes : Dict[int, SnakeNode]
        Dictionary mapping dimension to snake node
    output_file : Optional[str], optional
        File to save figure (default: None, show instead)
    figsize : Tuple[int, int], optional
        Figure size in inches (default: (20, 20))
    dpi : int, optional
        Resolution in dots per inch (default: 300)
    
    Returns
    -------
    Optional[plt.Figure]
        Figure object
    """
    if not HAS_MATPLOTLIB:
        raise ImportError("matplotlib required for graphical abstract")
    
    color_scheme = get_color_scheme()
    fig, axes = plt.subplots(4, 4, figsize=figsize, dpi=dpi)
    axes = axes.flatten()
    
    for dim in range(1, 17):
        ax = axes[dim - 1]
        
        if dim in snake_nodes:
            snake_node = snake_nodes[dim]
            _plot_snake_in_panel(ax, snake_node, dim, color_scheme)
        else:
            # Empty panel with dimension label
            ax.text(0.5, 0.5, f'Dim {dim}\nNo data', 
                   ha='center', va='center', fontsize=12)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
    
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=dpi, bbox_inches='tight')
        plt.close()
        return None
    
    return fig


def _plot_snake_in_panel(ax, snake_node: SnakeNode, dimension: int, color_scheme: Dict):
    """Plot snake in a single panel.
    
    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes to plot in
    snake_node : SnakeNode
        Snake node to plot
    dimension : int
        Dimension number
    color_scheme : Dict
        Color scheme dictionary
    """
    vertices = transition_to_vertex(snake_node.transition_sequence, dimension)
    length = len(vertices) - 1
    
    if dimension == 1:
        x = [(v >> 0) & 1 for v in vertices]
        y = list(range(len(vertices)))
        ax.plot(x, y, color=color_scheme['snake_color'],
                marker=color_scheme['snake_marker'],
                linewidth=1.5, markersize=4)
        ax.set_xlim(-0.1, 1.1)
        ax.set_xticks([0, 1])
        
    elif dimension == 2:
        x = [(v >> 0) & 1 for v in vertices]
        y = [(v >> 1) & 1 for v in vertices]
        ax.plot(x, y, color=color_scheme['snake_color'],
                marker=color_scheme['snake_marker'],
                linewidth=1.5, markersize=4)
        ax.set_xlim(-0.1, 1.1)
        ax.set_ylim(-0.1, 1.1)
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_aspect('equal')
        
    elif dimension == 3:
        # 3D projection to 2D
        x = [(v >> 0) & 1 for v in vertices]
        y = [(v >> 1) & 1 for v in vertices]
        z = [(v >> 2) & 1 for v in vertices]
        # Simple 2D projection: x-y with z as color/size
        ax.scatter(x, y, c=z, cmap='viridis', s=30, alpha=0.7)
        ax.plot(x, y, color=color_scheme['snake_color'],
                linewidth=1.5, alpha=0.5)
        ax.set_xlim(-0.1, 1.1)
        ax.set_ylim(-0.1, 1.1)
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_aspect('equal')
        
    else:
        # High dimension: use PCA projection
        try:
            coords = pca_projection(vertices, dimension, n_components=2)
            ax.plot(coords[:, 0], coords[:, 1],
                   color=color_scheme['snake_color'],
                   marker=color_scheme['snake_marker'],
                   linewidth=1.5, markersize=3, alpha=0.8)
        except:
            # Fallback: use first two dimensions
            x = [(v >> 0) & 1 for v in vertices]
            y = [(v >> 1) & 1 for v in vertices]
            ax.plot(x, y, color=color_scheme['snake_color'],
                   marker=color_scheme['snake_marker'],
                   linewidth=1.5, markersize=3)
    
    # Apply styling
    apply_styling(ax, dimension, length, color_scheme)
    ax.tick_params(labelsize=8)


def generate_panel_from_sequences(
    sequences: Dict[int, List[int]],
    output_file: Optional[str] = None,
    figsize: Tuple[int, int] = (20, 20),
    dpi: int = 300
) -> Optional[plt.Figure]:
    """Generate panel from transition sequences.
    
    Parameters
    ----------
    sequences : Dict[int, List[int]]
        Dictionary mapping dimension to transition sequence
    output_file : Optional[str], optional
        File to save figure
    figsize : Tuple[int, int], optional
        Figure size
    dpi : int, optional
        Resolution
    
    Returns
    -------
    Optional[plt.Figure]
        Figure object
    """
    snake_nodes = {}
    for dim, seq in sequences.items():
        try:
            snake_nodes[dim] = SnakeNode(seq, dim)
        except:
            pass  # Skip invalid sequences
    
    return generate_16d_panel(snake_nodes, output_file, figsize, dpi)


def generate_panel_from_analysis_results(
    analysis_results: Dict[int, Dict],
    output_file: Optional[str] = None,
    figsize: Tuple[int, int] = (20, 20),
    dpi: int = 300
) -> Optional[plt.Figure]:
    """Generate panel from analysis results.
    
    Parameters
    ----------
    analysis_results : Dict[int, Dict]
        Dictionary mapping dimension to analysis result dict
        Each dict should have 'snake_node' or 'transition_sequence'
    output_file : Optional[str], optional
        File to save figure
    figsize : Tuple[int, int], optional
        Figure size
    dpi : int, optional
        Resolution
    
    Returns
    -------
    Optional[plt.Figure]
        Figure object
    """
    snake_nodes = {}
    for dim, result in analysis_results.items():
        if 'snake_node' in result:
            snake_nodes[dim] = result['snake_node']
        elif 'transition_sequence' in result:
            try:
                snake_nodes[dim] = SnakeNode(result['transition_sequence'], dim)
            except:
                pass
    
    return generate_16d_panel(snake_nodes, output_file, figsize, dpi)

