import argparse
import os


def total_calibration_result(
    input_file: os.PathLike,
) -> tuple[int, int]:
    two_op_total = 0
    three_op_total = 0
    with open(input_file, "r") as f:
        for line in f:
            test_value_str, numbers_str = line.strip("\n").split(":")
            test_value = int(test_value_str)
            numbers = [int(n) for n in numbers_str.strip(" ").split(" ")]
            if can_produce_2_op(test_value, numbers[0], numbers[1:]):
                two_op_total += test_value
            if can_produce_3_op(test_value, numbers[0], numbers[1:]):
                three_op_total += test_value
    return two_op_total, three_op_total


def can_produce_2_op(test_value: int, initial: int, remaining: list[int]) -> bool:
    if not remaining:
        return test_value == initial
    return can_produce_2_op(
        test_value, initial + remaining[0], remaining[1:]
    ) or can_produce_2_op(test_value, initial * remaining[0], remaining[1:])


def can_produce_3_op(test_value: int, initial: int, remaining: list[int]) -> bool:
    if not remaining:
        return test_value == initial
    return (
        can_produce_3_op(test_value, initial + remaining[0], remaining[1:])
        or can_produce_3_op(test_value, initial * remaining[0], remaining[1:])
        or can_produce_3_op(test_value, int(f"{initial}{remaining[0]}"), remaining[1:])
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str)
    args = parser.parse_args()
    input_file = args.input
    two_op_total, three_op_total = total_calibration_result(input_file)
    print(f"Day 7, Part 1: {two_op_total}")
    print(f"Day 7, Part 2: {three_op_total}")
