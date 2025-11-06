# Package Architecture Diagram

This document contains Mermaid diagrams showing the package structure and module dependencies.

## Package Structure

```mermaid
graph TB
    subgraph "snake_in_box Package"
        Core[core/]
        Search[search/]
        Utils[utils/]
        Benchmarks[benchmarks/]
        Analysis[analysis/]
    end
    
    Core --> |"uses"| Search
    Core --> |"uses"| Utils
    Search --> |"uses"| Core
    Search --> |"uses"| Utils
    Utils --> |"uses"| Core
    Benchmarks --> |"uses"| Core
    Benchmarks --> |"uses"| Search
    Analysis --> |"uses"| Core
    Analysis --> |"uses"| Search
    Analysis --> |"uses"| Benchmarks
```

## Module Dependencies

```mermaid
graph LR
    subgraph "Core Module"
        Hypercube[HypercubeBitmap]
        SnakeNode[SnakeNode]
        Transitions[transitions.py]
        Validation[validation.py]
    end
    
    subgraph "Search Module"
        BFS[bfs_pruned.py]
        Fitness[fitness.py]
        Priming[priming.py]
        Parallel[parallel.py]
    end
    
    subgraph "Utils Module"
        Canonical[canonical.py]
        Export[export.py]
        Visualize[visualize.py]
    end
    
    subgraph "Benchmarks Module"
        Known[known_snakes.py]
        Perf[performance.py]
    end
    
    subgraph "Analysis Module"
        Analyze[analyze_dimensions.py]
        Reporting[reporting.py]
    end
    
    BFS --> SnakeNode
    BFS --> Canonical
    BFS --> Fitness
    Priming --> BFS
    Priming --> SnakeNode
    Fitness --> SnakeNode
    Canonical --> Transitions
    Export --> SnakeNode
    Visualize --> SnakeNode
    Known --> Transitions
    Analyze --> SnakeNode
    Analyze --> BFS
    Analyze --> Known
    Reporting --> Analyze
```

## Data Flow

```mermaid
flowchart TD
    Start([User calls pruned_bfs_search]) --> Init[Initialize empty SnakeNode]
    Init --> Level[Current level = [empty snake]]
    Level --> Generate[Generate children for each node]
    Generate --> Check{Memory limit<br/>exceeded?}
    Check -->|Yes| Prune[Prune by fitness]
    Check -->|No| Next[Move to next level]
    Prune --> Next
    Next --> Best{Better snake<br/>found?}
    Best -->|Yes| Update[Update best snake]
    Best -->|No| Continue[Continue]
    Update --> Continue
    Continue --> More{More nodes<br/>to expand?}
    More -->|Yes| Level
    More -->|No| Return[Return best snake]
```

## Class Relationships

```mermaid
classDiagram
    class HypercubeBitmap {
        +int dimension
        +int num_vertices
        +array bitmap
        +set_bit(vertex)
        +get_bit(vertex)
        +count_unmarked()
    }
    
    class SnakeNode {
        +List[int] transition_sequence
        +int dimension
        +HypercubeBitmap vertices_bitmap
        +int fitness
        +can_extend(dim)
        +create_child(dim)
        +get_length()
    }
    
    class SimpleFitnessEvaluator {
        +SnakeNode node
        +evaluate()
    }
    
    class AdvancedFitnessEvaluator {
        +SnakeNode node
        +count_unmarked_vertices()
        +count_dead_ends()
        +count_unreachable_vertices()
        +combined_fitness(weights)
    }
    
    SnakeNode --> HypercubeBitmap : contains
    SimpleFitnessEvaluator --> SnakeNode : evaluates
    AdvancedFitnessEvaluator --> SnakeNode : evaluates
```

## Related Documentation

- [Package Structure](../architecture/package-structure.md) - Detailed package organization
- [Module Dependencies](../architecture/module-dependencies.md) - Module relationships
- [Data Structures](../architecture/data-structures.md) - Core data structures

