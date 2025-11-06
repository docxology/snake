"""Performance plotting functions for computation time analysis."""

from typing import Dict, List, Optional
import numpy as np
try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


def plot_computation_time_vs_dimension(
    times: Dict[int, float],
    output_file: str = "output/visualizations/computation_time_vs_dimension.png",
    log_scale: bool = True
) -> None:
    """Plot computation time vs dimension.
    
    Parameters
    ----------
    times : Dict[int, float]
        Dictionary mapping dimension to computation time in seconds
    output_file : str, optional
        Output file path
    log_scale : bool, optional
        Use logarithmic scale for y-axis (default: True)
    """
    if not HAS_MATPLOTLIB:
        return
    
    dimensions = sorted(times.keys())
    time_values = [times[d] for d in dimensions]
    
    # Filter out zero times
    valid_data = [(d, t) for d, t in zip(dimensions, time_values) if t > 0]
    if not valid_data:
        return
    
    valid_dims, valid_times = zip(*valid_data)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.scatter(valid_dims, valid_times, s=100, alpha=0.7, c=valid_dims, 
               cmap='viridis', edgecolors='black', linewidths=1.5)
    ax.plot(valid_dims, valid_times, '--', alpha=0.5, linewidth=1)
    
    # Add dimension labels
    for d, t in valid_data:
        ax.annotate(f'D{d}', (d, t), xytext=(5, 5), textcoords='offset points', 
                   fontsize=9, fontweight='bold')
    
    ax.set_xlabel('Dimension N', fontsize=12, fontweight='bold')
    ax.set_ylabel('Computation Time (seconds)', fontsize=12, fontweight='bold')
    ax.set_title('Computation Time vs Dimension', fontsize=14, fontweight='bold')
    ax.grid(alpha=0.3)
    
    if log_scale:
        ax.set_yscale('log')
        ax.set_ylabel('Computation Time (seconds, log scale)', fontsize=12, fontweight='bold')
    
    plt.colorbar(plt.cm.ScalarMappable(cmap='viridis'), ax=ax, label='Dimension')
    plt.tight_layout()
    
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()


def plot_exponential_fit(
    times: Dict[int, float],
    output_file: str = "output/visualizations/exponential_fit.png"
) -> None:
    """Plot computation time with fitted exponential curve.
    
    Parameters
    ----------
    times : Dict[int, float]
        Dictionary mapping dimension to computation time
    output_file : str, optional
        Output file path
    """
    if not HAS_MATPLOTLIB:
        return
    
    dimensions = sorted(times.keys())
    time_values = [times[d] for d in dimensions]
    
    # Filter valid data
    valid_data = [(d, t) for d, t in zip(dimensions, time_values) if t > 0]
    if len(valid_data) < 2:
        return
    
    valid_dims, valid_times = zip(*valid_data)
    valid_dims = np.array(valid_dims)
    valid_times = np.array(valid_times)
    
    # Fit exponential model (lazy import to avoid circular dependency)
    from ..analysis.exponential_analysis import fit_exponential_model, estimate_time_for_dimension
    model = fit_exponential_model(times)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot actual data
    ax.scatter(valid_dims, valid_times, s=150, alpha=0.7, color='steelblue',
               edgecolors='black', linewidths=1.5, label='Actual Times', zorder=3)
    
    # Plot fitted curve
    if model['r_squared'] > 0.1:
        dim_range = np.arange(min(valid_dims), max(valid_dims) + 1, 0.1)
        fitted_times = [estimate_time_for_dimension(int(d), model) for d in dim_range]
        ax.plot(dim_range, fitted_times, 'r-', linewidth=2, alpha=0.7,
               label=f"Exponential Fit (R²={model['r_squared']:.3f})", zorder=2)
    
    ax.set_xlabel('Dimension N', fontsize=12, fontweight='bold')
    ax.set_ylabel('Computation Time (seconds, log scale)', fontsize=12, fontweight='bold')
    ax.set_title('Computation Time with Exponential Fit', fontsize=14, fontweight='bold')
    ax.set_yscale('log')
    ax.grid(alpha=0.3)
    ax.legend()
    
    plt.tight_layout()
    
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()


