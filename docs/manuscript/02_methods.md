# Methods

The search enumerates a frontier of paths and attempts the next legal
transition from each endpoint. Occupied vertices and neighbors of earlier
vertices along already used coordinates are marked in a bitmap. A free
neighbor of the endpoint can extend the path. Once the path leaves the
endpoint, its neighbors in used coordinates become prohibited by the induced
path condition. This update allows the search to revisit a previously used
coordinate without admitting a chord.

The solver ranks an oversized frontier by the count of unmarked vertices.
Its memory argument guides pruning after expansion. The resulting path can
be checked independently of these search choices. For each generated or
retained path, the replay compares consecutive vertices, checks uniqueness,
and enumerates occupied neighbors at each vertex. Any neighbor whose position
is more than one step away constitutes a chord. The replay also invokes the
package's public validator.

The final method check uses an exhaustive walk of the cube from its origin
without coordinate symmetry reduction. This gives an independent maximum for
the cube example. The other small searches are compared with the package's
literature table.
