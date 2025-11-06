# Module Dependencies

This document describes the dependency relationships between modules.

## Dependency Graph

```
core/ (no dependencies)
  ↓
search/ → core/, utils/
  ↓
utils/ → core/
  ↓
benchmarks/ → core/, search/
  ↓
analysis/ → core/, search/, benchmarks/, utils/
```

## Detailed Dependencies

### Core Module

**Dependencies**: None (base module)

**Exports**:
- `HypercubeBitmap`
- `SnakeNode`
- Conversion functions
- Validation functions

### Search Module

**Dependencies**:
- `core/`: Uses `SnakeNode`, `HypercubeBitmap`
- `utils/`: Uses canonical form functions

**Exports**:
- `pruned_bfs_search`
- `prime_search`
- `parallel_search`
- Fitness evaluators

### Utils Module

**Dependencies**:
- `core/`: Uses `SnakeNode` for visualization and export

**Exports**:
- Canonical form functions
- Export functions
- Visualization functions

### Benchmarks Module

**Dependencies**:
- `core/`: Uses validation and transitions
- `search/`: Uses search algorithms for benchmarking

**Exports**:
- Known records
- Performance profiling

### Analysis Module

**Dependencies**:
- `core/`: Uses `SnakeNode`, validation
- `search/`: Uses `pruned_bfs_search`
- `benchmarks/`: Uses known records
- `utils/`: Uses visualization for reports

**Exports**:
- Analysis functions
- Report generation

## Import Patterns

### Direct Imports

```python
# Core module
from snake_in_box.core import SnakeNode

# Search module
from snake_in_box.search import pruned_bfs_search

# Utils module
from snake_in_box.utils import export_snake
```

### Package-Level Imports

Most common functions are exported from main package:

```python
from snake_in_box import (
    SnakeNode,
    pruned_bfs_search,
    export_snake,
    get_known_snake
)
```

## Circular Dependencies

The package is designed to avoid circular dependencies:
- Dependencies flow downward (core → search → analysis)
- No upward dependencies
- Utils can depend on core but not search

## Extension Points

To extend the package:

1. **New fitness function**: Add to `search/fitness.py`
2. **New search strategy**: Add to `search/`
3. **New visualization**: Add to `utils/`
4. **New analysis**: Add to `analysis/`

## Related Documentation

- [Package Structure](package-structure.md) - Package organization
- [Package Architecture Diagram](../diagrams/package-architecture.md) - Visual diagram

