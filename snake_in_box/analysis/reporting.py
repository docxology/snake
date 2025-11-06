"""Report generation for analysis results."""

from typing import Dict, List, Optional
from datetime import datetime
import os
from .analyze_dimensions import generate_statistics
from .exponential_analysis import (
    analyze_computation_complexity,
    identify_slowdown_points,
    fit_exponential_model,
    estimate_time_for_dimension
)


def generate_analysis_report(
    results: Dict[int, Dict],
    output_file: str = "analysis_report.md",
    format: str = "markdown"
) -> str:
    """Generate comprehensive analysis report.
    
    Parameters
    ----------
    results : Dict[int, Dict]
        Analysis results from analyze_dimensions
    output_file : str, optional
        Output file path (default: "analysis_report.md")
    format : str, optional
        Report format: 'markdown' or 'html' (default: 'markdown')
    
    Returns
    -------
    str
        Report content
    """
    stats = generate_statistics(results)
    
    if format == "markdown":
        content = _generate_markdown_report(results, stats)
    elif format == "html":
        content = _generate_html_report(results, stats)
    else:
        content = _generate_markdown_report(results, stats)
    
    with open(output_file, 'w') as f:
        f.write(content)
    
    return content


def _generate_markdown_report(results: Dict[int, Dict], stats: Dict) -> str:
    """Generate Markdown report."""
    lines = []
    
    # Header
    lines.append("# Snake-in-the-Box Analysis Report")
    lines.append("")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    
    # Executive Summary
    lines.append("## Executive Summary")
    lines.append("")
    lines.append(f"- **Total Dimensions Analyzed**: {stats['total_dimensions']}")
    lines.append(f"- **Valid Snakes**: {stats['valid_snakes']}")
    lines.append(f"- **Invalid Snakes**: {stats['invalid_snakes']}")
    lines.append(f"- **From Known Records**: {stats['from_known']}")
    lines.append(f"- **From Search**: {stats['from_search']}")
    lines.append(f"- **Matches Known Records**: {stats['matches_known']}")
    lines.append(f"- **Total Analysis Time**: {stats['total_time']:.2f} seconds")
    lines.append(f"- **Average Time per Dimension**: {stats['average_time']:.2f} seconds")
    lines.append("")
    
    # Results Table
    lines.append("## Results by Dimension")
    lines.append("")
    lines.append("| Dimension | Length | Valid | Method | Known Record | Matches | Time (s) |")
    lines.append("|-----------|--------|-------|--------|--------------|---------|----------|")
    
    for dim in sorted(results.keys()):
        r = results[dim]
        known = str(r['known_record']) if r['known_record'] else "N/A"
        matches = "✓" if r['matches_known'] else "✗"
        lines.append(
            f"| {dim} | {r['length']} | {'✓' if r['is_valid'] else '✗'} | "
            f"{r['method']} | {known} | {matches} | {r['search_time']:.2f} |"
        )
    
    lines.append("")
    
    # Detailed Results
    lines.append("## Detailed Results")
    lines.append("")
    
    for dim in sorted(results.keys()):
        r = results[dim]
        lines.append(f"### Dimension {dim}")
        lines.append("")
        lines.append(f"- **Length**: {r['length']}")
        lines.append(f"- **Valid**: {'Yes' if r['is_valid'] else 'No'}")
        lines.append(f"- **Method**: {r['method']}")
        lines.append(f"- **Search Time**: {r['search_time']:.2f} seconds")
        
        if r['known_record']:
            lines.append(f"- **Known Record**: {r['known_record']}")
            lines.append(f"- **Matches Known**: {'Yes' if r['matches_known'] else 'No'}")
        
        if r['validation_message']:
            lines.append(f"- **Validation**: {r['validation_message']}")
        
        lines.append("")
    
    # Statistics
    lines.append("## Statistics")
    lines.append("")
    lines.append(f"- **Total Length**: {stats['total_length']}")
    lines.append(f"- **Average Length**: {stats['average_length']:.2f}")
    lines.append(f"- **Maximum Length**: {stats['max_length']}")
    lines.append(f"- **Minimum Length**: {stats['min_length']}")
    lines.append("")
    
    # Methodology
    lines.append("## Methodology")
    lines.append("")
    lines.append("Analysis performed using:")
    lines.append("- Heuristically-pruned breadth-first search (Ace 2025)")
    lines.append("- Known snake records from literature")
    lines.append("- Validation using Hamming distance constraints")
    lines.append("")
    
    return "\n".join(lines)


