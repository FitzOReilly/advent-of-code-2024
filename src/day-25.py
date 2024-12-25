import argparse
import os


def read_input(
    input_file: os.PathLike,
) -> tuple[list[tuple[int]], list[tuple[int]]]:
    locks = []
    keys = []
    with open(input_file, "r") as f:
        while (line := f.readline().strip("\n")) != "":
            if line[0] == "#":
                # Read lock
                pin_heights = [0] * len(line)
                while (lock_line := f.readline().strip("\n")) != "":
                    for idx, symbol in enumerate(lock_line):
                        if symbol == "#":
                            pin_heights[idx] += 1
                locks.append(tuple(pin_heights))
            else:
                # Read key
                # Start at -1 to compensate for the last line of "#" symbols
                pin_heights = [-1] * len(line)
                while (key_line := f.readline().strip("\n")) != "":
                    for idx, symbol in enumerate(key_line):
                        if symbol == "#":
                            pin_heights[idx] += 1
                keys.append(tuple(pin_heights))
    return locks, keys


def fits_together(lock: tuple[int], key: tuple[int]) -> bool:
    if len(lock) != len(key):
        return False
    return all(l + k <= 5 for l, k in zip(lock, key))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str)
    args = parser.parse_args()
    input_file = args.input
    locks, keys = read_input(input_file)
    pair_count = sum(int(fits_together(lock, key)) for lock in locks for key in keys)
    print(f"Day 25, Part 1: {pair_count}")
