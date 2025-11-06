"""Exponential slowdown analysis for computation time.

Analyzes computation time growth patterns to identify exponential regions
and estimate times for higher dimensions.
"""

from typing import Dict, List, Tuple, Optional
import numpy as np
from scipy import optimize
import math


def analyze_computation_complexity(times: Dict[int, float]) -> Dict:
    """Analyze computation complexity from timing data.
    
    Parameters
    ----------
    times : Dict[int, float]
        Dictionary mapping dimension to computation time in seconds
    
    Returns
    -------
    Dict
        Analysis results including:
        - growth_factors: Dict[int, float] - Growth factor from previous dimension
        - exponential_regions: List[Tuple[int, int]] - Regions with exponential growth
        - complexity_class: str - Overall complexity classification
        - doubling_dimensions: List[int] - Dimensions where time doubles
    """
    if len(times) < 2:
        return {
            'growth_factors': {},
            'exponential_regions': [],
            'complexity_class': 'insufficient_data',
            'doubling_dimensions': []
        }
    
    dimensions = sorted(times.keys())
    growth_factors = {}
    doubling_dimensions = []
    
    for i in range(1, len(dimensions)):
        dim_prev = dimensions[i-1]
        dim_curr = dimensions[i]
        
        time_prev = times[dim_prev]
        time_curr = times[dim_curr]
        
        if time_prev > 0:
            growth_factor = time_curr / time_prev
            growth_factors[dim_curr] = growth_factor
            
            # Check if time approximately doubled
            if 1.8 <= growth_factor <= 2.2:
                doubling_dimensions.append(dim_curr)
    
    # Identify exponential regions (growth factor >= 1.5)
    exponential_regions = []
    region_start = None
    
    for dim in dimensions[1:]:
        if dim in growth_factors and growth_factors[dim] >= 1.5:
            if region_start is None:
                region_start = dim - 1
        else:
            if region_start is not None:
                exponential_regions.append((region_start, dim - 1))
                region_start = None
    
    if region_start is not None:
        exponential_regions.append((region_start, dimensions[-1]))
    
    # Classify overall complexity
    avg_growth = np.mean(list(growth_factors.values())) if growth_factors else 1.0
    
    if avg_growth >= 2.0:
        complexity_class = 'exponential'
    elif avg_growth >= 1.5:
        complexity_class = 'super_linear'
    elif avg_growth >= 1.2:
        complexity_class = 'linear_growth'
    else:
        complexity_class = 'sub_linear'
    
    return {
        'growth_factors': growth_factors,
        'exponential_regions': exponential_regions,
        'complexity_class': complexity_class,
        'doubling_dimensions': doubling_dimensions,
        'average_growth_factor': avg_growth
    }


def identify_slowdown_points(times: Dict[int, float], threshold: float = 2.0) -> List[int]:
    """Identify dimensions where exponential slowdown begins.
    
    Parameters
    ----------
    times : Dict[int, float]
        Dictionary mapping dimension to computation time
    threshold : float, optional
        Growth factor threshold to consider as slowdown (default: 2.0)
    
    Returns
    -------
    List[int]
        List of dimensions where slowdown occurs
    """
    dimensions = sorted(times.keys())
    slowdown_points = []
    
    for i in range(1, len(dimensions)):
        dim_prev = dimensions[i-1]
        dim_curr = dimensions[i]
        
        time_prev = times[dim_prev]
        time_curr = times[dim_curr]
        
        if time_prev > 0:
            growth_factor = time_curr / time_prev
            if growth_factor >= threshold:
                slowdown_points.append(dim_curr)
    
    return slowdown_points


def fit_exponential_model(times: Dict[int, float]) -> Dict:
    """Fit exponential model to timing data.
    
    Fits model: time(N) = a * b^N
    
    Parameters
    ----------
    times : Dict[int, float]
        Dictionary mapping dimension to computation time
    
    Returns
    -------
    Dict
        Model parameters and statistics:
        - base: float - Base of exponential (b)
        - coefficient: float - Coefficient (a)
        - r_squared: float - R-squared value
        - model_function: callable - Function time(N) = a * b^N
    """
    if len(times) < 2:
        return {
            'base': 1.0,
            'coefficient': 0.0,
            'r_squared': 0.0,
            'model_function': lambda N: 0.0
        }
    
    dimensions = np.array(sorted(times.keys()))
    time_values = np.array([times[d] for d in dimensions])
    
    # Filter out zero times
    valid_mask = time_values > 0
    if valid_mask.sum() < 2:
        return {
            'base': 1.0,
            'coefficient': 0.0,
            'r_squared': 0.0,
            'model_function': lambda N: 0.0
        }
    
    dims_valid = dimensions[valid_mask]
    times_valid = time_values[valid_mask]
    
    # Use log-linear regression: log(time) = log(a) + N * log(b)
    log_times = np.log(times_valid)
    
    # Fit linear model: log(time) = intercept + slope * N
    coeffs = np.polyfit(dims_valid, log_times, 1)
    slope = coeffs[0]
    intercept = coeffs[1]
    
    # Convert back: a = exp(intercept), b = exp(slope)
    coefficient = np.exp(intercept)
    base = np.exp(slope)
    
    # Calculate R-squared
    predicted_log = intercept + slope * dims_valid
    predicted = np.exp(predicted_log)
    ss_res = np.sum((times_valid - predicted) ** 2)
    ss_tot = np.sum((times_valid - np.mean(times_valid)) ** 2)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
    
    def model_function(N: int) -> float:
        """Model function: time(N) = a * b^N"""
        return coefficient * (base ** N)
    
    return {
        'base': base,
        'coefficient': coefficient,
        'r_squared': r_squared,
        'model_function': model_function,
        'slope': slope,
        'intercept': intercept
    }


