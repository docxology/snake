"""Generate test outputs and calculations for dimensions 1-16.

Creates test data files, validation reports, and performance metrics.
"""

import os
import json
from datetime import datetime
from snake_in_box.analysis import analyze_dimensions, generate_statistics
from snake_in_box.benchmarks.known_snakes import KNOWN_RECORDS


def generate_test_data():
    """Generate test data files."""
    print("Generating test data files...")
    
    # Analyze dimensions 1-16
    results = analyze_dimensions(
        dimensions=list(range(1, 17)),
        use_known=True,
        memory_limit_gb=1.0,
        verbose=False
    )
    
    # Save results as JSON
    output_dir = "test_outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    # Convert results to JSON-serializable format
    json_results = {}
    for dim, result in results.items():
        json_results[dim] = {
            'dimension': result['dimension'],
            'length': result['length'],
            'is_valid': result['is_valid'],
            'validation_message': result['validation_message'],
            'known_record': result['known_record'],
            'matches_known': result['matches_known'],
            'search_time': result['search_time'],
            'method': result['method'],
            'transition_sequence': result['transition_sequence'] if result['transition_sequence'] else None,
        }
    
    with open(f"{output_dir}/analysis_results.json", 'w') as f:
        json.dump(json_results, f, indent=2)
    
    print(f"  Saved: {output_dir}/analysis_results.json")
    
    # Generate statistics
    stats = generate_statistics(results)
    
    with open(f"{output_dir}/statistics.json", 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"  Saved: {output_dir}/statistics.json")
    
    # Generate comparison table
    lines = []
    lines.append("Dimension | Length | Known Record | Matches | Valid")
    lines.append("-" * 60)
    
    for dim in sorted(results.keys()):
        r = results[dim]
        known = str(r['known_record']) if r['known_record'] else "N/A"
        matches = "Yes" if r['matches_known'] else "No"
        valid = "Yes" if r['is_valid'] else "No"
        lines.append(f"{dim:9} | {r['length']:6} | {known:12} | {matches:7} | {valid}")
    
    with open(f"{output_dir}/comparison_table.txt", 'w') as f:
        f.write("\n".join(lines))
    
    print(f"  Saved: {output_dir}/comparison_table.txt")
    
    return results


def generate_calculations():
    """Generate calculation outputs."""
    print("\nGenerating calculations...")
    
    output_dir = "test_outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    lines = []
    lines.append("Snake-in-the-Box Calculations")
    lines.append("=" * 60)
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    
    # Calculate theoretical maximums (upper bounds)
    lines.append("Theoretical Upper Bounds:")
    lines.append("")
    lines.append("Dimension | Vertices | Theoretical Max | Known Record")
    lines.append("-" * 60)
    
    for dim in range(1, 17):
        vertices = 2 ** dim
        # Upper bound: all vertices minus those adjacent to path
        # Rough estimate: vertices / (dim + 1)
        theoretical_max = vertices // (dim + 1)
        known = KNOWN_RECORDS.get(dim, "N/A")
        lines.append(f"{dim:9} | {vertices:8} | {theoretical_max:15} | {known}")
    
    lines.append("")
    
    # Calculate growth rates
    lines.append("Growth Rates (compared to previous dimension):")
    lines.append("")
    lines.append("Dimension | Length | Growth Factor | Vertices Growth")
    lines.append("-" * 60)
    
    prev_length = 0
    for dim in sorted(KNOWN_RECORDS.keys()):
        length = KNOWN_RECORDS[dim]
        if prev_length > 0:
            growth = length / prev_length
        else:
            growth = 0.0
        vertices_growth = 2.0  # Always doubles
        lines.append(f"{dim:9} | {length:6} | {growth:13.2f} | {vertices_growth:15.1f}")
        prev_length = length
    
    with open(f"{output_dir}/calculations.txt", 'w') as f:
        f.write("\n".join(lines))
    
    print(f"  Saved: {output_dir}/calculations.txt")


def main():
    """Generate all test outputs."""
    print("="*70)
    print("Generating Test Outputs and Calculations")
    print("="*70)
    print()
    
    results = generate_test_data()
    generate_calculations()
    
    print("\n" + "="*70)
    print("Test output generation complete!")
    print("="*70)


if __name__ == "__main__":
    main()

