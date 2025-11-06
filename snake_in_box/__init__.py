"""Snake-in-the-Box: N-dimensional snake-in-the-box algorithm.

Implements heuristically-pruned breadth-first search from Ace (2025).
"""

__version__ = "0.1.0"

from .core import (
    HypercubeBitmap,
    SnakeNode,
    vertex_to_transition,
    transition_to_vertex,
    compute_current_vertex,
    parse_hex_transition_string,
    validate_snake,
    validate_transition_sequence,
    hamming_distance,
    calculate_snake_for_dimension,
)
from .search import (
    pruned_bfs_search,
    prime_search,
    parallel_search,
)
from .utils import (
    is_canonical,
    get_legal_next_dimensions,
    export_snake,
    visualize_snake_3d,
    visualize_snake_auto,
    generate_16d_panel,
)
from .benchmarks import (
    get_known_record,
    get_known_snake,
    KNOWN_RECORDS,
)
from .analysis import (
    analyze_dimensions,
    analyze_single_dimension,
    generate_analysis_report,
    generate_validation_report,
    generate_performance_report,
    generate_exponential_analysis_report,
)

__all__ = [
    "HypercubeBitmap",
    "SnakeNode",
    "vertex_to_transition",
    "transition_to_vertex",
    "compute_current_vertex",
    "parse_hex_transition_string",
    "validate_snake",
    "validate_transition_sequence",
    "hamming_distance",
    "pruned_bfs_search",
    "prime_search",
    "parallel_search",
    "is_canonical",
    "get_legal_next_dimensions",
    "export_snake",
    "visualize_snake_3d",
    "visualize_snake_auto",
    "generate_16d_panel",
    "get_known_record",
    "get_known_snake",
    "KNOWN_RECORDS",
    "analyze_dimensions",
    "analyze_single_dimension",
    "generate_analysis_report",
    "generate_validation_report",
    "generate_performance_report",
    "generate_exponential_analysis_report",
    "calculate_snake_for_dimension",
]

