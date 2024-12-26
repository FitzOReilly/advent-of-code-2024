import argparse
import os


def read_input(
    input_file: os.PathLike,
) -> dict:
    connections = {}
    with open(input_file, "r") as f:
        for line in f:
            comp1, comp2 = line.strip("\n").split("-")
            connections[comp1] = connections.get(comp1, set()) | {comp2}
            connections[comp2] = connections.get(comp2, set()) | {comp1}
    return connections


def get_sets_of_three_startswith_t(connections: dict) -> set[tuple[str]]:
    sets = set()
    for comp1, connected1 in connections.items():
        for comp2 in connected1:
            connected2 = connections[comp2]
            for comp3 in connected1 & connected2:
                set_of_three = tuple(sorted((comp1, comp2, comp3)))
                if any(comp.startswith("t") for comp in set_of_three):
                    sets.add(set_of_three)
    return sets


def find_maximal_cliques(connections: dict) -> list[set[str]]:
    max_cliques = []
    clique = set()
    candidates = {c for c in connections}
    excluded = set()
    bron_kerbosch(connections, max_cliques, clique, candidates, excluded)
    return max_cliques


def bron_kerbosch(
    connections: dict,
    max_cliques: list[set[str]],
    clique: set[str],
    candidates: set[str],
    excluded: set[str],
) -> None:
    if len(candidates) == 0 and len(excluded) == 0:
        max_cliques.append(clique)
        return
    while candidates:
        c = candidates.pop()
        neighbors = connections[c]
        bron_kerbosch(
            connections,
            max_cliques,
            clique | {c},
            candidates & neighbors,
            excluded & neighbors,
        )
        candidates -= {c}
        excluded |= {c}


def get_password(sets: list[set[str]]) -> str:
    longest_set = set()
    for s in sets:
        if len(s) > len(longest_set):
            longest_set = s
    password = ",".join(sorted(longest_set))
    return password


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str)
    args = parser.parse_args()
    input_file = args.input
    connections = read_input(input_file)
    sets_of_three = get_sets_of_three_startswith_t(connections)
    print(f"Day 23, Part 1: {len(sets_of_three)}")
    max_cliques = find_maximal_cliques(connections)
    password = get_password(max_cliques)
    print(f"Day 23, Part 2: {password}")
