"""Parallel search example.

Demonstrates using parallel processing to speed up search.
"""

from snake_in_box import parallel_search, export_snake


def main():
    """Run parallel search example."""
    print("Running parallel search for dimension 7...")
    print("Using 4 workers (adjust based on your CPU)")
    
    result = parallel_search(
        dimension=7,
        memory_limit_gb=2.0,
        num_workers=4,
        verbose=True
    )
    
    if result:
        print(f"\nFound snake of length {result.get_length()}")
        print(f"Fitness: {result.fitness}")
        
        # Export results
        export_snake(result, "snake_7d_parallel")
        print("\nResults exported to snake_7d_parallel.json")
    else:
        print("Search failed")


if __name__ == "__main__":
    main()

