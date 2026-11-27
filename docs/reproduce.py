"""Generate verified path measurements and a figure for the manuscript."""

import json
from pathlib import Path

import matplotlib.pyplot as plt

from snake_in_box import (
    get_known_record,
    get_known_snake,
    pruned_bfs_search,
    transition_to_vertex,
    validate_snake,
)
from snake_in_box.utils.visualize_advanced import visualize_snake_3d_advanced


ROOT = Path(__file__).resolve().parents[1]


def read_path(transitions: list[int], dimension: int) -> dict:
    vertices = transition_to_vertex(transitions, dimension)
    positions = {vertex: index for index, vertex in enumerate(vertices)}
    chords = sum(
        positions.get(vertex ^ (1 << bit), -1) > index + 1
        for index, vertex in enumerate(vertices)
        for bit in range(dimension)
    )
    adjacent = all((left ^ right).bit_count() == 1 for left, right in zip(vertices, vertices[1:]))
    valid, reason = validate_snake(vertices)
    if len(positions) != len(vertices) or not adjacent or chords or not valid:
        raise ValueError(f"Invalid induced path in dimension {dimension}: {reason}")
    return {"dimension": dimension, "edges": len(transitions), "vertices": len(vertices), "chords": chords}


def cube_maximum(path: tuple[int, ...] = (0,)) -> int:
    longest = len(path) - 1
    for bit in range(3):
        neighbor = path[-1] ^ (1 << bit)
        if all((neighbor ^ earlier).bit_count() > 1 for earlier in path[:-1]):
            longest = max(longest, cube_maximum((*path, neighbor)))
    return longest


def main() -> None:
    searches = []
    for dimension in (3, 4, 5):
        snake = pruned_bfs_search(dimension, memory_limit_gb=0.1, verbose=False)
        if snake is None or snake.get_length() != get_known_record(dimension):
            raise ValueError(f"Search did not reproduce the reference length in dimension {dimension}.")
        stats = read_path(snake.transition_sequence, dimension)
        stats["transitions"] = snake.transition_sequence
        stats["vertex_order"] = transition_to_vertex(snake.transition_sequence, dimension)
        searches.append(stats)
        if dimension == 3:
            if stats["edges"] != cube_maximum():
                raise ValueError("The cube result differs from the independently enumerated maximum.")
            figure = visualize_snake_3d_advanced(snake, show_plot=False)

    dated_results = []
    for dimension in range(11, 17):
        archive = ROOT / "output" / "crack_results" / f"dimension_{dimension}_best.json"
        stored = json.loads(archive.read_text())
        stats = read_path(stored["transition_sequence"], dimension)
        if stored["dimension"] != dimension or stored["length"] != stats["edges"]:
            raise ValueError(f"Inconsistent retained path metadata in {archive.name}.")
        dated_results.append({**stats, "source": archive.relative_to(ROOT).as_posix()})

    literature = []
    for dimension in (11, 12, 13):
        transitions = get_known_snake(dimension)
        if transitions is None:
            raise ValueError(f"Missing stored literature sequence in dimension {dimension}.")
        stats = read_path(transitions, dimension)
        if stats["edges"] != get_known_record(dimension):
            raise ValueError(f"Stored literature sequence disagrees with its length in dimension {dimension}.")
        literature.append({**stats, "source": "snake_in_box/benchmarks/known_snakes.py"})

    data = ROOT / "output" / "data"
    figures = ROOT / "output" / "figures"
    data.mkdir(parents=True, exist_ok=True)
    figures.mkdir(parents=True, exist_ok=True)
    measurements = {
        "fresh_searches": searches,
        "dated_results": dated_results,
        "literature_sequences": literature,
    }
    (data / "snake-evidence.json").write_text(json.dumps(measurements, indent=2) + "\n")
    figure.savefig(figures / "snake-cube.png", dpi=160, bbox_inches="tight")
    plt.close(figure)
    registry = {"figures": [{
        "label": "fig:snake-cube",
        "filename": "snake-cube.png",
        "caption": "The generated induced path through the cube.",
        "alt_text": "The highlighted path bends around the cube through five vertices.",
        "generated_by": "python -m docs.reproduce",
    }]}
    (figures / "figure_registry.json").write_text(json.dumps(registry, indent=2) + "\n")
    print("Verified three fresh paths, six dated paths, and three literature sequences.")


if __name__ == "__main__":
    main()
