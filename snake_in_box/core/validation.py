"""Validation functions for snake-in-the-box solutions."""

from typing import List, Tuple
from .transitions import transition_to_vertex


def hamming_distance(a: int, b: int) -> int:
    """Calculate Hamming distance between two integers.
    
    Hamming distance is the number of bit positions where the two
    binary representations differ.
    
    Parameters
    ----------
    a : int
        First integer
    b : int
        Second integer
    
    Returns
    -------
    int
        Number of differing bits
    
    Examples
    --------
    >>> hamming_distance(0b000, 0b001)
    1
    >>> hamming_distance(0b000, 0b111)
    3
    """
    return bin(a ^ b).count('1')


def validate_snake(vertex_sequence: List[int]) -> Tuple[bool, str]:
    """Validate that a vertex sequence represents a valid snake.
    
    A valid snake must satisfy:
    1. Consecutive vertices have Hamming distance exactly 1
    2. Non-consecutive vertices have Hamming distance > 1
    
    This translates the C validation logic from the paper's appendix.
    
    Parameters
    ----------
    vertex_sequence : List[int]
        List of vertices in snake path
    
    Returns
    -------
    Tuple[bool, str]
        (is_valid, error_message)
        If valid, returns (True, "Valid snake")
        If invalid, returns (False, descriptive error message)
    
    Examples
    --------
    >>> validate_snake([0, 1, 3, 7, 6])
    (True, 'Valid snake')
    >>> validate_snake([0, 1, 0])  # Invalid: 0 and 2 are adjacent
    (False, 'Non-consecutive vertices 0 and 2 have Hamming distance 0, must be > 1')
    """
    n = len(vertex_sequence)
    
    if n < 2:
        return True, "Valid snake (trivial case)"
    
    # Check consecutive vertices have Hamming distance 1
    for i in range(n - 1):
        hamming_dist = hamming_distance(vertex_sequence[i], vertex_sequence[i + 1])
        if hamming_dist != 1:
            return False, (
                f"Consecutive vertices {i} and {i+1} have Hamming distance "
                f"{hamming_dist}, expected 1"
            )
    
    # Check non-consecutive vertices have Hamming distance > 1
    # This matches the C code: for (i = 2; i <= len; i++)
    #   for (j = 0; j <= i - 2; j++)
    for i in range(2, n):
        for j in range(i - 1):  # j from 0 to i-2 (inclusive)
            hamming_dist = hamming_distance(vertex_sequence[i], vertex_sequence[j])
            if hamming_dist <= 1:
                return False, (
                    f"Non-consecutive vertices {j} and {i} have Hamming distance "
                    f"{hamming_dist}, must be > 1"
                )
    
    return True, "Valid snake"


def validate_transition_sequence(
    transition_sequence: List[int],
    dimension: int
) -> Tuple[bool, str]:
    """Validate transition sequence and convert to check snake validity.
    
    First converts transition sequence to vertex sequence, then validates
    the resulting snake.
    
    Parameters
    ----------
    transition_sequence : List[int]
        Transition sequence to validate
    dimension : int
        Dimension of hypercube
    
    Returns
    -------
    Tuple[bool, str]
        (is_valid, error_message)
    """
    if not transition_sequence:
        return True, "Valid snake (empty sequence)"
    
    # Check transitions are in valid range
    for i, trans in enumerate(transition_sequence):
        if trans < 0 or trans >= dimension:
            return False, (
                f"Transition {i} has value {trans}, "
                f"must be in range [0, {dimension})"
            )
    
    # Convert to vertex sequence and validate
    try:
        vertices = transition_to_vertex(transition_sequence, dimension)
    except ValueError as e:
        return False, f"Invalid transition sequence: {e}"
    
    return validate_snake(vertices)


def validate_snake_from_hex_string(
    hex_string: str,
    dimension: int
) -> Tuple[bool, str]:
    """Parse hex string and validate the resulting snake.
    
    Convenience function that combines parsing and validation.
    
    Parameters
    ----------
    hex_string : str
        Hex string representation of transition sequence
    dimension : int
        Dimension of hypercube
    
    Returns
    -------
    Tuple[bool, str]
        (is_valid, error_message)
    """
    from .transitions import parse_hex_transition_string
    
    try:
        transitions = parse_hex_transition_string(hex_string)
    except Exception as e:
        return False, f"Failed to parse hex string: {e}"
    
    return validate_transition_sequence(transitions, dimension)

