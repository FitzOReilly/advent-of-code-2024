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


def get_sets_of_computers(connections: dict) -> list[set[str]]:
    sets = []
    for comp, connected in connections.items():
        additional_sets = [{comp}]
        for s in sets:
            if s <= connected | {comp}:
                additional_sets.append(s | {comp})
        sets.extend(additional_sets)
    return sets


def filter_by_len_and_prefix(
    sets: list[set[str]], length: int, prefix: str
) -> list[str]:
    filtered_sets = []
    for s in sets:
        if len(s) == length and any(comp.startswith(prefix) for comp in s):
            filtered_sets.append(",".join(sorted(s)))
    return filtered_sets


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
    all_sets = get_sets_of_computers(connections)
    sets_of_three = filter_by_len_and_prefix(all_sets, 3, "t")
    password = get_password(all_sets)
    print(f"Day 23, Part 1: {len(sets_of_three)}")
    print(f"Day 23, Part 2: {password}")
