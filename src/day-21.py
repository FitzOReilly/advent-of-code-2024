import argparse
import os

NUMERIC_KEYPAD = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    None: (3, 0),
    "0": (3, 1),
    "A": (3, 2),
}


DIRECTIONAL_KEYPAD = {
    None: (0, 0),
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}


def read_input(
    input_file: os.PathLike,
) -> list[str]:
    codes = []
    with open(input_file, "r") as f:
        for line in f:
            codes.append(line.strip("\n"))
    return codes


def complexity(code: str, levels: int) -> int:
    cache = {}
    seq_len = shortest_sequence_length(code, NUMERIC_KEYPAD, levels, cache)
    numeric_part = int(code.strip("A"))
    return seq_len * numeric_part


def shortest_sequence_length(code: str, keypad: dict, levels: int, cache: dict) -> int:
    if levels == 0:
        return len(code)
    total_length = 0
    current = "A"
    for c in code:
        sequences = next_char_sequence(current, c, keypad)
        lengths = []
        for seq in sequences:
            if (seq, levels - 1) in cache:
                length = cache[(seq, levels - 1)]
            else:
                length = shortest_sequence_length(
                    seq, DIRECTIONAL_KEYPAD, levels - 1, cache
                )
                cache[(seq, levels - 1)] = length
            lengths.append(length)
        total_length += min(lengths)
        current = c
    return total_length


def next_char_sequence(origin: str, target: str, keypad: dict) -> list[str]:
    current = keypad[origin]
    next_ = keypad[target]
    row_diff = next_[0] - current[0]
    col_diff = next_[1] - current[1]
    sequences = []
    vertical, horizontal = "", ""
    if row_diff < 0:
        vertical = -row_diff * "^"
    if row_diff > 0:
        vertical = row_diff * "v"
    if col_diff < 0:
        horizontal = -col_diff * "<"
    if col_diff > 0:
        horizontal = col_diff * ">"
    if (current[0] + row_diff, current[1]) != keypad[None]:
        sequences.append(f"{vertical}{horizontal}A")
    if (current[0], current[1] + col_diff) != keypad[None]:
        sequences.append(f"{horizontal}{vertical}A")
    return sequences


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str)
    args = parser.parse_args()
    input_file = args.input
    codes = read_input(input_file)
    sum_of_complexities_3 = sum(complexity(code, 3) for code in codes)
    print(f"Day 21, Part 1: {sum_of_complexities_3}")
    sum_of_complexities_26 = sum(complexity(code, 26) for code in codes)
    print(f"Day 21, Part 2: {sum_of_complexities_26}")
