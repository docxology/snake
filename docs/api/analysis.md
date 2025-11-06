# Analysis Module API

The `analysis` module provides comprehensive analysis tools for snake-in-the-box problems across dimensions 1-16.

## Functions

### `analyze_single_dimension(dimension: int, use_known: bool = True, memory_limit_gb: float = 2.0, verbose: bool = False) -> Dict`

Analyze a single dimension, using known snakes when available or running search.

**Parameters:**
- `dimension` (int): Dimension to analyze
- `use_known` (bool, optional): Use known snake if available (default: True)
- `memory_limit_gb` (float, optional): Memory limit for search (default: 2.0)
- `verbose` (bool, optional): Print progress (default: False)

**Returns:**
- `Dict`: Analysis result containing:
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

**Example:**
```python
from snake_in_box.analysis import analyze_single_dimension
result = analyze_single_dimension(dimension=7, use_known=True)
print(f"Length: {result['length']}, Valid: {result['is_valid']}")
```

### `analyze_dimensions(dimensions: List[int], use_known: bool = True, memory_limit_gb: float = 2.0, verbose: bool = False) -> Dict[int, Dict]`

Analyze multiple dimensions in batch.

**Parameters:**
- `dimensions` (List[int]): List of dimensions to analyze
- `use_known` (bool, optional): Use known snakes if available (default: True)
- `memory_limit_gb` (float, optional): Memory limit for search (default: 2.0)
- `verbose` (bool, optional): Print progress (default: False)

**Returns:**
- `Dict[int, Dict]`: Dictionary mapping dimension to analysis result

**Example:**
```python
from snake_in_box.analysis import analyze_dimensions
results = analyze_dimensions([1, 2, 3, 4, 5], use_known=True)
for dim, result in results.items():
    print(f"Dim {dim}: {result['length']}")
```

### `generate_analysis_report(results: Dict[int, Dict], output_file: str = "analysis_report.md", format: str = "markdown") -> str`

Generate comprehensive analysis report in Markdown or HTML format.

**Parameters:**
- `results` (Dict[int, Dict]): Analysis results from analyze_dimensions
- `output_file` (str, optional): Output file path (default: "analysis_report.md")
- `format` (str, optional): Report format: 'markdown' or 'html' (default: 'markdown')

**Returns:**
- `str`: Report content

**Example:**
```python
from snake_in_box.analysis import analyze_dimensions, generate_analysis_report
results = analyze_dimensions(range(1, 14))
generate_analysis_report(results, "output/reports/analysis_report.md", format="markdown")
```

### `generate_validation_report(results: Dict[int, Dict], output_file: str = "validation_report.md") -> str`

Generate validation report focusing on snake validity.

**Parameters:**
- `results` (Dict[int, Dict]): Analysis results
- `output_file` (str, optional): Output file path (default: "validation_report.md")

**Returns:**
- `str`: Report content

### `generate_performance_report(results: Dict[int, Dict], output_file: str = "performance_report.md") -> str`

Generate performance report focusing on computation time and efficiency.

**Parameters:**
- `results` (Dict[int, Dict]): Analysis results
- `output_file` (str, optional): Output file path (default: "performance_report.md")

**Returns:**
- `str`: Report content

### `generate_exponential_analysis_report(...)`

Generate exponential analysis report.

## Exponential Analysis Functions

### `analyze_computation_complexity(...)`

Analyze computation complexity.

### `identify_slowdown_points(...)`

Identify slowdown points in computation.

### `fit_exponential_model(...)`

Fit exponential model to computation times.

### `estimate_time_for_dimension(...)`

Estimate computation time for a dimension.

### `generate_exponential_report(...)`

Generate exponential analysis report.

## Related Documentation

- [Analysis Module AGENTS](../../snake_in_box/analysis/AGENTS.md) - Module documentation
- [Usage Guides](../guides/basic-usage.md) - Usage examples
- [Performance Tuning](../guides/performance-tuning.md) - Performance optimization

