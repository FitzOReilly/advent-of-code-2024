import argparse
import os


def read_input(
    input_file: os.PathLike,
) -> list[int]:
    with open(input_file, "r") as f:
        stones = [int(n) for n in f.readline().strip("\n").split(" ")]
    return stones


def count_stones(stones: list[int], blink_count: int) -> int:
    return count_stones_recursively(stones, blink_count, {})


def count_stones_recursively(
    stones: list[int], blink_count: int, cache: dict[tuple[int]]
) -> int:
    if blink_count == 0:
        return len(stones)
    count = 0
    for stone in stones:
        if (stone, blink_count) in cache:
            count += cache[(stone, blink_count)]
        else:
            cache[(stone, blink_count)] = count_stones_recursively(
                blink(stone), blink_count - 1, cache
            )
            count += cache[(stone, blink_count)]
    return count


def blink(number: int) -> list[int]:
    if number == 0:
        return [1]
    elif (length := len(s := str(number))) % 2 == 0:
        return [int(s[: length // 2]), int(s[length // 2 :])]
    else:
        return [number * 2024]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str)
    args = parser.parse_args()
    input_file = args.input
    initial = read_input(input_file)
    print(f"Day 11, Part 1: {count_stones(initial, 25)}")
    print(f"Day 11, Part 2: {count_stones(initial, 75)}")
