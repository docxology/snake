"""Priming strategy for high-dimensional search."""

from typing import List, Optional, Dict
import time
from ..core.snake_node import SnakeNode
from .bfs_pruned import pruned_bfs_search


def detect_dimension(transition_sequence: List[int]) -> int:
    """Determine dimension from transition sequence.
    
    The dimension is one more than the maximum transition value,
    since transitions are 0-indexed.
    
    Parameters
    ----------
    transition_sequence : List[int]
        Transition sequence
    
    Returns
    -------
    int
        Detected dimension
    """
    if not transition_sequence:
        return 1  # Empty sequence, minimum dimension is 1
    
    return max(transition_sequence) + 1


def prime_search(
    lower_dimension_snake: List[int],
    target_dimension: int,
    memory_limit_gb: float = 18.0,
    verbose: bool = True
) -> Optional[List[int]]:
    """Extend a snake from dimension n to dimension n+1 or higher.
    
    This implements the priming strategy used in the paper, where a known
    good snake in a lower dimension is extended to a higher dimension.
    
    Parameters
    ----------
    lower_dimension_snake : List[int]
        Known good snake transition sequence in lower dimension
    target_dimension : int
        Target dimension to extend to
    memory_limit_gb : float, optional
        Maximum memory in gigabytes (default: 18)
    verbose : bool, optional
        Print progress (default: True)
    
    Returns
    -------
    Optional[List[int]]
        Extended snake transition sequence, or None if search fails.
        Returns the seed snake if no extension found but search was attempted.
    
    Examples
    --------
    >>> # Extend 9D snake to 10D
    >>> snake_9d = get_known_snake(9)
    >>> snake_10d = prime_search(snake_9d, 10)
    """
    current_snake = lower_dimension_snake
    current_dim = detect_dimension(current_snake)
    
    if current_dim >= target_dimension:
        if verbose:
            print(f"Snake already in dimension {current_dim}, target is {target_dimension}")
        return current_snake
    
    while current_dim < target_dimension:
        if verbose:
            print(f"Extending from dimension {current_dim} to {current_dim + 1}")
        
        # Create initial node seeded with current snake
        try:
            initial_node = SnakeNode(current_snake, current_dim + 1)
        except ValueError as e:
            if verbose:
                print(f"Error creating initial node: {e}")
            # Return current snake as fallback
            return current_snake
        
        # For high dimensions (14+), use more aggressive search
        if current_dim + 1 >= 14:
            max_levels = 200000  # Much more levels for high dimensions
            min_extension = 1  # Try to find at least 1 extension
            # Also increase memory limit for high dimensions
            search_memory = min(memory_limit_gb * 2.0, 50.0)
        else:
            max_levels = 50000
            min_extension = 1
            search_memory = memory_limit_gb
        
        # Run pruned BFS starting from this seed
        extended_snake_node = pruned_bfs_search_from_seed(
            initial_node,
            current_dim + 1,
            memory_limit_gb=search_memory if current_dim + 1 >= 14 else memory_limit_gb,
            max_levels=max_levels,
            min_extension=min_extension,
            verbose=verbose
        )
        
        if extended_snake_node is None:
            if verbose:
                print(f"Search failed to extend from dimension {current_dim}, using seed as fallback")
            # Return current snake as valid lower bound
            return current_snake
        
        # Check if we actually extended
        if extended_snake_node.get_length() > len(current_snake):
            current_snake = extended_snake_node.transition_sequence
            current_dim += 1
            
            if verbose:
                print(
                    f"Extended to dimension {current_dim}, "
                    f"length: {len(current_snake)}"
                )
        else:
            if verbose:
                print(f"No extension found from dimension {current_dim}, using seed")
            # Return current snake - search was attempted but no extension found
            return current_snake
    
    return current_snake


