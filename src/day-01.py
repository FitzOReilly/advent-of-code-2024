import argparse
import os
from collections import Counter


def read_input(input_file: os.PathLike) -> tuple[int, int]:
    left = []
    right = []
    with open(input_file, "r") as f:
        for line in f:
            numbers = line.split()
            left.append(int(numbers[0]))
            right.append(int(numbers[1]))
    return left, right


def total_distance(left: list, right: list) -> int:
    left.sort()
    right.sort()
    total_distance = sum(abs(l - r) for l, r in zip(left, right))
    return total_distance


def similarity_score(left: list, right: list) -> int:
    right_counts = Counter(right)
    similarity_score = sum(right_counts[l] * l for l in left)
    return similarity_score


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str)
    args = parser.parse_args()
    left, right = read_input(args.input)
    print(f"Day 1, Part 1: {total_distance(left, right)}")
    print(f"Day 1, Part 2: {similarity_score(left, right)}")
