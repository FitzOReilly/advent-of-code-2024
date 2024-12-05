import argparse
import os


def read_input(input_file: os.PathLike) -> list[list[int]]:
    levels = []
    with open(input_file, "r") as f:
        for line in f:
            numbers = [int(n) for n in line.split()]
            levels.append(numbers)
    return levels


def is_level_safe(numbers: list) -> int:
    diff = numbers[1] - numbers[0]
    if -3 <= diff <= -1:
        min_diff = -3
        max_diff = -1
    elif 1 <= diff <= 3:
        min_diff = 1
        max_diff = 3
    else:
        return False
    prev = numbers[1]
    for curr in numbers[2:]:
        diff = curr - prev
        if diff < min_diff or diff > max_diff:
            return False
        prev = curr
    return True


def count_safe_levels(levels: list[list[int]]) -> int:
    safe_count = 0
    for numbers in levels:
        if is_level_safe(numbers):
            safe_count += 1
    return safe_count


def count_safe_levels_with_problem_dampener(levels: list[list[int]]) -> int:
    safe_count = 0
    for numbers in levels:
        is_safe = False
        for skipped in range(len(numbers)):
            numbers_without_skipped = numbers[:skipped] + numbers[skipped + 1 :]
            if is_level_safe(numbers_without_skipped):
                is_safe = True
                break
        if is_safe:
            safe_count += 1
    return safe_count


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str)
    args = parser.parse_args()
    levels = read_input(args.input)
    print(f"Day 2, Part 1: {count_safe_levels(levels)}")
    print(f"Day 2, Part 2: {count_safe_levels_with_problem_dampener(levels)}")
