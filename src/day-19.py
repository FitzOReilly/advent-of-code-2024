import argparse
import os


def read_input(
    input_file: os.PathLike,
) -> tuple[list[str], list[str]]:
    desired = []
    with open(input_file, "r") as f:
        available = list(f.readline().strip("\n").split(", "))
        f.readline()
        while (line := f.readline().strip("\n")) != "":
            desired.append(line.strip("\n"))
    return available, desired


def count_possible(available: set[str], desired: list[str]) -> tuple[int, int]:
    possibility_count = init_possibilities(available)
    possible_pattern_count = 0
    possible_combination_count = 0
    for d in desired:
        count = count_possibilities(set(available), possibility_count, d)
        possible_pattern_count += 1 if count > 0 else 0
        possible_combination_count += count
    return possible_pattern_count, possible_combination_count


def init_possibilities(available: list[str]) -> dict:
    possibility_count = {}
    sorted_available = sorted(available, key=lambda a: len(a))
    for sa in sorted_available:
        possibility_count[sa] = 1 + count_possibilities(
            set(available), possibility_count, sa
        )
    return possibility_count


def count_possibilities(
    available: set[str], possibility_count: dict, pattern: str
) -> int:
    if pattern == "":
        return 1
    if pattern in possibility_count:
        return possibility_count[pattern]
    count = 0
    for length in range(1, len(pattern)):
        if pattern[:length] in available:
            count += count_possibilities(available, possibility_count, pattern[length:])
    possibility_count[pattern] = count
    return count


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str)
    args = parser.parse_args()
    input_file = args.input
    available, desired = read_input(input_file)
    possible_pattern_count, possible_combination_count = count_possible(
        available, desired
    )
    print(f"Day 19, Part 1: {possible_pattern_count}")
    print(f"Day 19, Part 2: {possible_combination_count}")
