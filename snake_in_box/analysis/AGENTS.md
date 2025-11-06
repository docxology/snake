# Analysis Module: Agent Documentation

## Purpose

The `analysis` module provides comprehensive analysis tools for snake-in-the-box problems across dimensions 1-16. It includes dimension analysis, report generation, validation reporting, performance reporting, and feasibility analysis for high dimensions.

## Key Functions

### analyze_single_dimension

**Purpose**: Analyze a single dimension, using known snakes when available or running search.

**Parameters**:
- `dimension`: int - Dimension to analyze
- `use_known`: bool - Use known snake if available (default: True)
- `memory_limit_gb`: float - Memory limit for search (default: 2.0)
- `verbose`: bool - Print progress (default: False)

**Returns**: `Dict` containing:
- `dimension`: int
- `snake_node`: SnakeNode or None
- `transition_sequence`: List[int] or None
- `length`: int
- `is_valid`: bool
- `validation_message`: str
- `known_record`: int or None
- `matches_known`: bool
- `search_time`: float
- `method`: str ('known' or 'search')

**Usage**:
```python
from snake_in_box.analysis import analyze_single_dimension
result = analyze_single_dimension(dimension=7, use_known=True)
print(f"Length: {result['length']}, Valid: {result['is_valid']}")
```

### analyze_dimensions

**Purpose**: Analyze multiple dimensions in batch.

**Parameters**:
- `dimensions`: List[int] - List of dimensions to analyze
- `use_known`: bool - Use known snakes if available (default: True)
- `memory_limit_gb`: float - Memory limit for search (default: 2.0)
- `verbose`: bool - Print progress (default: False)

**Returns**: `Dict[int, Dict]` - Dictionary mapping dimension to analysis result

**Usage**:
```python
from snake_in_box.analysis import analyze_dimensions
results = analyze_dimensions([1, 2, 3, 4, 5], use_known=True)
for dim, result in results.items():
    print(f"Dim {dim}: {result['length']}")
```

### generate_analysis_report

**Purpose**: Generate comprehensive analysis report in Markdown or HTML format.

**Parameters**:
- `results`: Dict[int, Dict] - Analysis results from analyze_dimensions
- `output_file`: str - Output file path (default: "analysis_report.md")
- `format`: str - Report format: 'markdown' or 'html' (default: 'markdown')

**Returns**: `str` - Report content

**Usage**:
```python
from snake_in_box.analysis import analyze_dimensions, generate_analysis_report
results = analyze_dimensions(range(1, 14))
generate_analysis_report(results, "output/reports/analysis_report.md", format="markdown")
```

### generate_validation_report

**Purpose**: Generate validation report focusing on snake validity.

**Parameters**:
- `results`: Dict[int, Dict] - Analysis results
- `output_file`: str - Output file path (default: "validation_report.md")

**Returns**: `str` - Report content

**Usage**:
```python
from snake_in_box.analysis import analyze_dimensions, generate_validation_report
results = analyze_dimensions(range(1, 14))
generate_validation_report(results, "output/reports/validation_report.md")
```

### generate_performance_report

**Purpose**: Generate performance report focusing on computation time and efficiency.

**Parameters**:
- `results`: Dict[int, Dict] - Analysis results
- `output_file`: str - Output file path (default: "performance_report.md")

**Returns**: `str` - Report content

**Usage**:
```python
from snake_in_box.analysis import analyze_dimensions, generate_performance_report
results = analyze_dimensions(range(1, 14))
generate_performance_report(results, "output/reports/performance_report.md")
```

### generate_statistics

**Purpose**: Generate statistics from analysis results.

**Parameters**:
- `results`: Dict[int, Dict] - Analysis results

**Returns**: `Dict` containing:
- `total_dimensions`: int
- `valid_snakes`: int
- `invalid_snakes`: int
- `from_known`: int
- `from_search`: int
- `matches_known`: int
- `total_time`: float
- `average_time`: float
- `total_length`: int
- `average_length`: float
- `max_length`: int
- `min_length`: int

## Feasibility Analysis

### analyze_dimension_complexity

**Purpose**: Analyze computational complexity for a dimension.

**Parameters**:
- `dimension`: int - Dimension to analyze

**Returns**: `Dict` containing:
- `num_vertices`: Total vertices in hypercube
- `num_edges`: Total edges
- `bitmap_memory_gb`: Memory for bitmap (GB)
- `estimated_nodes`: Estimated search tree nodes
- `estimated_memory_gb`: Estimated memory for search (GB)
- `estimated_time_hours`: Estimated search time (hours)
- `feasible`: bool - Whether dimension is computationally feasible

**Usage**:
```python
from snake_in_box.analysis.dimension_feasibility import analyze_dimension_complexity
analysis = analyze_dimension_complexity(16)
print(f"Memory: {analysis['estimated_memory_gb']:.2f} GB")
print(f"Time: {analysis['estimated_time_hours']:.2f} hours")
```

### estimate_requirements_for_dimension_16

**Purpose**: Estimate requirements and strategies to reach dimension 16.

**Returns**: `Dict` with requirements and feasibility assessment

## Dependencies

- `core/`: SnakeNode, validation functions
- `search/`: pruned_bfs_search
- `benchmarks/`: Known snakes and records
- `typing`: Type hints
- `datetime`: Report timestamps

## Report Formats

### Markdown Reports
- Comprehensive analysis with tables
- Executive summary
- Detailed results by dimension
- Statistics and methodology

### HTML Reports
- Styled tables
- Interactive format
- Suitable for web viewing

## Analysis Workflow

1. **Single Dimension**:
   - Check for known snake
   - If not available, run search
   - Validate result
   - Compare with known record

2. **Multiple Dimensions**:
   - Iterate through dimension list
   - Apply single dimension analysis
   - Aggregate statistics
   - Generate reports

3. **Report Generation**:
   - Generate statistics
   - Format results
   - Write to file
   - Return content

## Performance Characteristics

- **Time**: O(n × search_time) for n dimensions
- **Memory**: Uses search memory limits per dimension
- **Efficiency**: Reuses known snakes when available

## Testing

See `tests/test_analysis.py`:
- Analysis function tests
- Report generation tests
- Statistics calculation tests

## Usage Patterns

### Complete Analysis Workflow
```python
from snake_in_box.analysis import (
    analyze_dimensions,
    generate_analysis_report,
    generate_validation_report,
    generate_performance_report
)

# Analyze dimensions 1-13
results = analyze_dimensions(range(1, 14), use_known=True, verbose=True)

# Generate all reports
generate_analysis_report(results, "output/reports/analysis_report.md")
generate_validation_report(results, "output/reports/validation_report.md")
generate_performance_report(results, "output/reports/performance_report.md")
```

### Feasibility Assessment
```python
from snake_in_box.analysis.dimension_feasibility import (
    analyze_dimension_complexity,
    estimate_requirements_for_dimension_16
)

# Analyze dimension 16
complexity = analyze_dimension_complexity(16)
print(f"Feasible: {complexity['feasible']}")

# Estimate requirements
requirements = estimate_requirements_for_dimension_16()
print(f"Recommended: {requirements['recommended_approach']}")
```

## Integration with Other Modules

- **Core**: Uses SnakeNode and validation
- **Search**: Calls pruned_bfs_search when needed
- **Benchmarks**: Retrieves known snakes and records
- **Utils**: May use visualization for reports

## Notes

- Analysis supports dimensions 1-16
- Known snakes are preferred when available (faster)
- Search is fallback for unknown dimensions
- Reports can be generated in multiple formats
- Feasibility analysis helps plan high-dimension searches

