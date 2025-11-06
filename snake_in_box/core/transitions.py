"""Transition and vertex sequence conversion utilities."""

from typing import List, Union


def vertex_to_transition(vertex_sequence: List[int]) -> List[int]:
    """Convert vertex sequence to transition sequence.
    
    A transition sequence represents which bit position changes between
    consecutive vertices. For vertices v[i] and v[i+1], the transition
    is log2(v[i] XOR v[i+1]).
    
    Parameters
    ----------
    vertex_sequence : List[int]
        Ordered list of vertex labels (integers representing binary labels)
    
    Returns
    -------
    List[int]
        Transition sequence, where each element is the bit position that changes
    
    Examples
    --------
    >>> vertex_to_transition([0, 1, 3, 7, 6])
    [0, 1, 2, 0]
    >>> # 0->1: bit 0 changes, 1->3: bit 1 changes, 3->7: bit 2 changes, 7->6: bit 0 changes
    """
    if len(vertex_sequence) < 2:
        return []
    
    transitions = []
    for i in range(len(vertex_sequence) - 1):
        xor_result = vertex_sequence[i] ^ vertex_sequence[i + 1]
        
        if xor_result == 0:
            raise ValueError(
                f"Consecutive vertices {i} and {i+1} are identical: "
                f"{vertex_sequence[i]}"
            )
        
        # Find bit position: log2(xor_result)
        # Use bit_length() - 1 to get the position of the highest set bit
        # For powers of 2, this gives the correct bit position
        if xor_result & (xor_result - 1) != 0:
            # Not a power of 2 - multiple bits differ
            raise ValueError(
                f"Consecutive vertices {i} and {i+1} differ in multiple bits: "
                f"{bin(vertex_sequence[i])} vs {bin(vertex_sequence[i+1])}"
            )
        
        # For powers of 2, bit_length() gives log2 + 1, so subtract 1
        bit_position = xor_result.bit_length() - 1
        transitions.append(bit_position)
    
    return transitions


def transition_to_vertex(
    transition_sequence: List[int],
    dimension: int,
    start_vertex: int = 0
) -> List[int]:
    """Convert transition sequence to vertex sequence.
    
    Starting from start_vertex, apply each transition by flipping the
    corresponding bit position.
    
    Parameters
    ----------
    transition_sequence : List[int]
        Sequence of bit positions to flip
    dimension : int
        Dimension of hypercube (for validation)
    start_vertex : int, optional
        Starting vertex (default: 0, the origin)
    
    Returns
    -------
    List[int]
        Vertex sequence starting from start_vertex
    
    Examples
    --------
    >>> transition_to_vertex([0, 1, 2, 0], 3)
    [0, 1, 3, 7, 6]
    """
    vertices = [start_vertex]
    current = start_vertex
    
    for transition in transition_sequence:
        if transition < 0 or transition >= dimension:
            raise ValueError(
                f"Transition {transition} out of range [0, {dimension})"
            )
        
        # Flip bit at transition position
        current ^= (1 << transition)
        vertices.append(current)
    
    return vertices


def compute_current_vertex(transition_sequence: List[int]) -> int:
    """Compute current vertex from transition sequence.
    
    Starting from origin (0), apply all transitions to get final vertex.
    
    Parameters
    ----------
    transition_sequence : List[int]
        Sequence of bit positions to flip
    
    Returns
    -------
    int
        Final vertex after applying all transitions
    
    Examples
    --------
    >>> compute_current_vertex([0, 1, 2, 0])
    6
    """
    vertex = 0
    for transition in transition_sequence:
        vertex ^= (1 << transition)
    return vertex


def parse_hex_transition_string(hex_string: str) -> List[int]:
    """Parse transition sequence from hex string format.
    
    The paper uses hex digits (0-9, a-f) where a=10, b=11, etc.
    Commas and whitespace are ignored. This matches the C code format
    from the paper's appendix.
    
    Parameters
    ----------
    hex_string : str
        String containing hex digits representing transitions
    
    Returns
    -------
    List[int]
        Transition sequence as list of integers
    
    Examples
    --------
    >>> parse_hex_transition_string("0120")
    [0, 1, 2, 0]
    >>> parse_hex_transition_string("0,1,2,0")
    [0, 1, 2, 0]
    >>> parse_hex_transition_string("012a")
    [0, 1, 2, 10]
    """
    transitions = []
    hex_digits = "0123456789abcdef"
    
    for char in hex_string:
        char_lower = char.lower()
        if char_lower in hex_digits:
            digit_value = hex_digits.index(char_lower)
            transitions.append(digit_value)
        # Ignore commas, whitespace, and other characters
    
    return transitions


def transition_string_to_vertex_sequence(
    hex_string: str,
    dimension: int,
    start_vertex: int = 0
) -> List[int]:
    """Parse hex string and convert directly to vertex sequence.
    
    Convenience function combining parse_hex_transition_string and
    transition_to_vertex.
    
    Parameters
    ----------
    hex_string : str
        Hex string representation of transition sequence
    dimension : int
        Dimension of hypercube
    start_vertex : int, optional
        Starting vertex (default: 0)
    
    Returns
    -------
    List[int]
        Vertex sequence
    """
    transitions = parse_hex_transition_string(hex_string)
    return transition_to_vertex(transitions, dimension, start_vertex)

