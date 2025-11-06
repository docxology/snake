# Package Structure

This document describes the organization and structure of the Snake-in-the-Box package.

## Directory Structure

```
snake_in_box/
├── __init__.py              # Package initialization and exports
├── AGENTS.md                # Package-level documentation
├── core/                    # Core data structures
│   ├── __init__.py
│   ├── AGENTS.md
│   ├── hypercube.py         # HypercubeBitmap class
│   ├── snake_node.py        # SnakeNode class
│   ├── transitions.py       # Conversion utilities
│   └── validation.py        # Validation functions
├── search/                  # Search algorithms
│   ├── __init__.py
│   ├── AGENTS.md
│   ├── bfs_pruned.py       # Pruned BFS algorithm
│   ├── fitness.py          # Fitness evaluators
│   ├── priming.py          # Priming strategy
│   └── parallel.py         # Parallel search
├── utils/                   # Utilities
│   ├── __init__.py
│   ├── AGENTS.md
│   ├── canonical.py        # Canonical form
│   ├── export.py           # Export functions
│   ├── visualize.py       # Basic visualization
│   ├── visualize_advanced.py  # Advanced visualization
│   ├── visualization_helpers.py  # Visualization helpers
│   ├── graphical_abstract.py  # Panel generator
│   └── performance_plots.py  # Performance plotting
├── benchmarks/             # Benchmarks
│   ├── __init__.py
│   ├── AGENTS.md
│   ├── known_snakes.py     # Known records
│   └── performance.py     # Profiling tools
└── analysis/               # Analysis
    ├── __init__.py
    ├── AGENTS.md
    ├── analyze_dimensions.py  # Dimension analysis
    ├── reporting.py        # Report generation
    └── dimension_feasibility.py  # Feasibility analysis
```

## Module Responsibilities

### Core Module

**Purpose**: Fundamental data structures and utilities

**Components**:
- `HypercubeBitmap`: Bitmap representation of hypercube
- `SnakeNode`: Search tree node
- Transition/vertex conversions
- Validation functions

**Dependencies**: None (base module)

### Search Module

**Purpose**: Search algorithms and strategies

**Components**:
- Pruned BFS algorithm
- Fitness evaluators
- Priming strategy
- Parallel processing

**Dependencies**: `core/`, `utils/`

### Utils Module

**Purpose**: Utility functions

**Components**:
- Canonical form utilities
- Export functions
- Visualization tools

**Dependencies**: `core/`

### Benchmarks Module

**Purpose**: Known records and performance profiling

**Components**:
- Known snake database
- Performance profiling tools

**Dependencies**: `core/`, `search/`

### Analysis Module

**Purpose**: Analysis and reporting

**Components**:
- Dimension analysis
- Report generation
- Feasibility analysis

**Dependencies**: `core/`, `search/`, `benchmarks/`, `utils/`

## Package Exports

The main package (`__init__.py`) exports:

- **Core**: `HypercubeBitmap`, `SnakeNode`, conversion and validation functions, `calculate_snake_for_dimension`
- **Search**: `pruned_bfs_search`, `prime_search`, `parallel_search`
- **Utils**: `is_canonical`, `get_legal_next_dimensions`, `export_snake`, `visualize_snake_3d`, `visualize_snake_auto`, `generate_16d_panel`
- **Benchmarks**: `get_known_record`, `get_known_snake`, `KNOWN_RECORDS`
- **Analysis**: `analyze_dimensions`, `analyze_single_dimension`, report generation functions (`generate_analysis_report`, `generate_validation_report`, `generate_performance_report`, `generate_exponential_analysis_report`)

Note: Additional visualization functions (`visualize_snake_heatmap`, `visualize_snake_3d_projection`, `visualize_snake_transition_matrix`) and `export_analysis_data` are available from `snake_in_box.utils` module.

## Design Principles

1. **Modularity**: Each module is self-contained with clear interfaces
2. **Separation of Concerns**: Each module has a single responsibility
3. **Dependency Management**: Dependencies flow downward (core → search → analysis)
4. **Extensibility**: Easy to add new search strategies or fitness functions

## Related Documentation

- [Module Dependencies](module-dependencies.md) - Dependency graph
- [Data Structures](data-structures.md) - Core data structures
- [Memory Management](memory-management.md) - Memory optimization

