"""Heuristically-pruned breadth-first search algorithm."""

from typing import List, Optional, Dict, Tuple
import sys
import time
from ..core.snake_node import SnakeNode
from ..utils.canonical import get_legal_next_dimensions
from .fitness import SimpleFitnessEvaluator


def pruned_bfs_search(
    dimension: int,
    memory_limit_gb: float = 18.0,
    verbose: bool = True
) -> Optional[SnakeNode]:
    """Execute heuristically-pruned breadth-first search for snake-in-the-box.
    
    This implements the algorithm from Ace (2025) that discovered record-breaking
    snakes in dimensions 11-13. The search performs level-by-level expansion of
    a search tree, pruning nodes when memory constraints are exceeded based on
    a fitness heuristic.
    
    Parameters
    ----------
    dimension : int
        Dimension of hypercube to search (n in Q_n)
    memory_limit_gb : float, optional
        Maximum memory usage in gigabytes (default: 18)
    fitness_function : str, optional
        Fitness measure for pruning: 'unmarked_count' (default)
    verbose : bool, optional
        Print progress information (default: True)
    
    Returns
    -------
    Optional[SnakeNode]
        Best snake found, containing:
        - transition_sequence: list of int
        - dimension: int
        - fitness: float
        - vertices_bitmap: HypercubeBitmap
        Returns None if search fails
    
    Examples
    --------
    >>> result = pruned_bfs_search(dimension=7)
    >>> print(f"Found snake of length {result.get_length()}")
    Found snake of length 50
    """
    # Initialize with empty snake at origin
    current_level: List[SnakeNode] = [SnakeNode([], dimension)]
    best_snake: Optional[SnakeNode] = None
    max_length = 0
    
    level_count = 0
    start_time = time.time()
    level_times = []
    total_nodes_explored = 0
    
    while current_level:
        level_start_time = time.time()
        next_level: List[SnakeNode] = []
        
        # Generate all children for current level
        for node in current_level:
            # Get legal next dimensions (canonical form)
            legal_dims = get_legal_next_dimensions(node.transition_sequence)
            
            for dim in legal_dims:
                # Check if extension is valid
                if is_valid_extension(node, dim):
                    try:
                        child = node.create_child(dim)
                        next_level.append(child)
                        total_nodes_explored += 1
                        
                        # Track best snake found
                        child_length = child.get_length()
                        if child_length > max_length:
                            max_length = child_length
                            best_snake = child
                            if verbose:
                                print(
                                    f"Level {level_count + 1}: "
                                    f"New best length {max_length}"
                                )
                    except ValueError:
                        # Extension invalid, skip
                        continue
        
        # Prune if memory limit exceeded
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
        
        level_elapsed = time.time() - level_start_time
        level_times.append(level_elapsed)
        
        if verbose:
            print(
                f"Level {level_count}: {len(current_level)} nodes, "
                f"best length: {max_length}, time: {level_elapsed:.3f}s"
            )
        
        # Stop if no more nodes to expand
        if not current_level:
            break
    
    total_time = time.time() - start_time
    
    # Store timing metadata in snake node if possible
    if best_snake and hasattr(best_snake, '__dict__'):
        best_snake._search_metadata = {
            'total_time': total_time,
            'level_count': level_count,
            'nodes_explored': total_nodes_explored,
            'level_times': level_times
        }
    
    if verbose:
        print(f"Search completed: {total_time:.2f}s, {level_count} levels, {total_nodes_explored} nodes explored")
    
    return best_snake


def is_valid_extension(node: SnakeNode, new_dimension: int) -> bool:
    """Check if snake can be extended with given dimension.
    
    Parameters
    ----------
    node : SnakeNode
        Current snake node
    new_dimension : int
        Dimension (bit position) to extend in
    
    Returns
    -------
    bool
        True if extension is valid
    """
    return node.can_extend(new_dimension)


def prune_by_fitness(
    nodes: List[SnakeNode],
    memory_limit_gb: float
) -> List[SnakeNode]:
    """Prune nodes by fitness to fit within memory limit.
    
    Sorts nodes by fitness (unmarked vertex count) in descending order
    and keeps only the top nodes that fit within memory constraints.
    
    Parameters
    ----------
    nodes : List[SnakeNode]
        List of nodes to prune
    memory_limit_gb : float
        Maximum memory in gigabytes
    
    Returns
    -------
    List[SnakeNode]
        Pruned list of nodes
    """
    if not nodes:
        return nodes
    
    # Calculate memory threshold
    bytes_per_node = estimate_node_size(nodes[0])
    max_nodes = int((memory_limit_gb * 1024**3) / bytes_per_node)
    
    if len(nodes) <= max_nodes:
        return nodes
    
    # Sort by fitness (unmarked vertex count) descending
    nodes.sort(key=lambda n: n.fitness, reverse=True)
    
    # Keep top nodes within memory limit
    return nodes[:max_nodes]


def estimate_memory_usage(nodes: List[SnakeNode]) -> float:
    """Estimate memory usage for a list of nodes.
    
    Parameters
    ----------
    nodes : List[SnakeNode]
        List of nodes
    
    Returns
    -------
    float
        Estimated memory usage in gigabytes
    """
    if not nodes:
        return 0.0
    
    bytes_per_node = estimate_node_size(nodes[0])
    total_bytes = len(nodes) * bytes_per_node
    return total_bytes / (1024**3)  # Convert to GB


def estimate_node_size(node: SnakeNode) -> int:
    """Estimate memory size of a node in bytes.
    
    Estimates include:
    - Transition sequence list
    - Bitmap array
    - Python object overhead
    
    Parameters
    ----------
    node : SnakeNode
        Node to estimate size for
    
    Returns
    -------
    int
        Estimated size in bytes
    """
    # Transition sequence: list overhead + ints
    transition_size = sys.getsizeof(node.transition_sequence)
    transition_size += len(node.transition_sequence) * sys.getsizeof(0)
    
    # Bitmap: array overhead + 64-bit words
    bitmap_size = sys.getsizeof(node.vertices_bitmap.bitmap)
    bitmap_size += node.vertices_bitmap.num_words * 8  # 8 bytes per 64-bit word
    
    # Object overhead (rough estimate)
    object_overhead = 200
    
    return transition_size + bitmap_size + object_overhead


def estimate_branching_factor(nodes: List[SnakeNode]) -> int:
    """Estimate average branching factor for next level.
    
    Parameters
    ----------
    nodes : List[SnakeNode]
        Current level nodes
    
    Returns
    -------
    int
        Estimated number of children
    """
    if not nodes:
        return 0
    
    # Rough estimate: average legal dimensions per node
    total_legal = 0
    for node in nodes[:min(100, len(nodes))]:  # Sample first 100
        legal_dims = get_legal_next_dimensions(node.transition_sequence)
        total_legal += len(legal_dims)
    
    avg_legal = total_legal / min(100, len(nodes))
    
    # Estimate children (assuming some extensions are invalid)
    estimated_children = int(len(nodes) * avg_legal * 0.5)  # 50% valid
    
    return estimated_children

