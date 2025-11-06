"""Performance profiling tools."""

from typing import Optional
import cProfile
import pstats
from ..core.snake_node import SnakeNode
from ..search.bfs_pruned import pruned_bfs_search


def profile_memory_usage(
    dimension: int,
    memory_limit_gb: float = 1.0
) -> Optional[SnakeNode]:
    """Profile memory usage during search.
    
    Uses memory_profiler to track memory consumption.
    Requires @profile decorator or running with python -m memory_profiler.
    
    Parameters
    ----------
    dimension : int
        Dimension to search
    memory_limit_gb : float, optional
        Memory limit in GB (default: 1.0 for profiling)
    
    Returns
    -------
    Optional[SnakeNode]
        Search result
    
    Examples
    --------
    Run with: python -m memory_profiler script.py
    Or use: profile_memory_usage(7)
    """
    return pruned_bfs_search(
        dimension=dimension,
        memory_limit_gb=memory_limit_gb,
        verbose=False
    )


def profile_performance(
    dimension: int,
    output_file: Optional[str] = None,
    sort_by: str = 'cumulative',
    num_stats: int = 20
) -> Optional[SnakeNode]:
    """Profile CPU performance using cProfile.
    
    Parameters
    ----------
    dimension : int
        Dimension to search
    output_file : Optional[str], optional
        File to save profile stats (default: None, print to stdout)
    sort_by : str, optional
        Sort stats by this key (default: 'cumulative')
    num_stats : int, optional
        Number of top functions to show (default: 20)
    
    Returns
    -------
    Optional[SnakeNode]
        Search result
    
    Examples
    --------
    >>> result = profile_performance(7, 'profile_stats.txt')
    """
    profiler = cProfile.Profile()
    profiler.enable()
    
    result = pruned_bfs_search(
        dimension=dimension,
        memory_limit_gb=18.0,
        verbose=False
    )
    
    profiler.disable()
    
    stats = pstats.Stats(profiler)
    stats.sort_stats(sort_by)
    
    if output_file:
        with open(output_file, 'w') as f:
            stats.print_stats(num_stats, file=f)
    else:
        stats.print_stats(num_stats)
    
    return result


def benchmark_known_snakes() -> None:
    """Benchmark search against known records.
    
    Runs search for dimensions with known records and compares
    results to expected lengths.
    """
    from .known_snakes import KNOWN_RECORDS, get_known_record
    
    print("Benchmarking against known records:")
    print("-" * 50)
    
    for dim in sorted(KNOWN_RECORDS.keys()):
        if dim > 7:  # Skip high dimensions for quick benchmark
            continue
        
        expected = get_known_record(dim)
        print(f"Dimension {dim}: Expected length {expected}")
        
        result = pruned_bfs_search(
            dimension=dim,
            memory_limit_gb=2.0,
            verbose=False
        )
        
        if result:
            actual = result.get_length()
            match = "✓" if actual >= expected else "✗"
            print(f"  {match} Found length {actual}")
        else:
            print(f"  ✗ Search failed")
        
        print()


def compare_fitness_functions(dimension: int = 5) -> None:
    """Compare different fitness functions.
    
    Parameters
    ----------
    dimension : int, optional
        Dimension to test (default: 5)
    """
    from ..search.fitness import SimpleFitnessEvaluator, AdvancedFitnessEvaluator
    from ..core.snake_node import SnakeNode
    
    print(f"Comparing fitness functions for dimension {dimension}:")
    print("-" * 50)
    
    # Create a test node
    test_node = SnakeNode([0, 1, 2, 0], dimension)
    
    # Simple fitness
    simple_eval = SimpleFitnessEvaluator(test_node)
    simple_fitness = simple_eval.evaluate()
    print(f"Simple (unmarked count): {simple_fitness}")
    
    # Advanced fitness
    advanced_eval = AdvancedFitnessEvaluator(test_node)
    unmarked = advanced_eval.count_unmarked_vertices()
    dead_ends = advanced_eval.count_dead_ends()
    unreachable = advanced_eval.count_unreachable_vertices()
    
    print(f"Advanced:")
    print(f"  Unmarked vertices: {unmarked}")
    print(f"  Dead ends: {dead_ends}")
    print(f"  Unreachable: {unreachable}")
    print(f"  Combined: {advanced_eval.combined_fitness()}")

