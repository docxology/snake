# Data Flow Diagrams

This document contains Mermaid diagrams showing data flow through the system.

## SnakeNode Creation Flow

```mermaid
flowchart TD
    Start([Create SnakeNode]) --> Input[Input:<br/>transition_sequence<br/>dimension]
    Input --> Init[Initialize HypercubeBitmap]
    Init --> Origin[Start at origin<br/>vertex 0]
    Origin --> Mark1[Mark vertex 0<br/>as occupied]
    Mark1 --> Adj1[Mark adjacent vertices<br/>as prohibited]
    Adj1 --> Loop{For each<br/>transition}
    Loop -->|Next| Flip[Flip bit at<br/>transition position]
    Flip --> Mark2[Mark new vertex<br/>as occupied]
    Mark2 --> Adj2[Mark adjacent vertices<br/>as prohibited]
    Adj2 --> Loop
    Loop -->|Done| Fitness[Calculate fitness<br/>count unmarked]
    Fitness --> Return([Return SnakeNode])
```

## Bitmap Operations Flow

```mermaid
flowchart TD
    Start([Bitmap operation]) --> Op{Operation<br/>type?}
    Op -->|set_bit| Set[Set bit at vertex]
    Op -->|get_bit| Get[Get bit at vertex]
    Op -->|count_unmarked| Count[Count unmarked vertices]
    
    Set --> Calc1[Calculate word index<br/>vertex >> 6]
    Calc1 --> Calc2[Calculate bit index<br/>vertex & 63]
    Calc2 --> Update[Update bitmap[word_idx]<br/>|= 1 << bit_idx]
    Update --> End1([Done])
    
    Get --> Calc3[Calculate word index]
    Calc3 --> Calc4[Calculate bit index]
    Calc4 --> Check[Check bitmap[word_idx]<br/>& 1 << bit_idx]
    Check --> End2([Return bool])
    
    Count --> Iterate[Iterate all vertices]
    Iterate --> Check2{Vertex<br/>marked?}
    Check2 -->|No| Increment[Increment count]
    Check2 -->|Yes| Next[Next vertex]
    Increment --> Next
    Next --> More{More<br/>vertices?}
    More -->|Yes| Iterate
    More -->|No| End3([Return count])
```

## Search Data Flow

```mermaid
flowchart LR
    User([User]) --> API[pruned_bfs_search]
    API --> Init[Initialize SnakeNode]
    Init --> Level[Current level]
    Level --> Generate[Generate children]
    Generate --> Validate[Validate extensions]
    Validate --> Create[Create child nodes]
    Create --> Fitness[Calculate fitness]
    Fitness --> Memory{Memory<br/>check}
    Memory -->|Exceeded| Prune[Prune by fitness]
    Memory -->|OK| Next[Next level]
    Prune --> Next
    Next --> Best[Track best snake]
    Best --> Loop{More<br/>levels?}
    Loop -->|Yes| Level
    Loop -->|No| Return[Return best snake]
    Return --> User
```

## Priming Data Flow

```mermaid
flowchart TD
    Start([prime_search]) --> Input[Input:<br/>lower_dim_snake<br/>target_dimension]
    Input --> Detect[Detect current dimension]
    Detect --> Check{Current <br/>target?}
    Check -->|No| Return([Return snake])
    Check -->|Yes| Create[Create SnakeNode<br/>in higher dimension]
    Create --> Seed[Seed node created]
    Seed --> BFS[Run pruned_bfs_search_from_seed]
    BFS --> Extend[Extend snake]
    Extend --> Success{Success?}
    Success -->|No| Fail([Return None])
    Success -->|Yes| Update[Update snake<br/>and dimension]
    Update --> Check
```

## Validation Flow

```mermaid
flowchart TD
    Start([Validate snake]) --> Input[Input:<br/>vertex_sequence]
    Input --> Convert[Convert to vertices<br/>if needed]
    Convert --> Loop1{For each<br/>consecutive pair}
    Loop1 --> Check1[Check Hamming<br/>distance = 1]
    Check1 --> Valid1{Valid?}
    Valid1 -->|No| Error1([Error:<br/>Consecutive invalid])
    Valid1 -->|Yes| Loop1
    Loop1 -->|Done| Loop2{For each<br/>non-consecutive pair}
    Loop2 --> Check2[Check Hamming<br/>distance > 1]
    Check2 --> Valid2{Valid?}
    Valid2 -->|No| Error2([Error:<br/>Non-consecutive invalid])
    Valid2 -->|Yes| Loop2
    Loop2 -->|Done| Success([Valid snake])
```

## Export Flow

```mermaid
flowchart TD
    Start([export_snake]) --> Input[Input:<br/>SnakeNode<br/>filename]
    Input --> Extract[Extract data:<br/>- transition_sequence<br/>- vertex_sequence<br/>- dimension<br/>- length]
    Extract --> JSON[Generate JSON]
    Extract --> Text[Generate hex text]
    Extract --> CSV[Generate CSV]
    JSON --> Write1[Write JSON file]
    Text --> Write2[Write text file]
    CSV --> Write3[Write CSV file]
    Write1 --> Done([Done])
    Write2 --> Done
    Write3 --> Done
```

## Related Documentation

- [Data Structures](../architecture/data-structures.md) - Core data structures
- [Algorithm Flow](../diagrams/algorithm-flow.md) - Algorithm flowcharts
- [Package Architecture](../diagrams/package-architecture.md) - Package structure

