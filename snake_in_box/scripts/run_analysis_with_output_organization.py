#!/usr/bin/env python3
"""Run complete analysis with organized output structure.

RECOMMENDED: This is the most comprehensive analysis script.

This script runs the full analysis and ensures all outputs are
organized in the output/ directory structure. It includes:
- Complete analysis for dimensions 1-16
- All report types (analysis, validation, performance, feasibility)
- Graphical abstract generation
- Individual visualizations
- Organized output directory structure

For simpler analysis without feasibility reports, use:
    run_analysis.py

For analysis with performance plots and exponential analysis, use:
    run_full_analysis.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from snake_in_box.analysis import analyze_dimensions, generate_analysis_report, generate_validation_report
from snake_in_box.analysis.dimension_feasibility import generate_feasibility_report
from snake_in_box.utils.graphical_abstract import generate_16d_panel
from snake_in_box.utils.visualize_advanced import (
    visualize_snake_auto,
    visualize_snake_heatmap,
    visualize_snake_3d_projection,
    visualize_snake_transition_matrix,
)
from snake_in_box.utils.export import export_analysis_data
from snake_in_box.scripts.generate_snakes_for_all_dimensions import get_snake_for_dimension


def main():
    """Run complete analysis with organized outputs."""
    # Ensure output directory structure exists
    output_base = "output"
    os.makedirs(f"{output_base}/reports", exist_ok=True)
    os.makedirs(f"{output_base}/visualizations", exist_ok=True)
    os.makedirs(f"{output_base}/graphical_abstracts", exist_ok=True)
    os.makedirs(f"{output_base}/test_outputs", exist_ok=True)
    os.makedirs(f"{output_base}/data", exist_ok=True)
    
    print("="*70)
    print("Snake-in-the-Box: Complete Analysis with Organized Outputs")
    print("="*70)
    print()
    
    # Step 1: Generate/retrieve snakes
    print("Step 1: Generating/retrieving snakes for dimensions 1-16...")
    snake_nodes = {}
    
    for dim in range(1, 17):
        print(f"  Dimension {dim}...", end=" ")
        node = get_snake_for_dimension(dim)
        if node:
            snake_nodes[dim] = node
            print(f"✓ (Length: {node.get_length()})")
        else:
            print("✗")
    
    print(f"\n  Generated {len(snake_nodes)} snakes")
    
    # Step 2: Analyze
    print("\n" + "="*70)
    print("Step 2: Analyzing dimensions...")
    
    results = {}
    for dim in range(1, 17):
        if dim in snake_nodes:
            from snake_in_box.analysis.analyze_dimensions import analyze_single_dimension
            result = analyze_single_dimension(
                dim,
                use_known=False,
                memory_limit_gb=0.5,
                verbose=False
            )
            result['snake_node'] = snake_nodes[dim]
            result['transition_sequence'] = snake_nodes[dim].transition_sequence
            result['length'] = snake_nodes[dim].get_length()
            result['method'] = 'generated'
            results[dim] = result
    
    # Step 3: Generate reports (in output/reports/)
    print("\n" + "="*70)
    print("Step 3: Generating reports...")
    
    generate_analysis_report(
        results, 
        f"{output_base}/reports/analysis_report.md", 
        format="markdown"
    )
    generate_analysis_report(
        results, 
        f"{output_base}/reports/analysis_report.html", 
        format="html"
    )
    generate_validation_report(
        results, 
        f"{output_base}/reports/validation_report.md"
    )
    from snake_in_box.analysis.reporting import generate_performance_report
    generate_performance_report(
        results, 
        f"{output_base}/reports/performance_report.md"
    )
    
    # Generate feasibility report
    generate_feasibility_report(f"{output_base}/reports/feasibility_analysis.md")
    
    print("  Generated reports in output/reports/")
    
    # Step 4: Generate graphical abstract (in output/graphical_abstracts/)
    print("\n" + "="*70)
    print("Step 4: Generating graphical abstract...")
    
    try:
        panel_nodes = {dim: snake_nodes[dim] for dim in snake_nodes.keys() if dim <= 16}
        if panel_nodes:
            generate_16d_panel(
                panel_nodes,
                output_file=f"{output_base}/graphical_abstracts/graphical_abstract_16d.png",
                figsize=(20, 20),
                dpi=300
            )
            print(f"  Generated: {output_base}/graphical_abstracts/graphical_abstract_16d.png")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Step 5: Generate individual visualizations (in output/visualizations/)
    print("\n" + "="*70)
    print("Step 5: Generating individual visualizations...")
    
    generated = 0
    for dim in range(1, 17):
        if dim in snake_nodes:
            try:
                # Standard visualization
                fig = visualize_snake_auto(snake_nodes[dim], show_plot=False)
                if fig:
                    fig.savefig(
                        f"{output_base}/visualizations/dimension_{dim:02d}.png",
                        dpi=150,
                        bbox_inches='tight'
                    )
                    import matplotlib.pyplot as plt
                    plt.close(fig)
                    generated += 1
                
                # Additional visualizations for dimensions >= 4
                if dim >= 4:
                    # Heatmap
                    try:
                        fig = visualize_snake_heatmap(snake_nodes[dim], show_plot=False)
                        if fig:
                            fig.savefig(
                                f"{output_base}/visualizations/dimension_{dim:02d}_heatmap.png",
                                dpi=150,
                                bbox_inches='tight'
                            )
                            plt.close(fig)
                    except Exception:
                        pass
                    
                    # 3D projection
                    try:
                        fig = visualize_snake_3d_projection(snake_nodes[dim], show_plot=False)
                        if fig:
                            fig.savefig(
                                f"{output_base}/visualizations/dimension_{dim:02d}_3d.png",
                                dpi=150,
                                bbox_inches='tight'
                            )
                            plt.close(fig)
                    except Exception:
                        pass
                
                # Transition matrix for all dimensions
                try:
                    fig = visualize_snake_transition_matrix(snake_nodes[dim], show_plot=False)
                    if fig:
                        fig.savefig(
                            f"{output_base}/visualizations/dimension_{dim:02d}_transitions.png",
                            dpi=150,
                            bbox_inches='tight'
                        )
                        plt.close(fig)
                except Exception:
                    pass
                    
            except Exception as e:
                print(f"  Error visualizing dimension {dim}: {e}")
    
    print(f"  Generated {generated} standard visualizations + additional views in {output_base}/visualizations/")
    
    # Step 6: Save data files (in output/data/)
    print("\n" + "="*70)
    print("Step 6: Saving data files...")
    
    # Enhanced data export with comprehensive format
    exported_files = export_analysis_data(
        results,
        output_dir=f"{output_base}/data",
        include_sequences=True
    )
    
    print(f"  Saved comprehensive data:")
    for format_name, file_path in exported_files.items():
        print(f"    - {format_name}: {file_path}")
    
    # Also save simple format for backward compatibility
    import json
    data = {}
    for dim, result in results.items():
        data[dim] = {
            'dimension': result['dimension'],
            'length': result['length'],
            'is_valid': result['is_valid'],
            'method': result['method'],
            'transition_sequence': result.get('transition_sequence'),
        }
    
    with open(f"{output_base}/data/analysis_results.json", 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"  Also saved: {output_base}/data/analysis_results.json (backward compatibility)")
    
    # Summary
    print("\n" + "="*70)
    print("Analysis Complete!")
    print("="*70)
    print(f"\nAll outputs organized in: {output_base}/")
    print(f"  - Reports: {output_base}/reports/")
    print(f"  - Visualizations: {output_base}/visualizations/")
    print(f"  - Graphical Abstracts: {output_base}/graphical_abstracts/")
    print(f"  - Data: {output_base}/data/")


if __name__ == "__main__":
    main()

