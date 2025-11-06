# Algorithm Flow Diagram

This document contains Mermaid diagrams showing the algorithm flow for the pruned BFS search.

## Main Algorithm Flow

```mermaid
flowchart TD
    Start([Start: pruned_bfs_search]) --> Init[Initialize:<br/>- current_level = [empty snake]<br/>- best_snake = None<br/>- max_length = 0]
    Init --> Loop{Current level<br/>not empty?}
    Loop -->|No| End([Return best_snake])
    Loop -->|Yes| Generate[For each node:<br/>- Get legal dimensions<br/>- Generate valid children<br/>- Track best snake]
    Generate --> Estimate[Estimate memory usage<br/>for next level]
    Estimate --> Check{Memory limit<br/>exceeded?}
    Check -->|Yes| Prune[Prune by fitness:<br/>- Sort by fitness<br/>- Keep top nodes]
    Check -->|No| Free[Free previous level]
    Prune --> Free
    Free --> Update[Update:<br/>- current_level = next_level<br/>- level_count++]
    Update --> Loop
```

## Node Extension Flow

```mermaid
flowchart TD
    Start([Node extension]) --> Legal[Get legal next dimensions<br/>using canonical form]
    Legal --> ForEach{For each<br/>legal dimension}
    ForEach -->|Next| Check[Check if extension<br/>is valid]
    Check --> Valid{Valid<br/>extension?}
    Valid -->|No| ForEach
    Valid -->|Yes| Create[Create child node]
    Create --> Add[Add to next level]
    Add --> Length{Length ><br/>max_length?}
    Length -->|Yes| Best[Update best snake]
    Length -->|No| ForEach
    Best --> ForEach
    ForEach -->|Done| End([Return children])
```

## Pruning Flow

```mermaid
flowchart TD
    Start([Pruning needed]) --> Estimate[Estimate memory per node]
    Estimate --> Calculate[Calculate max nodes<br/>that fit in memory]
    Calculate --> Sort[Sort nodes by fitness<br/>descending]
    Sort --> Select[Select top N nodes<br/>where N = max_nodes]
    Select --> Discard[Discard remaining nodes]
    Discard --> Return([Return pruned list])
```

## Priming Strategy Flow

```mermaid
flowchart TD
    Start([prime_search]) --> Get[Get lower dimension snake]
    Get --> Check{Current dim <br/>< target dim?}
    Check -->|No| Return([Return current snake])
    Check -->|Yes| Create[Create SnakeNode<br/>in higher dimension]
    Create --> Search[Run pruned_bfs_search_from_seed]
    Search --> Success{Search<br/>successful?}
    Success -->|No| Fail([Return None])
    Success -->|Yes| Update[Update current snake<br/>and dimension]
    Update --> Check
```

## Memory Management Flow

```mermaid
flowchart TD
    Start([Level expansion]) --> Current[Current level in memory]
    Current --> Generate[Generate next level]
    Generate --> Estimate[Estimate memory usage]
    Estimate --> Check{Exceeds<br/>limit?}
    Check -->|Yes| Prune[Prune nodes]
    Check -->|No| Free[Free current level]
    Prune --> Free
    Free --> Next[Next level becomes current]
    Next --> Only[Only two levels<br/>in memory at once]
```

## Related Documentation

- [Pruned BFS Algorithm](../algorithm/pruned-bfs.md) - Detailed algorithm description
- [Algorithm Overview](../algorithm/overview.md) - Algorithm overview
- [Memory Management](../architecture/memory-management.md) - Memory optimization

