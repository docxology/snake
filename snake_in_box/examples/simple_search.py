"""Simple search example.

Demonstrates basic usage of the pruned BFS search algorithm.
"""

from snake_in_box import pruned_bfs_search, export_snake


def main():
    """Run simple search example."""
    print("Running pruned BFS search for dimension 7...")
    
    result = pruned_bfs_search(
        dimension=7,
        memory_limit_gb=2.0,
        verbose=True
    )
    
    if result:
        print(f"\nFound snake of length {result.get_length()}")
        print(f"Fitness: {result.fitness}")
        
        # Export results
        export_snake(result, "snake_7d")
        print("\nResults exported to snake_7d.json and snake_7d.txt")
    else:
        print("Search failed")


if __name__ == "__main__":
    main()

