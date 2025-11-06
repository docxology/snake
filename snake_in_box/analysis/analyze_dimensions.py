"""Analysis module for dimensions 1-16."""

from typing import Dict, List, Optional, Tuple
import time
from ..core.snake_node import SnakeNode
from ..core.validation import validate_transition_sequence
from ..benchmarks.known_snakes import get_known_record, get_known_snake, KNOWN_RECORDS


def analyze_single_dimension(
    dimension: int,
    use_known: bool = True,
    memory_limit_gb: float = 2.0,
    verbose: bool = False
) -> Dict:
    """Analyze a single dimension using modular calculation.
    
    Parameters
    ----------
    dimension : int
        Dimension to analyze
    use_known : bool, optional
        Use known snake if available (default: True)
    memory_limit_gb : float, optional
        Memory limit for search (default: 2.0)
    verbose : bool, optional
        Print progress (default: False)
    
    Returns
    -------
    Dict
        Analysis result containing:
        - dimension: int
        - snake_node: SnakeNode or None
        - transition_sequence: List[int] or None
        - length: int
        - is_valid: bool
        - validation_message: str
        - known_record: int or None
        - matches_known: bool
        - search_time: float (computation time in seconds)
        - computation_time_seconds: float
        - computation_time_hours: float
        - method: str ('known', 'search', 'priming', 'failed')
        - metadata: Dict with search statistics
    """
    # Use modular calculation function (lazy import to avoid circular dependency)
    from ..core.calculation import calculate_snake_for_dimension
    
    calc_result = calculate_snake_for_dimension(
        N=dimension,
        use_known=use_known,
        memory_limit_gb=memory_limit_gb,
        verbose=verbose
    )
    
    result = {
        'dimension': dimension,
        'snake_node': calc_result.get('snake_node'),
        'transition_sequence': calc_result.get('snake_node').transition_sequence if calc_result.get('snake_node') else None,
        'length': calc_result.get('length', 0),
        'is_valid': calc_result.get('is_valid', False),
        'validation_message': '',
        'known_record': get_known_record(dimension),
        'matches_known': False,
        'search_time': calc_result.get('computation_time_seconds', 0.0),
        'computation_time_seconds': calc_result.get('computation_time_seconds', 0.0),
        'computation_time_hours': calc_result.get('computation_time_hours', 0.0),
        'method': calc_result.get('method', 'failed'),
        'metadata': calc_result.get('metadata', {})
    }
    
    # Validate if we have a snake
    if result['transition_sequence']:
        is_valid, msg = validate_transition_sequence(
            result['transition_sequence'],
            dimension
        )
        result['is_valid'] = is_valid
        result['validation_message'] = msg
        
        # Check if matches known record
        if result.get('known_record'):
            result['matches_known'] = (result['length'] >= result['known_record'])
        else:
            result['matches_known'] = False
    else:
        result['validation_message'] = calc_result.get('metadata', {}).get('error', 'No snake found')
    
    return result


def analyze_dimensions(
    dimensions: List[int],
    use_known: bool = True,
    memory_limit_gb: float = 2.0,
    verbose: bool = False
) -> Dict[int, Dict]:
    """Analyze multiple dimensions.
    
    Parameters
    ----------
    dimensions : List[int]
        List of dimensions to analyze
    use_known : bool, optional
        Use known snakes if available (default: True)
    memory_limit_gb : float, optional
        Memory limit for search (default: 2.0)
    verbose : bool, optional
        Print progress (default: False)
    
    Returns
    -------
    Dict[int, Dict]
        Dictionary mapping dimension to analysis result
    """
    results = {}
    
    for dim in dimensions:
        if verbose:
            print(f"\n{'='*60}")
            print(f"Analyzing dimension {dim}")
            print(f"{'='*60}")
        
        results[dim] = analyze_single_dimension(
            dimension=dim,
            use_known=use_known,
            memory_limit_gb=memory_limit_gb,
            verbose=verbose
        )
        
        if verbose:
            result = results[dim]
            print(f"Dimension {dim}:")
            print(f"  Length: {result['length']}")
            print(f"  Valid: {result['is_valid']}")
            print(f"  Method: {result['method']}")
            if result['known_record']:
                print(f"  Known record: {result['known_record']}")
                print(f"  Matches: {result['matches_known']}")
            print(f"  Time: {result['search_time']:.2f}s")
    
    return results


def generate_statistics(results: Dict[int, Dict]) -> Dict:
    """Generate statistics from analysis results.
    
    Parameters
    ----------
    results : Dict[int, Dict]
        Analysis results
    
    Returns
    -------
    Dict
        Statistics dictionary
    """
    stats = {
        'total_dimensions': len(results),
        'valid_snakes': 0,
        'invalid_snakes': 0,
        'from_known': 0,
        'from_search': 0,
        'matches_known': 0,
        'total_time': 0.0,
        'average_time': 0.0,
        'total_length': 0,
        'average_length': 0.0,
        'max_length': 0,
        'min_length': float('inf'),
    }
    
    for dim, result in results.items():
        if result['is_valid']:
            stats['valid_snakes'] += 1
        else:
            stats['invalid_snakes'] += 1
        
        if result['method'] == 'known':
            stats['from_known'] += 1
        elif result['method'] == 'search':
            stats['from_search'] += 1
        
        if result['matches_known']:
            stats['matches_known'] += 1
        
        stats['total_time'] += result['search_time']
        stats['total_length'] += result['length']
        
        if result['length'] > stats['max_length']:
            stats['max_length'] = result['length']
        if result['length'] < stats['min_length']:
            stats['min_length'] = result['length']
    
    if stats['total_dimensions'] > 0:
        stats['average_time'] = stats['total_time'] / stats['total_dimensions']
        stats['average_length'] = stats['total_length'] / stats['total_dimensions']
    
    if stats['min_length'] == float('inf'):
        stats['min_length'] = 0
    
    return stats

