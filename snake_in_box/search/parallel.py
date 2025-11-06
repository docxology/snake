"""Parallel search implementation."""

from typing import List, Optional, Tuple
from multiprocessing import Pool, Manager
import multiprocessing as mp
from ..core.snake_node import SnakeNode
from .bfs_pruned import (
    is_valid_extension,
    estimate_memory_usage,
    prune_by_fitness,
    estimate_node_size,
)


def parallel_search(
    dimension: int,
    memory_limit_gb: float = 18.0,
    num_workers: int = 10,
    verbose: bool = True
) -> Optional[SnakeNode]:
    """Parallel search distributing node expansion across workers.
    
    Parameters
    ----------
    dimension : int
        Dimension of hypercube
    memory_limit_gb : float, optional
        Maximum memory in gigabytes (default: 18)
    num_workers : int, optional
        Number of parallel workers (default: 10, matching paper)
    verbose : bool, optional
        Print progress (default: True)
    
    Returns
    -------
    Optional[SnakeNode]
        Best snake found, or None if search fails
    """
    from ..core.snake_node import SnakeNode
    from ..utils.canonical import get_legal_next_dimensions
    
    # Initialize with empty snake
    current_level: List[SnakeNode] = [SnakeNode([], dimension)]
    best_snake: Optional[SnakeNode] = None
    max_length = 0
    
    level_count = 0
    
    # Shared state for best snake tracking
    manager = Manager()
    best_snake_lock = manager.Lock()
    best_snake_shared = manager.dict({'length': 0, 'sequence': []})
    
    while current_level:
        # Distribute current level nodes among workers
        chunk_size = max(1, len(current_level) // num_workers)
        chunks = [
            current_level[i:i + chunk_size]
            for i in range(0, len(current_level), chunk_size)
        ]
        
        # Expand nodes in parallel
        with Pool(num_workers) as pool:
            results = pool.starmap(
                expand_nodes_worker,
                [
                    (chunk, dimension, best_snake_shared, best_snake_lock)
                    for chunk in chunks
                ]
            )
        
        # Collect results from all workers
        next_level: List[SnakeNode] = []
        for worker_nodes in results:
            next_level.extend(worker_nodes)
        
        # Update best snake from shared state
        with best_snake_lock:
            if best_snake_shared['length'] > max_length:
                max_length = best_snake_shared['length']
                # Reconstruct best snake node
                best_snake = SnakeNode(
                    best_snake_shared['sequence'],
                    dimension
                )
                if verbose:
                    print(
                        f"Level {level_count + 1}: "
                        f"New best length {max_length}"
                    )
        
        # Prune combined results
        if estimate_memory_usage(next_level) > memory_limit_gb:
            if verbose:
                print(
                    f"Level {level_count + 1}: Pruning {len(next_level)} nodes "
                    f"to fit memory limit"
                )
            next_level = prune_by_fitness(next_level, memory_limit_gb)
        
        # Free memory from previous level
        del current_level
        current_level = next_level
        level_count += 1
        
        if verbose:
            print(
                f"Level {level_count}: {len(current_level)} nodes, "
                f"best length: {max_length}"
            )
        
        if not current_level:
            break
    
    return best_snake


def expand_nodes_worker(
    nodes: List[SnakeNode],
    dimension: int,
    best_snake_shared: dict,
    best_snake_lock
) -> List[SnakeNode]:
    """Worker function for parallel expansion.
    
    Expands a chunk of nodes and updates shared best snake state.
    
    Parameters
    ----------
    nodes : List[SnakeNode]
        Chunk of nodes to expand
    dimension : int
        Dimension of hypercube
    best_snake_shared : dict
        Shared dictionary for best snake tracking
    best_snake_lock : Lock
        Lock for thread-safe access to shared state
    
    Returns
    -------
    List[SnakeNode]
        Expanded child nodes
    """
    from ..utils.canonical import get_legal_next_dimensions
    
    expanded: List[SnakeNode] = []
    
    for node in nodes:
        legal_dims = get_legal_next_dimensions(node.transition_sequence)
        
        for dim in legal_dims:
            if is_valid_extension(node, dim):
                try:
                    child = node.create_child(dim)
                    expanded.append(child)
                    
                    # Update shared best snake
                    length = child.get_length()
                    with best_snake_lock:
                        if length > best_snake_shared['length']:
                            best_snake_shared['length'] = length
                            best_snake_shared['sequence'] = child.transition_sequence
                except ValueError:
                    continue
    
    return expanded