def _generate_html_report(results: Dict[int, Dict], stats: Dict) -> str:
    """Generate HTML report."""
    html = []
    
    html.append("<!DOCTYPE html>")
    html.append("<html>")
    html.append("<head>")
    html.append("<title>Snake-in-the-Box Analysis Report</title>")
    html.append("<style>")
    html.append("body { font-family: Arial, sans-serif; margin: 20px; }")
    html.append("table { border-collapse: collapse; width: 100%; }")
    html.append("th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }")
    html.append("th { background-color: #4CAF50; color: white; }")
    html.append("tr:nth-child(even) { background-color: #f2f2f2; }")
    html.append("</style>")
    html.append("</head>")
    html.append("<body>")
    
    html.append("<h1>Snake-in-the-Box Analysis Report</h1>")
    html.append(f"<p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")
    
    html.append("<h2>Executive Summary</h2>")
    html.append("<ul>")
    html.append(f"<li><strong>Total Dimensions Analyzed</strong>: {stats['total_dimensions']}</li>")
    html.append(f"<li><strong>Valid Snakes</strong>: {stats['valid_snakes']}</li>")
    html.append(f"<li><strong>From Known Records</strong>: {stats['from_known']}</li>")
    html.append(f"<li><strong>From Search</strong>: {stats['from_search']}</li>")
    html.append(f"<li><strong>Total Analysis Time</strong>: {stats['total_time']:.2f} seconds</li>")
    html.append("</ul>")
    
    html.append("<h2>Results by Dimension</h2>")
    html.append("<table>")
    html.append("<tr><th>Dimension</th><th>Length</th><th>Valid</th><th>Method</th><th>Known Record</th><th>Matches</th><th>Time (s)</th></tr>")
    
    for dim in sorted(results.keys()):
        r = results[dim]
        known = str(r['known_record']) if r['known_record'] else "N/A"
        matches = "✓" if r['matches_known'] else "✗"
        valid = "✓" if r['is_valid'] else "✗"
        html.append(
            f"<tr><td>{dim}</td><td>{r['length']}</td><td>{valid}</td>"
            f"<td>{r['method']}</td><td>{known}</td><td>{matches}</td>"
            f"<td>{r['search_time']:.2f}</td></tr>"
        )
    
    html.append("</table>")
    html.append("</body>")
    html.append("</html>")
    
    return "\n".join(html)


def generate_validation_report(
    results: Dict[int, Dict],
    output_file: str = "validation_report.md"
) -> str:
    """Generate validation report.
    
    Parameters
    ----------
    results : Dict[int, Dict]
        Analysis results
    output_file : str, optional
        Output file path (default: "validation_report.md")
    
    Returns
    -------
    str
        Report content
    """
    lines = []
    
    lines.append("# Snake-in-the-Box Validation Report")
    lines.append("")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    
    lines.append("## Validation Summary")
    lines.append("")
    
    valid_count = sum(1 for r in results.values() if r['is_valid'])
    invalid_count = len(results) - valid_count
    
    lines.append(f"- **Total Dimensions**: {len(results)}")
    lines.append(f"- **Valid Snakes**: {valid_count}")
    lines.append(f"- **Invalid Snakes**: {invalid_count}")
    lines.append("")
    
    lines.append("## Validation Details")
    lines.append("")
    
    for dim in sorted(results.keys()):
        r = results[dim]
        lines.append(f"### Dimension {dim}")
        lines.append("")
        lines.append(f"- **Valid**: {'✓ Yes' if r['is_valid'] else '✗ No'}")
        lines.append(f"- **Length**: {r['length']}")
        
        if r['validation_message']:
            lines.append(f"- **Message**: {r['validation_message']}")
        
        if not r['is_valid']:
            lines.append(f"- **Error**: Validation failed")
        
        lines.append("")
    
    content = "\n".join(lines)
    
    with open(output_file, 'w') as f:
        f.write(content)
    
    return content


def generate_performance_report(
    results: Dict[int, Dict],
    output_file: str = "performance_report.md"
) -> str:
    """Generate performance report.
    
    Parameters
    ----------
    results : Dict[int, Dict]
        Analysis results
    output_file : str, optional
        Output file path (default: "performance_report.md")
    
    Returns
    -------
    str
        Report content
    """
    lines = []
    
    lines.append("# Snake-in-the-Box Performance Report")
    lines.append("")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    
    stats = generate_statistics(results)
    
    lines.append("## Performance Summary")
    lines.append("")
    lines.append(f"- **Total Time**: {stats['total_time']:.2f} seconds")
    lines.append(f"- **Average Time per Dimension**: {stats['average_time']:.2f} seconds")
    lines.append(f"- **Dimensions from Search**: {stats['from_search']}")
    lines.append(f"- **Dimensions from Known**: {stats['from_known']}")
    lines.append("")
    
    lines.append("## Performance by Dimension")
    lines.append("")
    lines.append("| Dimension | Method | Time (s) | Length |")
    lines.append("|-----------|--------|----------|--------|")
    
    for dim in sorted(results.keys()):
        r = results[dim]
        method = r.get('method', 'unknown')
        time_val = r.get('search_time', 0.0)
        length = r.get('length', 0)
        lines.append(f"| {dim} | {method} | {time_val:.2f} | {length} |")
    
    lines.append("")
    
    content = "\n".join(lines)
    
    # Create directory if needed (handle case where dirname is empty)
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    with open(output_file, 'w') as f:
        f.write(content)
    
    return content