def estimate_time_for_dimension(N: int, model_params: Dict) -> float:
    """Estimate computation time for dimension N using fitted model.
    
    Parameters
    ----------
    N : int
        Dimension to estimate
    model_params : Dict
        Model parameters from fit_exponential_model()
    
    Returns
    -------
    float
        Estimated time in seconds
    """
    model_func = model_params.get('model_function')
    if model_func:
        return model_func(N)
    return 0.0


def analyze_memory_complexity(dimensions: List[int]) -> Dict[int, Dict]:
    """Analyze memory complexity for dimensions.
    
    Parameters
    ----------
    dimensions : List[int]
        List of dimensions to analyze
    
    Returns
    -------
    Dict[int, Dict]
        Memory analysis for each dimension
    """
    results = {}
    
    for N in dimensions:
        num_vertices = 2 ** N
        num_edges = N * (2 ** (N - 1))
        
        # Bitmap memory: 2^N bits = 2^N / 8 bytes
        bitmap_bytes = num_vertices / 8
        bitmap_gb = bitmap_bytes / (1024 ** 3)
        
        # Estimated node size
        node_size_bytes = 100 + bitmap_bytes
        node_size_gb = node_size_bytes / (1024 ** 3)
        
        # Rough estimate of nodes (conservative)
        estimated_nodes = min(10 ** (N - 3), 10 ** 7) if N <= 10 else 2 ** (N - 3) * 1000
        estimated_memory_gb = estimated_nodes * node_size_gb
        
        results[N] = {
            'num_vertices': num_vertices,
            'num_edges': num_edges,
            'bitmap_memory_gb': bitmap_gb,
            'node_size_gb': node_size_gb,
            'estimated_nodes': estimated_nodes,
            'estimated_memory_gb': estimated_memory_gb
        }
    
    return results


def generate_exponential_report(
    times: Dict[int, float],
    output_file: str = "output/reports/exponential_analysis.md"
) -> str:
    """Generate comprehensive exponential analysis report.
    
    Parameters
    ----------
    times : Dict[int, float]
        Computation times by dimension
    output_file : str, optional
        Output file path
    
    Returns
    -------
    str
        Report content
    """
    from datetime import datetime
    
    lines = []
    lines.append("# Exponential Slowdown Analysis")
    lines.append("")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    
    # Complexity analysis
    complexity = analyze_computation_complexity(times)
    lines.append("## Complexity Analysis")
    lines.append("")
    lines.append(f"- **Overall Complexity**: {complexity['complexity_class']}")
    lines.append(f"- **Average Growth Factor**: {complexity['average_growth_factor']:.3f}")
    lines.append("")
    
    # Growth factors table
    if complexity['growth_factors']:
        lines.append("### Growth Factors by Dimension")
        lines.append("")
        lines.append("| Dimension | Time (s) | Growth Factor |")
        lines.append("|-----------|----------|---------------|")
        
        dimensions = sorted(times.keys())
        for i, dim in enumerate(dimensions):
            time_val = times[dim]
            growth = complexity['growth_factors'].get(dim, '-')
            if isinstance(growth, float):
                growth_str = f"{growth:.3f}"
            else:
                growth_str = str(growth)
            lines.append(f"| {dim} | {time_val:.6f} | {growth_str} |")
        lines.append("")
    
    # Exponential regions
    if complexity['exponential_regions']:
        lines.append("### Exponential Growth Regions")
        lines.append("")
        for start, end in complexity['exponential_regions']:
            lines.append(f"- Dimensions {start}-{end}: Exponential growth (factor >= 1.5)")
        lines.append("")
    
    # Slowdown points
    slowdown_points = identify_slowdown_points(times)
    if slowdown_points:
        lines.append("### Slowdown Points")
        lines.append("")
        lines.append("Dimensions where computation time doubles or more:")
        for dim in slowdown_points:
            lines.append(f"- Dimension {dim}: {times[dim]:.6f}s")
        lines.append("")
    
    # Exponential model
    model = fit_exponential_model(times)
    lines.append("## Exponential Model Fit")
    lines.append("")
    lines.append(f"Model: time(N) = {model['coefficient']:.6e} * {model['base']:.6f}^N")
    lines.append(f"R-squared: {model['r_squared']:.4f}")
    lines.append("")
    
    # Estimates for higher dimensions
    if model['r_squared'] > 0.5:
        lines.append("### Estimated Times for Higher Dimensions")
        lines.append("")
        lines.append("| Dimension | Estimated Time (seconds) | Estimated Time (hours) |")
        lines.append("|-----------|-------------------------|------------------------|")
        
        for N in range(max(times.keys()) + 1, max(times.keys()) + 5):
            est_seconds = estimate_time_for_dimension(N, model)
            est_hours = est_seconds / 3600.0
            lines.append(f"| {N} | {est_seconds:.2e} | {est_hours:.2f} |")
        lines.append("")
    
    # Memory analysis
    dimensions_list = sorted(times.keys())
    memory_analysis = analyze_memory_complexity(dimensions_list)
    
    lines.append("## Memory Complexity Analysis")
    lines.append("")
    lines.append("| Dimension | Vertices | Bitmap (GB) | Est. Memory (GB) |")
    lines.append("|-----------|----------|-------------|------------------|")
    
    for N in dimensions_list:
        mem = memory_analysis[N]
        lines.append(
            f"| {N} | {mem['num_vertices']:,} | "
            f"{mem['bitmap_memory_gb']:.6f} | {mem['estimated_memory_gb']:.2f} |"
        )
    lines.append("")
    
    content = "\n".join(lines)
    
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        f.write(content)
    
    return content

