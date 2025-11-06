"""Primed search example.

Demonstrates using priming strategy to extend known snakes to higher dimensions.
"""

from snake_in_box import prime_search, get_known_snake, export_snake


def main():
    """Run primed search example."""
    print("Extending 9D snake to 10D using priming strategy...")
    
    # Get known 9D snake
    snake_9d = get_known_snake(9)
    if not snake_9d:
        print("Failed to load 9D snake")
        return
    
    print(f"Starting with 9D snake of length {len(snake_9d)}")
    
    # Extend to 10D
    snake_10d = prime_search(
        snake_9d,
        target_dimension=10,
        memory_limit_gb=2.0,
        verbose=True
    )
    
    if snake_10d:
        print(f"\nExtended to 10D snake of length {len(snake_10d)}")
        
        # Create node for export
        from snake_in_box import SnakeNode
        node = SnakeNode(snake_10d, 10)
        export_snake(node, "snake_10d_primed")
        print("\nResults exported to snake_10d_primed.json")
    else:
        print("Priming failed")


if __name__ == "__main__":
    main()