def generate_exponential_analysis_report(
    results: Dict[int, Dict],
    output_file: str = "output/reports/exponential_analysis.md"
) -> str:
    """Generate exponential slowdown analysis report.
    
    Parameters
    ----------
    results : Dict[int, Dict]
        Analysis results with computation times
    output_file : str, optional
        Output file path
    
    Returns
    -------
    str
        Report content
    """
    # Extract computation times
    times = {}
    for dim, result in results.items():
        time_val = result.get('computation_time_seconds') or result.get('search_time', 0.0)
        if time_val > 0:
            times[dim] = time_val
    
    if not times:
        return "No timing data available for exponential analysis."
    
    # Run exponential analysis
    complexity = analyze_computation_complexity(times)
    slowdown_points = identify_slowdown_points(times)
    model = fit_exponential_model(times)
    
    lines = []
    lines.append("# Exponential Slowdown Analysis Report")
    lines.append("")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    
    # Summary
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Complexity Class**: {complexity['complexity_class']}")
    lines.append(f"- **Average Growth Factor**: {complexity['average_growth_factor']:.3f}")
    lines.append(f"- **Exponential Regions**: {len(complexity['exponential_regions'])}")
    lines.append(f"- **Slowdown Points**: {len(slowdown_points)}")
    lines.append(f"- **Model R-squared**: {model['r_squared']:.4f}")
    lines.append("")
    
    # Growth factors
    if complexity['growth_factors']:
        lines.append("## Growth Factors")
        lines.append("")
        lines.append("| Dimension | Time (s) | Growth Factor |")
        lines.append("|-----------|----------|---------------|")
        
        dimensions = sorted(times.keys())
        for i, dim in enumerate(dimensions):
            time_val = times[dim]
            growth = complexity['growth_factors'].get(dim, '-')
            if isinstance(growth, float):
                growth_str = f"{growth:.3f}x"
            else:
                growth_str = str(growth)
            lines.append(f"| {dim} | {time_val:.6f} | {growth_str} |")
        lines.append("")
    
    # Exponential regions
    if complexity['exponential_regions']:
        lines.append("## Exponential Growth Regions")
        lines.append("")
        for start, end in complexity['exponential_regions']:
            lines.append(f"- **Dimensions {start}-{end}**: Exponential growth (factor >= 1.5)")
        lines.append("")
    
    # Slowdown points
    if slowdown_points:
        lines.append("## Critical Slowdown Points")
        lines.append("")
        lines.append("Dimensions where computation time doubles or more:")
        lines.append("")
        for dim in slowdown_points:
            time_val = times[dim]
            lines.append(f"- **Dimension {dim}**: {time_val:.6f}s (doubling point)")
        lines.append("")
    
    # Model fit
    lines.append("## Exponential Model")
    lines.append("")
    lines.append(f"Fitted model: **time(N) = {model['coefficient']:.6e} × {model['base']:.6f}^N**")
    lines.append(f"R-squared: {model['r_squared']:.4f}")
    lines.append("")
    
    if model['r_squared'] > 0.5:
        lines.append("### Time Estimates for Higher Dimensions")
        lines.append("")
        lines.append("| Dimension | Estimated Time (seconds) | Estimated Time (hours) |")
        lines.append("|-----------|-------------------------|------------------------|")
        
        max_dim = max(times.keys())
        for N in range(max_dim + 1, max_dim + 5):
            est_seconds = estimate_time_for_dimension(N, model)
            est_hours = est_seconds / 3600.0
            if est_hours < 1:
                time_str = f"{est_seconds:.2f}s"
            elif est_hours < 24:
                time_str = f"{est_hours:.2f} hours"
            else:
                time_str = f"{est_hours/24:.2f} days"
            lines.append(f"| {N} | {est_seconds:.2e} | {time_str} |")
        lines.append("")
    
    # Interpretation
    lines.append("## Interpretation")
    lines.append("")
    if complexity['complexity_class'] == 'exponential':
        lines.append("The computation time shows **exponential growth**, meaning each")
        lines.append("dimension increase multiplies computation time by a constant factor.")
        lines.append("This is expected for NP-hard problems like snake-in-the-box.")
    elif complexity['complexity_class'] == 'super_linear':
        lines.append("The computation time shows **super-linear growth**, faster than")
        lines.append("linear but not fully exponential. This suggests effective pruning")
        lines.append("is reducing the search space.")
    else:
        lines.append("The computation time shows **sub-exponential growth**, suggesting")
        lines.append("effective heuristics are controlling the search space explosion.")
    lines.append("")
    
    content = "\n".join(lines)
    
    # Create directory if needed (handle case where dirname is empty)
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    with open(output_file, 'w') as f:
        f.write(content)
    
    return content