def pruned_bfs_search_from_seed(
    seed_node: SnakeNode,
    dimension: int,
    memory_limit_gb: float = 18.0,
    max_levels: int = 50000,
    min_extension: int = 1,
    verbose: bool = True
) -> Optional[SnakeNode]:
    """Modified BFS that starts from a seed snake instead of origin.
    
    When extending to a higher dimension, allows using the new dimension
    and searches for extensions. Uses backtracking strategy if seed is stuck.
    Continues searching until it finds at least min_extension additional edges
    or exhausts the search space.
    
    Parameters
    ----------
    seed_node : SnakeNode
        Starting snake node
    dimension : int
        Target dimension
    memory_limit_gb : float, optional
        Memory limit (default: 18.0)
    max_levels : int, optional
        Maximum search levels (default: 50000)
    min_extension : int, optional
        Minimum extension required (default: 1)
    verbose : bool, optional
        Print progress (default: True)
    """
    if seed_node.dimension != dimension:
        raise ValueError(
            f"Seed node dimension {seed_node.dimension} "
            f"does not match target dimension {dimension}"
        )
    
    start_time = time.time()
    seed_length = seed_node.get_length()
    target_length = seed_length + min_extension
    
    # Start with seed node, but also try shorter prefixes to allow backtracking
    initial_nodes: List[SnakeNode] = [seed_node]
    
    # Try shorter prefixes (backtracking strategy) to find extension points
    # More aggressive prefix selection for high dimensions
    if seed_length > 100:
        # Try many more prefixes, especially for high dimensions
        if dimension >= 14:
            # For high dimensions, try many more prefixes including very short ones
            prefix_ratios = [0.999, 0.99, 0.98, 0.97, 0.95, 0.93, 0.9, 0.87, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
            # Also try fixed-length prefixes at key points
            fixed_lengths = [seed_length - 1, seed_length - 10, seed_length - 50, seed_length - 100, 
                           seed_length - 500, seed_length - 1000, seed_length // 2, seed_length // 4]
        else:
            prefix_ratios = [0.98, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7]
            fixed_lengths = []
        
        # Try ratio-based prefixes
        for prefix_ratio in prefix_ratios:
            prefix_len = int(seed_length * prefix_ratio)
            if prefix_len > 0 and prefix_len < seed_length:
                prefix_seq = seed_node.transition_sequence[:prefix_len]
                try:
                    prefix_node = SnakeNode(prefix_seq, dimension)
                    # Check if this prefix can actually extend
                    from ..utils.canonical import get_legal_next_dimensions
                    legal_dims = get_legal_next_dimensions(prefix_seq)
                    new_dim = dimension - 1
                    
                    # Check if we can extend in the new dimension
                    can_extend_new_dim = prefix_node.can_extend(new_dim)
                    can_extend_any = any(prefix_node.can_extend(d) for d in legal_dims if d < dimension)
                    
                    if can_extend_new_dim or can_extend_any:
                        initial_nodes.append(prefix_node)
                        if verbose:
                            print(f"  Added prefix of length {prefix_len} (can extend: new_dim={can_extend_new_dim}, any={can_extend_any})")
                except ValueError:
                    pass
        
        # Try fixed-length prefixes
        for prefix_len in fixed_lengths:
            if prefix_len > 0 and prefix_len < seed_length and prefix_len not in [int(seed_length * r) for r in prefix_ratios]:
                prefix_seq = seed_node.transition_sequence[:prefix_len]
                try:
                    prefix_node = SnakeNode(prefix_seq, dimension)
                    from ..utils.canonical import get_legal_next_dimensions
                    legal_dims = get_legal_next_dimensions(prefix_seq)
                    new_dim = dimension - 1
                    can_extend_new_dim = prefix_node.can_extend(new_dim)
                    can_extend_any = any(prefix_node.can_extend(d) for d in legal_dims if d < dimension)
                    
                    if can_extend_new_dim or can_extend_any:
                        initial_nodes.append(prefix_node)
                        if verbose:
                            print(f"  Added fixed prefix of length {prefix_len}")
                except ValueError:
                    pass
    
    # Filter initial nodes to only those that can actually extend
    # But for high dimensions, be more lenient - include nodes that might extend after some backtracking
    viable_nodes = []
    for node in initial_nodes:
        from ..utils.canonical import get_legal_next_dimensions
        from .bfs_pruned import is_valid_extension
        legal_dims = get_legal_next_dimensions(node.transition_sequence)
        new_dim = dimension - 1
        if new_dim not in legal_dims and new_dim < dimension:
            legal_dims = list(legal_dims) + [new_dim]
        
        # Check if this node can extend in any dimension
        can_extend = any(is_valid_extension(node, d) for d in legal_dims if d < dimension)
        if can_extend:
            viable_nodes.append(node)
        elif dimension >= 14:
            # For high dimensions, include nodes with good fitness even if stuck
            # They might become unstuck after some search
            if node.fitness > 100:  # Has some unmarked vertices
                viable_nodes.append(node)
                if verbose:
                    print(f"  Including stuck node of length {node.get_length()} (fitness={node.fitness}) for high-dim search")
        elif verbose:
            print(f"  Skipping node of length {node.get_length()} - cannot extend")
    
    if not viable_nodes:
        if verbose:
            print(f"Warning: No viable starting nodes found from prefixes")
            print(f"Trying very short prefixes to find extension points...")
        
        # Last resort: try very short prefixes that should have room
        for short_len in [100, 50, 20, 10, 5]:
            if short_len < seed_length:
                try:
                    short_seq = seed_node.transition_sequence[:short_len]
                    short_node = SnakeNode(short_seq, dimension)
                    from ..utils.canonical import get_legal_next_dimensions
                    from .bfs_pruned import is_valid_extension
                    legal_dims = get_legal_next_dimensions(short_seq)
                    new_dim = dimension - 1
                    if new_dim not in legal_dims and new_dim < dimension:
                        legal_dims = list(legal_dims) + [new_dim]
                    
                    if any(is_valid_extension(short_node, d) for d in legal_dims if d < dimension):
                        viable_nodes.append(short_node)
                        if verbose:
                            print(f"  Found viable short prefix of length {short_len}")
                        break
                except (ValueError, Exception):
                    continue
        
        # If still nothing, use seed anyway and let search try
        if not viable_nodes:
            if verbose:
                print(f"Using seed node anyway - search will attempt to find extension points")
            viable_nodes = [seed_node]
    
    current_level: List[SnakeNode] = viable_nodes
    best_snake: Optional[SnakeNode] = seed_node
    max_length = seed_length
    
    level_count = 0
    total_nodes_explored = 0
    no_improvement_count = 0
    # Much more patience for high dimensions - they need extensive search
    max_no_improvement = 5000 if dimension >= 14 else 2000
    
    if verbose:
        print(
            f"Starting from seed snake of length {seed_length} "
            f"in dimension {dimension} (trying {len(viable_nodes)} viable starting points)"
        )
        print(f"Target: extend to at least length {target_length}")
    
    while current_level and level_count < max_levels:
        next_level: List[SnakeNode] = []
        
        # Generate all children for current level
        for node in current_level:
            from ..utils.canonical import get_legal_next_dimensions
            from .bfs_pruned import is_valid_extension
            
            legal_dims = get_legal_next_dimensions(node.transition_sequence)
            
            # When extending to higher dimension, allow using the new dimension
            new_dim = dimension - 1
            if new_dim not in legal_dims and new_dim < dimension:
                legal_dims = list(legal_dims) + [new_dim]
            
            for dim_val in legal_dims:
                if dim_val >= dimension:
                    continue
                if is_valid_extension(node, dim_val):
                    try:
                        child = node.create_child(dim_val)
                        next_level.append(child)
                        total_nodes_explored += 1
                        
                        child_length = child.get_length()
                        if child_length > max_length:
                            max_length = child_length
                            best_snake = child
                            no_improvement_count = 0
                            if verbose:
                                print(
                                    f"Level {level_count + 1}: "
                                    f"New best length {max_length} "
                                    f"(extension: +{max_length - seed_length})"
                                )
                            
                            # If we've reached target, we can optionally continue or return
                            if max_length >= target_length:
                                if verbose:
                                    print(f"Reached target length {target_length}, continuing search...")
                        else:
                            no_improvement_count += 1
                    except ValueError:
                        continue
        
        # If no children generated, we're stuck
        if not next_level:
            if verbose:
                print(f"No valid extensions found at level {level_count + 1}")
            
            # For high dimensions, be very aggressive about finding extension points
            if dimension >= 14:
                if verbose:
                    print(f"Trying aggressive backtracking for high dimension (level {level_count + 1})...")
                
                # Try many different prefix lengths
                if best_snake and best_snake.get_length() > 10:
                    tried_lengths = set()
                    # Try many ratios
                    for ratio in [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.05]:
                        prefix_len = max(1, int(best_snake.get_length() * ratio))
                        if prefix_len < best_snake.get_length() and prefix_len not in tried_lengths:
                            tried_lengths.add(prefix_len)
                            try:
                                prefix_seq = best_snake.transition_sequence[:prefix_len]
                                prefix_node = SnakeNode(prefix_seq, dimension)
                                from ..utils.canonical import get_legal_next_dimensions
                                from .bfs_pruned import is_valid_extension
                                legal_dims = get_legal_next_dimensions(prefix_seq)
                                new_dim = dimension - 1
                                if new_dim not in legal_dims and new_dim < dimension:
                                    legal_dims = list(legal_dims) + [new_dim]
                                
                                # Check all legal dimensions
                                for d in legal_dims:
                                    if d < dimension and is_valid_extension(prefix_node, d):
                                        next_level.append(prefix_node)
                                        if verbose:
                                            print(f"  Found viable prefix of length {prefix_len} (can extend in dim {d})")
                                        break
                                
                                if next_level:
                                    break
                            except (ValueError, Exception) as e:
                                continue
                    
                    # Also try fixed short lengths
                    if not next_level:
                        for short_len in [1000, 500, 200, 100, 50, 20, 10]:
                            if short_len < best_snake.get_length() and short_len not in tried_lengths:
                                try:
                                    prefix_seq = best_snake.transition_sequence[:short_len]
                                    prefix_node = SnakeNode(prefix_seq, dimension)
                                    from ..utils.canonical import get_legal_next_dimensions
                                    from .bfs_pruned import is_valid_extension
                                    legal_dims = get_legal_next_dimensions(prefix_seq)
                                    new_dim = dimension - 1
                                    if new_dim not in legal_dims and new_dim < dimension:
                                        legal_dims = list(legal_dims) + [new_dim]
                                    
                                    for d in legal_dims:
                                        if d < dimension and is_valid_extension(prefix_node, d):
                                            next_level.append(prefix_node)
                                            if verbose:
                                                print(f"  Found viable fixed prefix of length {short_len}")
                                            break
                                except (ValueError, Exception):
                                    continue
                                if next_level:
                                    break
                
                # Only break if we've tried everything and still nothing
                if not next_level and level_count > 100:
                    if verbose:
                        print(f"Exhausted backtracking options after {level_count} levels")
                    break
                elif not next_level:
                    # Continue searching - might find something
                    if verbose and level_count % 100 == 0:
                        print(f"Still searching for extension points (level {level_count})...")
                    continue
            else:
                # For lower dimensions, break if stuck
                break
        
        # Prune if memory limit exceeded
        from .bfs_pruned import estimate_memory_usage, prune_by_fitness
        
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
        
        # Progress reporting
        if verbose:
            report_interval = 10 if dimension >= 14 else 50
            if level_count % report_interval == 0 or max_length > seed_length:
                elapsed = time.time() - start_time
                extension = max_length - seed_length
                print(
                    f"Level {level_count}: {len(current_level)} nodes, "
                    f"best length: {max_length} (+{extension}), "
                    f"time: {elapsed:.1f}s"
                )
        
        # Stop if no improvement for too long (but only if we've made some progress)
        if no_improvement_count > max_no_improvement:
            if max_length > seed_length:
                if verbose:
                    print(f"No improvement for {max_no_improvement} levels, stopping with extension")
                break
            elif level_count > 1000:
                # For high dimensions, search longer even without improvement
                if dimension >= 14 and level_count < 5000:
                    if verbose and level_count % 500 == 0:
                        print(f"Continuing search despite no improvement (level {level_count})...")
                    no_improvement_count = 0  # Reset counter to continue
                else:
                    if verbose:
                        print(f"No improvement after {level_count} levels, stopping")
                    break
        
        # Stop if we've exhausted the search
        if not current_level:
            break
    
    total_time = time.time() - start_time
    
    # Only return if we actually extended
    if best_snake and max_length > seed_length:
        if best_snake and hasattr(best_snake, '__dict__'):
            best_snake._search_metadata = {
                'total_time': total_time,
                'level_count': level_count,
                'nodes_explored': total_nodes_explored,
                'from_seed': True,
                'extension': max_length - seed_length
            }
        
        if verbose:
            extension = max_length - seed_length
            print(
                f"Search completed: extended from {seed_length} to {max_length} "
                f"(+{extension}) after {level_count} levels, {total_time:.2f}s"
            )
        
        return best_snake
    else:
        if verbose:
            print(
                f"Search completed: no extension found after {level_count} levels, "
                f"{total_time:.2f}s"
            )
        # Return None if no extension found
        return None

