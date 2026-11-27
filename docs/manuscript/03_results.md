# Results

| Dimension | Fresh length in edges | Chords |
| --- | ---: | ---: |
| 3 | 4 | 0 |
| 4 | 7 | 0 |
| 5 | 13 | 0 |

The cube search found the vertex order `0, 1, 3, 7, 6`. The independent
enumeration found the same maximum length.

![The highlighted path bends around the cube through five vertices.](../../output/figures/snake-cube.png){#fig:snake-cube}

The replay checked the length, uniqueness, and induced-path property of
every retained sequence below. The dated search results were loaded from
the repository's output directory. The literature sequence lengths came
from the package's stored representation of the paper's transitions.

| Dimension | Dated result length in edges | Stored literature sequence length |
| --- | ---: | ---: |
| 11 | 374 | 732 |
| 12 | 733 | 1439 |
| 13 | 1440 | 2854 |
| 14 | 2855 | |
| 15 | 2856 | |
| 16 | 2857 | |

The render worktree's evidence file records each source path and the
validated edge, vertex and chord counts.
