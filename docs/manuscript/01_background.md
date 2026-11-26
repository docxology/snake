# Background

The hypercube graph has a vertex for each binary word of a fixed width and an
edge for each pair that differs in one bit. A snake is an induced path in this
graph. The coding-theory motivation, transition encoding, and search strategy
are described by @ace2025. That paper gives explicit lower bounds in dimensions
eleven through thirteen. Its copied PDF and text transcription are preserved
in the repository's reference directory.

The implementation starts at the all-zero word. A transition is the index of
a bit to flip. This encoding makes sequence length an edge count and keeps
the starting vertex implicit. Restricting new bit indices to first appearance
order removes equivalent coordinate permutations from the search.
