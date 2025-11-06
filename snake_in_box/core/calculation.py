"""Modular calculation function for snake-in-the-box.

Provides unified interface for calculating snakes for arbitrary dimension N.
"""

from typing import Dict, Optional
import time
from .snake_node import SnakeNode
from ..search.bfs_pruned import pruned_bfs_search
from ..search.priming import prime_search
from ..benchmarks.known_snakes import get_known_snake, get_known_record, KNOWN_RECORDS


def calculate_snake_for_dimension(
    N: int,
    use_known: bool = True,
    memory_limit_gb: float = 18.0,
    timeout_hours: float = None,
    verbose: bool = True
) -> Dict:
    """Calculate snake for dimension N.
    
    Unified function that handles all calculation strategies:
    - Known snakes (if available)
    - Direct search (for small dimensions)
    - Priming strategy (for high dimensions)
    
    Parameters
    ----------
    N : int
        Dimension of hypercube (must be >= 1)
    use_known : bool, optional
        Use known snake if available (default: True)
    memory_limit_gb : float, optional
        Memory limit for search in gigabytes (default: 18.0)
    timeout_hours : float, optional
        Maximum time to spend searching in hours (default: None, no timeout)
    verbose : bool, optional
        Print progress information (default: True)
    
    Returns
    -------
    Dict
        Dictionary containing:
        - snake_node: SnakeNode or None
        - computation_time_seconds: float
        - computation_time_hours: float
        - method: str ('known', 'search', 'priming', 'failed')
        - dimension: int
        - length: int
        - is_valid: bool
        - metadata: Dict with search statistics
    """
    if N < 1:
        raise ValueError(f"Dimension N must be >= 1, got {N}")
    
    start_time = time.time()
    result = {
        'snake_node': None,
        'computation_time_seconds': 0.0,
        'computation_time_hours': 0.0,
        'method': 'failed',
        'dimension': N,
        'length': 0,
        'is_valid': False,
        'metadata': {}
    }
    
    # Try known snake first
    if use_known and N in KNOWN_RECORDS:
        known_seq = get_known_snake(N)
        if known_seq:
            try:
                node = SnakeNode(known_seq, N)
                elapsed = time.time() - start_time
                result['snake_node'] = node
                result['computation_time_seconds'] = elapsed
                result['computation_time_hours'] = elapsed / 3600.0
                result['method'] = 'known'
                result['length'] = node.get_length()
                result['is_valid'] = True
                result['metadata'] = {
                    'known_record': get_known_record(N),
                    'matches_record': node.get_length() >= get_known_record(N)
                }
                if verbose:
                    print(f"Dimension {N}: Using known snake (length {result['length']})")
                return result
            except Exception as e:
                if verbose:
                    print(f"Dimension {N}: Error creating known snake: {e}")
    
    # For small dimensions (N <= 8), try direct search
    if N <= 8:
        if verbose:
            print(f"Dimension {N}: Running direct search...")
        try:
            node = pruned_bfs_search(
                dimension=N,
                memory_limit_gb=memory_limit_gb,
                verbose=verbose
            )
            elapsed = time.time() - start_time
            
            if node:
                result['snake_node'] = node
                result['computation_time_seconds'] = elapsed
                result['computation_time_hours'] = elapsed / 3600.0
                result['method'] = 'search'
                result['length'] = node.get_length()
                result['is_valid'] = True
                
                # Extract search metadata if available
                if hasattr(node, '_search_metadata'):
                    result['metadata'] = node._search_metadata
                else:
                    result['metadata'] = {'search_method': 'direct'}
                
                if verbose:
                    print(f"Dimension {N}: Search completed (length {result['length']}, {elapsed:.2f}s)")
                return result
        except Exception as e:
            if verbose:
                print(f"Dimension {N}: Search failed: {e}")
    
    # For high dimensions (N >= 9), try priming strategy
    if N >= 9:
        if verbose:
            print(f"Dimension {N}: Attempting priming strategy...")
        
        # Find best lower-dimensional snake to extend from
        seed_dim = None
        seed_seq = None
        
        # Try dimension N-1 first (most likely to extend)
        if N - 1 in KNOWN_RECORDS:
            seed_seq = get_known_snake(N - 1)
            if seed_seq:
                seed_dim = N - 1
        else:
            # Try recursively finding a known snake
            for lower_dim in range(N - 1, 0, -1):
                if lower_dim in KNOWN_RECORDS:
                    seed_seq = get_known_snake(lower_dim)
                    if seed_seq:
                        seed_dim = lower_dim
                        break
        
        if seed_seq and seed_dim:
            try:
                if verbose:
                    print(f"Dimension {N}: Extending from dimension {seed_dim} (length {len(seed_seq)})...")
                
                # For dimensions 14-16, be more aggressive with search
                if N >= 14:
                    if verbose:
                        print(f"Dimension {N}: Using extended search parameters for high dimension...")
                    # Use higher memory limit and more levels for high dimensions
                    extended_memory = min(memory_limit_gb * 1.5, 50.0)  # Up to 50GB
                    extended_seq = prime_search(
                        lower_dimension_snake=seed_seq,
                        target_dimension=N,
                        memory_limit_gb=extended_memory,
                        verbose=verbose
                    )
                else:
                    extended_seq = prime_search(
                        lower_dimension_snake=seed_seq,
                        target_dimension=N,
                        memory_limit_gb=memory_limit_gb,
                        verbose=verbose
                    )
                
                elapsed = time.time() - start_time
                
                if extended_seq and len(extended_seq) > len(seed_seq):
                    node = SnakeNode(extended_seq, N)
                    result['snake_node'] = node
                    result['computation_time_seconds'] = elapsed
                    result['computation_time_hours'] = elapsed / 3600.0
                    result['method'] = 'priming'
                    result['length'] = node.get_length()
                    result['is_valid'] = True
                    result['metadata'] = {
                        'seed_dimension': seed_dim,
                        'seed_length': len(seed_seq),
                        'extended_length': len(extended_seq),
                        'extension': len(extended_seq) - len(seed_seq)
                    }
                    
                    if verbose:
                        extension = len(extended_seq) - len(seed_seq)
                        print(f"Dimension {N}: Priming successful (length {result['length']}, +{extension}, {elapsed:.2f}s)")
                    return result
                elif extended_seq and len(extended_seq) == len(seed_seq):
                    # Same length - still valid but no extension found
                    node = SnakeNode(extended_seq, N)
                    result['snake_node'] = node
                    result['computation_time_seconds'] = elapsed
                    result['computation_time_hours'] = elapsed / 3600.0
                    result['method'] = 'priming'
                    result['length'] = node.get_length()
                    result['is_valid'] = True
                    result['metadata'] = {
                        'seed_dimension': seed_dim,
                        'seed_length': len(seed_seq),
                        'extended_length': len(extended_seq),
                        'note': 'Search attempted but no extension found - using seed as valid lower bound'
                    }
                    if verbose:
                        print(f"Dimension {N}: Priming attempted but no extension found (length {result['length']}, {elapsed:.2f}s)")
                    return result
                else:
                    if verbose:
                        print(f"Dimension {N}: Priming returned None - search failed")
            except Exception as e:
                if verbose:
                    print(f"Dimension {N}: Priming failed with error: {e}")
                import traceback
                if verbose:
                    traceback.print_exc()
    
    # If all methods failed, try direct search as last resort
    if verbose:
        print(f"Dimension {N}: Attempting direct search as last resort...")
    try:
        node = pruned_bfs_search(
            dimension=N,
            memory_limit_gb=memory_limit_gb,
            verbose=verbose
        )
        elapsed = time.time() - start_time
        
        if node:
            result['snake_node'] = node
            result['computation_time_seconds'] = elapsed
            result['computation_time_hours'] = elapsed / 3600.0
            result['method'] = 'search'
            result['length'] = node.get_length()
            result['is_valid'] = True
            result['metadata'] = {'search_method': 'direct_fallback'}
            return result
    except Exception as e:
        if verbose:
            print(f"Dimension {N}: Direct search also failed: {e}")
    
    # All methods failed
    elapsed = time.time() - start_time
    result['computation_time_seconds'] = elapsed
    result['computation_time_hours'] = elapsed / 3600.0
    result['method'] = 'failed'
    result['metadata'] = {'error': 'All calculation methods failed'}
    
    if verbose:
        print(f"Dimension {N}: All calculation methods failed")
    
    return result

