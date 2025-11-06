#!/usr/bin/env python3
"""Run full analysis for dimensions 1-16 with visualizations and performance plots.

This script includes:
- Full analysis with performance plots
- Exponential analysis and fitting
- Slowdown analysis
- Memory vs dimension plots

For the most comprehensive analysis with organized outputs and feasibility reports, use:
    run_analysis_with_output_organization.py
"""

import sys
import os
import time
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from snake_in_box.analysis import analyze_dimensions, generate_analysis_report, generate_validation_report
from snake_in_box.analysis.reporting import generate_performance_report, generate_exponential_analysis_report
from snake_in_box.utils.graphical_abstract import generate_16d_panel
from snake_in_box.utils.visualize_advanced import visualize_snake_auto
from snake_in_box.utils.performance_plots import (
    plot_computation_time_vs_dimension,
    plot_exponential_fit,
    plot_slowdown_analysis,
    plot_memory_vs_dimension,
)
from snake_in_box.scripts.generate_snakes_for_all_dimensions import get_snake_for_dimension
from snake_in_box.search import pruned_bfs_search
from snake_in_box.benchmarks.known_snakes import get_known_snake, KNOWN_RECORDS


def generate_snakes_all_dimensions():
    """Generate or retrieve snakes for all dimensions 1-16."""
    print("Generating snakes for dimensions 1-16...")
    snake_nodes = {}
    computation_times = {}
    
    for dim in range(1, 17):
        print(f"  Dimension {dim}...", end=" ", flush=True)
        start_time = time.time()
        
        # Try known snake first
        if dim in KNOWN_RECORDS:
            known_seq = get_known_snake(dim)
            if known_seq:
                from snake_in_box.core.snake_node import SnakeNode
                node = SnakeNode(known_seq, dim)
                snake_nodes[dim] = node
                elapsed = time.time() - start_time
                computation_times[dim] = elapsed
                print(f"✓ Known (Length: {node.get_length()}, Time: {elapsed:.3f}s)")
                continue
        
        # Try simple generation
        node = get_snake_for_dimension(dim)
        if node:
            elapsed = time.time() - start_time
            computation_times[dim] = elapsed
            snake_nodes[dim] = node
            print(f"✓ Generated (Length: {node.get_length()}, Time: {elapsed:.3f}s)")
        else:
            # For dimensions 14-16, use dimension 13 snake as lower bound
            # Full search requires extensive computational resources
            # The 13D snake provides a valid lower bound for higher dimensions
            if dim >= 14:
                if 13 in snake_nodes:
                    from snake_in_box.core.snake_node import SnakeNode
                    # Use 13D snake as lower bound (valid but not optimal)
                    lower_bound_seq = snake_nodes[13].transition_sequence
                    node = SnakeNode(lower_bound_seq, dim)
                    elapsed = time.time() - start_time
                    computation_times[dim] = elapsed
                    snake_nodes[dim] = node
                    print(f"⚠ Lower bound (Length: {node.get_length()}, Time: {elapsed:.3f}s)")
                else:
                    print("✗")
            # Try search for small dimensions
            elif dim <= 8:
                try:
                    node = pruned_bfs_search(dimension=dim, memory_limit_gb=2.0, verbose=False)
                    if node:
                        elapsed = time.time() - start_time
                        computation_times[dim] = elapsed
                        snake_nodes[dim] = node
                        print(f"✓ Search (Length: {node.get_length()}, Time: {elapsed:.3f}s)")
                    else:
                        print("✗")
                except Exception as e:
                    print(f"✗ ({e})")
            else:
                print("✗")
    
    return snake_nodes, computation_times


