"""Canonical form utilities for symmetry reduction."""

from typing import List


def is_canonical(transition_sequence: List[int]) -> bool:
    """Check if transition sequence follows Kochut's canonical form.
    
    Canonical form rules:
    - First digit must be 0
    - Each subsequent digit must be ≤ max_dimension_used + 1
    
    This ensures exactly one representative from each equivalence class
    of snakes related by hypercube symmetries.
    
    Parameters
    ----------
    transition_sequence : List[int]
        Transition sequence to check
    
    Returns
    -------
    bool
        True if sequence is in canonical form, False otherwise
    
    Examples
    --------
    >>> is_canonical([0, 1, 2, 0, 1])
    True
    >>> is_canonical([1, 0, 2])  # Doesn't start with 0
    False
    >>> is_canonical([0, 1, 3])  # 3 > max(0,1) + 1 = 2
    False
    """
    if not transition_sequence:
        return True
    
    # First digit must be 0
    if transition_sequence[0] != 0:
        return False
    
    # Track maximum dimension used so far
    max_dimension = 0
    
    for i, dim in enumerate(transition_sequence):
        # Each digit must be ≤ max_dimension + 1
        if dim > max_dimension + 1:
            return False
        
        # Update max_dimension if we've introduced a new dimension
        if dim == max_dimension + 1:
            max_dimension = dim
    
    return True


def get_legal_next_dimensions(transition_sequence: List[int]) -> List[int]:
    """Get legal next dimensions for canonical extension.
    
    For canonical form, the next dimension can be:
    - Any previously used dimension
    - Exactly one more than the maximum dimension used so far
    
    Parameters
    ----------
    transition_sequence : List[int]
        Current transition sequence (may be empty)
    
    Returns
    -------
    List[int]
        List of legal next dimension values
    
    Examples
    --------
    >>> get_legal_next_dimensions([])
    [0]
    >>> get_legal_next_dimensions([0])
    [0, 1]
    >>> get_legal_next_dimensions([0, 1, 2])
    [0, 1, 2, 3]
    >>> get_legal_next_dimensions([0, 1, 0, 2])
    [0, 1, 2, 3]
    """
    if not transition_sequence:
        # Empty sequence: first transition must be 0
        return [0]
    
    # Get maximum dimension used
    max_dim = max(transition_sequence)
    
    # Can use any previously used dimension or introduce max_dim + 1
    legal = list(set(transition_sequence))  # Unique previously used dimensions
    legal.append(max_dim + 1)  # Can introduce next dimension
    
    # Sort for consistency
    legal.sort()
    
    return legal