def plot_slowdown_analysis(
    times: Dict[int, float],
    output_file: str = "output/visualizations/slowdown_analysis.png"
) -> None:
    """Plot slowdown analysis highlighting exponential growth regions.
    
    Parameters
    ----------
    times : Dict[int, float]
        Dictionary mapping dimension to computation time
    output_file : str, optional
        Output file path
    """
    if not HAS_MATPLOTLIB:
        return
    
    # Lazy import to avoid circular dependency
    from ..analysis.exponential_analysis import analyze_computation_complexity, identify_slowdown_points
    
    dimensions = sorted(times.keys())
    time_values = [times[d] for d in dimensions]
    
    valid_data = [(d, t) for d, t in zip(dimensions, time_values) if t > 0]
    if not valid_data:
        return
    
    valid_dims, valid_times = zip(*valid_data)
    
    complexity = analyze_computation_complexity(times)
    slowdown_points = identify_slowdown_points(times)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Top plot: Time vs dimension with slowdown points highlighted
    colors = ['green' if d not in slowdown_points else 'red' for d in valid_dims]
    ax1.scatter(valid_dims, valid_times, s=150, c=colors, alpha=0.7,
               edgecolors='black', linewidths=1.5)
    ax1.plot(valid_dims, valid_times, '--', alpha=0.3, linewidth=1)
    
    # Highlight exponential regions
    for start, end in complexity['exponential_regions']:
        ax1.axvspan(start, end, alpha=0.2, color='orange', label='Exponential Region')
    
    ax1.set_xlabel('Dimension N', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Computation Time (seconds, log scale)', fontsize=12, fontweight='bold')
    ax1.set_title('Computation Time with Slowdown Points Highlighted', fontsize=14, fontweight='bold')
    ax1.set_yscale('log')
    ax1.grid(alpha=0.3)
    ax1.legend()
    
    # Bottom plot: Growth factors
    if complexity['growth_factors']:
        growth_dims = sorted(complexity['growth_factors'].keys())
        growth_values = [complexity['growth_factors'][d] for d in growth_dims]
        
        colors_growth = ['green' if g < 2.0 else 'red' for g in growth_values]
        ax2.bar(growth_dims, growth_values, color=colors_growth, alpha=0.7, edgecolor='black')
        ax2.axhline(y=2.0, color='red', linestyle='--', linewidth=2, label='Doubling Threshold')
        ax2.set_xlabel('Dimension N', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Growth Factor', fontsize=12, fontweight='bold')
        ax2.set_title('Growth Factor by Dimension', fontsize=14, fontweight='bold')
        ax2.grid(axis='y', alpha=0.3)
        ax2.legend()
    
    plt.tight_layout()
    
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()


def plot_memory_vs_dimension(
    dimensions: List[int],
    output_file: str = "output/visualizations/memory_vs_dimension.png"
) -> None:
    """Plot memory requirements vs dimension.
    
    Parameters
    ----------
    dimensions : List[int]
        List of dimensions to analyze
    output_file : str, optional
        Output file path
    """
    if not HAS_MATPLOTLIB:
        return
    
    # Lazy import to avoid circular dependency
    from ..analysis.exponential_analysis import analyze_memory_complexity
    
    memory_analysis = analyze_memory_complexity(dimensions)
    
    dims = sorted(memory_analysis.keys())
    bitmap_mem = [memory_analysis[d]['bitmap_memory_gb'] for d in dims]
    est_mem = [memory_analysis[d]['estimated_memory_gb'] for d in dims]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(dims, bitmap_mem, 'o-', label='Bitmap Memory', linewidth=2, markersize=8)
    ax.plot(dims, est_mem, 's-', label='Estimated Total Memory', linewidth=2, markersize=8)
    
    ax.set_xlabel('Dimension N', fontsize=12, fontweight='bold')
    ax.set_ylabel('Memory (GB, log scale)', fontsize=12, fontweight='bold')
    ax.set_title('Memory Requirements vs Dimension', fontsize=14, fontweight='bold')
    ax.set_yscale('log')
    ax.grid(alpha=0.3)
    ax.legend()
    
    plt.tight_layout()
    
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

