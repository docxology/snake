#!/usr/bin/env python3
"""Run complete analysis for dimensions 1-16.

This is a simpler version of the analysis script.
For the most comprehensive analysis with organized outputs, use:
    run_analysis_with_output_organization.py

For analysis with performance plots and exponential analysis, use:
    run_full_analysis.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from snake_in_box.analysis import analyze_dimensions, generate_analysis_report, generate_validation_report
from snake_in_box.analysis.reporting import generate_performance_report
from snake_in_box.utils.graphical_abstract import generate_16d_panel
from snake_in_box.utils.visualize_advanced import visualize_snake_auto
from snake_in_box.scripts.generate_snakes_for_all_dimensions import get_snake_for_dimension


def main():
    """Run analysis and generate all outputs."""
    output_base = "output"
    os.makedirs(f"{output_base}/reports", exist_ok=True)
    os.makedirs(f"{output_base}/visualizations", exist_ok=True)
    os.makedirs(f"{output_base}/graphical_abstracts", exist_ok=True)
    os.makedirs(f"{output_base}/data", exist_ok=True)
    
    print("Generating snakes for dimensions 1-16...")
    snake_nodes = {}
    for dim in range(1, 17):
        node = get_snake_for_dimension(dim)
        if node:
            snake_nodes[dim] = node
            print(f"  Dimension {dim}: Length {node.get_length()}")
    
    print(f"\nAnalyzing {len(snake_nodes)} dimensions...")
    results = {}
    for dim in range(1, 17):
        if dim in snake_nodes:
            from snake_in_box.analysis.analyze_dimensions import analyze_single_dimension
            result = analyze_single_dimension(dim, use_known=False, memory_limit_gb=0.5, verbose=False)
            result['snake_node'] = snake_nodes[dim]
            result['transition_sequence'] = snake_nodes[dim].transition_sequence
            result['length'] = snake_nodes[dim].get_length()
            result['method'] = 'generated'
            results[dim] = result
    
    print("Generating reports...")
    generate_analysis_report(results, f"{output_base}/reports/analysis_report.md", format="markdown")
    generate_analysis_report(results, f"{output_base}/reports/analysis_report.html", format="html")
    generate_validation_report(results, f"{output_base}/reports/validation_report.md")
    generate_performance_report(results, f"{output_base}/reports/performance_report.md")
    
    print("Generating graphical abstract...")
    panel_nodes = {dim: snake_nodes[dim] for dim in snake_nodes.keys() if dim <= 16}
    if panel_nodes:
        generate_16d_panel(panel_nodes, output_file=f"{output_base}/graphical_abstracts/graphical_abstract_16d.png", figsize=(20, 20), dpi=300)
    
    print("Generating visualizations...")
    for dim in range(1, 17):
        if dim in snake_nodes:
            try:
                fig = visualize_snake_auto(snake_nodes[dim], show_plot=False)
                if fig:
                    fig.savefig(f"{output_base}/visualizations/dimension_{dim:02d}.png", dpi=150, bbox_inches='tight')
                    import matplotlib.pyplot as plt
                    plt.close(fig)
            except Exception:
                pass
    
    print("Saving data...")
    import json
    data = {dim: {'dimension': r['dimension'], 'length': r['length'], 'is_valid': r['is_valid'], 'method': r['method'], 'transition_sequence': r.get('transition_sequence')} for dim, r in results.items()}
    with open(f"{output_base}/data/analysis_results.json", 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\nComplete. Outputs in {output_base}/")


if __name__ == "__main__":
    main()

