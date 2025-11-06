"""Export functions for snake results."""

import json
import csv
from typing import Optional, Dict, List, Any
from datetime import datetime
from ..core.snake_node import SnakeNode
from ..core.transitions import transition_to_vertex


def export_snake(
    snake_node: SnakeNode,
    filename: str,
    include_vertices: bool = True
) -> None:
    """Export snake to file in multiple formats.
    
    Exports to:
    - JSON file with full metadata
    - Text file with comma-separated transition sequence (paper format)
    
    Parameters
    ----------
    snake_node : SnakeNode
        Snake node to export
    filename : str
        Base filename (without extension)
    include_vertices : bool, optional
        Include vertex sequence in JSON (default: True)
    
    Examples
    --------
    >>> result = pruned_bfs_search(dimension=7)
    >>> export_snake(result, 'snake_7d')
    # Creates snake_7d.json and snake_7d.txt
    """
    # Prepare data dictionary
    data = {
        'dimension': snake_node.dimension,
        'length': snake_node.get_length(),
        'transition_sequence': snake_node.transition_sequence,
        'fitness': snake_node.fitness,
    }
    
    if include_vertices:
        data['vertex_sequence'] = transition_to_vertex(
            snake_node.transition_sequence,
            snake_node.dimension
        )
    
    # Export JSON
    json_filename = filename if filename.endswith('.json') else filename + '.json'
    with open(json_filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    # Export text format (comma-separated transitions, paper format)
    txt_filename = filename if filename.endswith('.txt') else filename + '.txt'
    with open(txt_filename, 'w') as f:
        # Convert to hex string format (0-9, a-f)
        hex_string = ''.join(
            format(t, 'x') if t < 10 else chr(ord('a') + t - 10)
            for t in snake_node.transition_sequence
        )
        f.write(hex_string)
    
    # Also export comma-separated format
    csv_filename = filename + '_comma.txt'
    with open(csv_filename, 'w') as f:
        f.write(','.join(map(str, snake_node.transition_sequence)))


def export_analysis_data(
    results: Dict[int, Dict],
    output_dir: str = "output/data",
    include_sequences: bool = True
) -> Dict[str, str]:
    """Export comprehensive analysis data in multiple formats.
    
    Parameters
    ----------
    results : Dict[int, Dict]
        Analysis results dictionary mapping dimension to result data
    output_dir : str, optional
        Output directory (default: "output/data")
    include_sequences : bool, optional
        Include transition sequences in exports (default: True)
    
    Returns
    -------
    Dict[str, str]
        Dictionary mapping format name to file path
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    exported_files = {}
    
    # Prepare comprehensive data
    comprehensive_data = {
        'metadata': {
            'export_date': datetime.now().isoformat(),
            'total_dimensions': len(results),
            'dimensions_analyzed': sorted(results.keys())
        },
        'results': {}
    }
    
    for dim, result in results.items():
        dim_data = {
            'dimension': dim,
            'length': result.get('length', 0),
            'is_valid': result.get('is_valid', False),
            'method': result.get('method', 'unknown'),
            'fitness': result.get('fitness', 0),
            'computation_time_seconds': result.get('computation_time_seconds', 0.0),
            'computation_time_hours': result.get('computation_time_hours', 0.0),
            'known_record': result.get('known_record'),
            'matches_known': result.get('matches_known', False),
            'validation_message': result.get('validation_message', ''),
        }
        
        if include_sequences and 'transition_sequence' in result:
            dim_data['transition_sequence'] = result['transition_sequence']
            if 'vertex_sequence' in result:
                dim_data['vertex_sequence'] = result['vertex_sequence']
        
        if 'metadata' in result:
            dim_data['metadata'] = result['metadata']
        
        comprehensive_data['results'][dim] = dim_data
    
    # Export JSON
    json_path = os.path.join(output_dir, 'analysis_results_comprehensive.json')
    with open(json_path, 'w') as f:
        json.dump(comprehensive_data, f, indent=2)
    exported_files['json'] = json_path
    
    # Export CSV summary
    csv_path = os.path.join(output_dir, 'analysis_summary.csv')
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'dimension', 'length', 'is_valid', 'method', 'fitness',
            'computation_time_seconds', 'computation_time_hours',
            'known_record', 'matches_known'
        ])
        
        for dim in sorted(results.keys()):
            result = results[dim]
            writer.writerow([
                dim,
                result.get('length', 0),
                result.get('is_valid', False),
                result.get('method', 'unknown'),
                result.get('fitness', 0),
                result.get('computation_time_seconds', 0.0),
                result.get('computation_time_hours', 0.0),
                result.get('known_record', ''),
                result.get('matches_known', False)
            ])
    exported_files['csv'] = csv_path
    
    # Export statistics summary
    stats = {
        'total_dimensions': len(results),
        'valid_snakes': sum(1 for r in results.values() if r.get('is_valid', False)),
        'invalid_snakes': sum(1 for r in results.values() if not r.get('is_valid', False)),
        'from_known': sum(1 for r in results.values() if r.get('method') == 'known'),
        'from_search': sum(1 for r in results.values() if r.get('method') == 'search'),
        'from_priming': sum(1 for r in results.values() if r.get('method') == 'priming'),
        'total_length': sum(r.get('length', 0) for r in results.values()),
        'average_length': sum(r.get('length', 0) for r in results.values()) / len(results) if results else 0,
        'total_time_seconds': sum(r.get('computation_time_seconds', 0.0) for r in results.values()),
        'total_time_hours': sum(r.get('computation_time_hours', 0.0) for r in results.values()),
    }
    
    stats_path = os.path.join(output_dir, 'statistics.json')
    with open(stats_path, 'w') as f:
        json.dump(stats, f, indent=2)
    exported_files['statistics'] = stats_path
    
    return exported_files