def create_performance_plots(snake_nodes, computation_times, output_dir="output"):
    """Create bar and scatter plots for performance analysis."""
    import matplotlib.pyplot as plt
    import numpy as np
    
    os.makedirs(f"{output_dir}/visualizations", exist_ok=True)
    
    dimensions = sorted([d for d in snake_nodes.keys()])
    lengths = [snake_nodes[d].get_length() for d in dimensions]
    times = [computation_times.get(d, 0.0) for d in dimensions]
    
    # Bar plot: Snake length by dimension
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(dimensions, lengths, color='steelblue', alpha=0.7)
    ax.set_xlabel('Dimension', fontsize=12)
    ax.set_ylabel('Snake Length', fontsize=12)
    ax.set_title('Snake Length by Dimension', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    ax.set_xticks(dimensions)
    
    # Add value labels on bars
    for bar, length in zip(bars, lengths):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{length}', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/visualizations/snake_length_by_dimension.png", dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  Created: {output_dir}/visualizations/snake_length_by_dimension.png")
    
    # Scatter plot: Computation time vs snake length
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Filter out zero times
    valid_data = [(l, t) for l, t in zip(lengths, times) if t > 0]
    if valid_data:
        valid_lengths, valid_times = zip(*valid_data)
        scatter = ax.scatter(valid_lengths, valid_times, s=100, alpha=0.6, c=dimensions[:len(valid_lengths)], 
                            cmap='viridis', edgecolors='black', linewidths=1)
        
        # Add dimension labels
        for i, (l, t, d) in enumerate(zip(valid_lengths, valid_times, dimensions[:len(valid_lengths)])):
            ax.annotate(f'D{d}', (l, t), xytext=(5, 5), textcoords='offset points', fontsize=8)
        
        ax.set_xlabel('Snake Length', fontsize=12)
        ax.set_ylabel('Computation Time (seconds)', fontsize=12)
        ax.set_title('Computation Time vs Snake Length', fontsize=14, fontweight='bold')
        ax.grid(alpha=0.3)
        ax.set_xscale('log')
        ax.set_yscale('log')
        
        plt.colorbar(scatter, ax=ax, label='Dimension')
        plt.tight_layout()
        plt.savefig(f"{output_dir}/visualizations/computation_time_vs_length.png", dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  Created: {output_dir}/visualizations/computation_time_vs_length.png")
    
    # Bar plot: Computation time by dimension
    if any(t > 0 for t in times):
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(dimensions, times, color='coral', alpha=0.7)
        ax.set_xlabel('Dimension', fontsize=12)
        ax.set_ylabel('Computation Time (seconds)', fontsize=12)
        ax.set_title('Computation Time by Dimension', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        ax.set_xticks(dimensions)
        ax.set_yscale('log')
        
        # Add value labels
        for bar, time_val in zip(bars, times):
            if time_val > 0:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{time_val:.3f}s', ha='center', va='bottom', fontsize=8, rotation=90)
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/visualizations/computation_time_by_dimension.png", dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  Created: {output_dir}/visualizations/computation_time_by_dimension.png")


def main():
    """Run complete analysis."""
    output_base = "output"
    os.makedirs(f"{output_base}/reports", exist_ok=True)
    os.makedirs(f"{output_base}/visualizations", exist_ok=True)
    os.makedirs(f"{output_base}/graphical_abstracts", exist_ok=True)
    os.makedirs(f"{output_base}/data", exist_ok=True)
    
    print("="*70)
    print("Full Analysis: Dimensions 1-16")
    print("="*70)
    print()
    
    # Step 1: Generate snakes using modular calculation
    snake_nodes, computation_times = generate_snakes_all_dimensions()
    print(f"\nGenerated {len(snake_nodes)} snakes")
    
    # Step 2: Analyze with proper time tracking
    print("\nAnalyzing dimensions...")
    results = {}
    for N in range(1, 17):
        if N in snake_nodes:
            from snake_in_box.analysis.analyze_dimensions import analyze_single_dimension
            result = analyze_single_dimension(N, use_known=True, memory_limit_gb=18.0, verbose=False)
            # Ensure we use the calculated snake and times
            result['snake_node'] = snake_nodes[N]
            result['transition_sequence'] = snake_nodes[N].transition_sequence
            result['length'] = snake_nodes[N].get_length()
            result['computation_time_seconds'] = computation_times.get(N, 0.0)
            result['computation_time_hours'] = computation_times.get(N, 0.0) / 3600.0
            results[N] = result
    
    # Step 3: Generate reports
    print("\nGenerating reports...")
    generate_analysis_report(results, f"{output_base}/reports/analysis_report.md", format="markdown")
    generate_analysis_report(results, f"{output_base}/reports/analysis_report.html", format="html")
    generate_validation_report(results, f"{output_base}/reports/validation_report.md")
    generate_performance_report(results, f"{output_base}/reports/performance_report.md")
    
    # Generate exponential analysis report
    print("Generating exponential analysis report...")
    generate_exponential_analysis_report(results, f"{output_base}/reports/exponential_analysis.md")
    
    # Step 4: Generate graphical abstract
    print("\nGenerating graphical abstract...")
    panel_nodes = {dim: snake_nodes[dim] for dim in snake_nodes.keys() if dim <= 16}
    if panel_nodes:
        generate_16d_panel(panel_nodes, output_file=f"{output_base}/graphical_abstracts/graphical_abstract_16d.png", 
                          figsize=(20, 20), dpi=300)
        print(f"  Created: {output_base}/graphical_abstracts/graphical_abstract_16d.png")
    
    # Step 5: Generate individual visualizations
    print("\nGenerating individual visualizations...")
    generated = 0
    for dim in range(1, 17):
        if dim in snake_nodes:
            try:
                fig = visualize_snake_auto(snake_nodes[dim], show_plot=False)
                if fig:
                    fig.savefig(f"{output_base}/visualizations/dimension_{dim:02d}.png", dpi=150, bbox_inches='tight')
                    import matplotlib.pyplot as plt
                    plt.close(fig)
                    generated += 1
            except Exception:
                pass
    print(f"  Generated {generated} visualizations")
    
    # Step 6: Create performance plots
    print("\nCreating performance plots...")
    create_performance_plots(snake_nodes, computation_times, output_base)
    
    # Create exponential analysis plots
    print("Creating exponential analysis plots...")
    times_dict = {N: computation_times.get(N, 0.0) for N in range(1, 17) if N in snake_nodes}
    if times_dict:
        plot_computation_time_vs_dimension(times_dict, f"{output_base}/visualizations/computation_time_vs_dimension.png")
        plot_exponential_fit(times_dict, f"{output_base}/visualizations/exponential_fit.png")
        plot_slowdown_analysis(times_dict, f"{output_base}/visualizations/slowdown_analysis.png")
        plot_memory_vs_dimension(list(range(1, 17)), f"{output_base}/visualizations/memory_vs_dimension.png")
    
    # Step 7: Save data with exponential analysis
    print("\nSaving data...")
    data = {}
    for N, result in results.items():
        data[N] = {
            'dimension': N,
            'length': result['length'],
            'is_valid': result['is_valid'],
            'method': result['method'],
            'computation_time_seconds': result.get('computation_time_seconds', 0.0),
            'computation_time_hours': result.get('computation_time_hours', 0.0),
            'transition_sequence': result.get('transition_sequence'),
            'metadata': result.get('metadata', {})
        }
    
    with open(f"{output_base}/data/analysis_results.json", 'w') as f:
        json.dump(data, f, indent=2)
    
    # Save computation times with metadata
    times_with_metadata = {}
    for N in range(1, 17):
        if N in computation_times:
            times_with_metadata[N] = {
                'computation_time_seconds': computation_times[N],
                'computation_time_hours': computation_times[N] / 3600.0,
                'method': results.get(N, {}).get('method', 'unknown')
            }
    
    with open(f"{output_base}/data/computation_times.json", 'w') as f:
        json.dump(times_with_metadata, f, indent=2)
    
    # Save exponential model parameters
    from snake_in_box.analysis.exponential_analysis import fit_exponential_model
    times_dict = {N: computation_times.get(N, 0.0) for N in range(1, 17) if N in snake_nodes}
    if times_dict:
        model = fit_exponential_model(times_dict)
        with open(f"{output_base}/data/exponential_model.json", 'w') as f:
            json.dump({
                'base': model['base'],
                'coefficient': model['coefficient'],
                'r_squared': model['r_squared'],
                'slope': model['slope'],
                'intercept': model['intercept']
            }, f, indent=2)
    
    print(f"\n{'='*70}")
    print("Analysis Complete!")
    print(f"{'='*70}")
    print(f"\nOutputs in: {output_base}/")
    print(f"  - Reports: {output_base}/reports/")
    print(f"  - Visualizations: {output_base}/visualizations/")
    print(f"  - Graphical Abstracts: {output_base}/graphical_abstracts/")
    print(f"  - Data: {output_base}/data/")


if __name__ == "__main__":
    main()

