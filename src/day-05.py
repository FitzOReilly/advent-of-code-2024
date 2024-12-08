import argparse
import functools
import os


def sum_of_middles(input_file: os.PathLike) -> tuple[int, int]:
    sum_of_correct_middles = 0
    sum_of_fixed_middles = 0
    after = {}
    with open(input_file, "r") as f:
        # Read the first section of the input until the blank line
        # (page ordering rules)
        while (line := f.readline().strip("\n")) != "":
            a, b = (int(n) for n in line.split("|"))
            after[a] = after.get(a, set()) | {b}
        # Read the second section of the input (updates)
        while (line := f.readline().strip("\n")) != "":
            numbers = [int(n) for n in line.split(",")]
            before = set()
            correctly_ordered = True
            for n in numbers:
                if len(before & after[n]) != 0:
                    correctly_ordered = False
                    break
                before |= {n}
            if correctly_ordered:
                middle = numbers[len(numbers) // 2]
                sum_of_correct_middles += middle
            else:
                fixed = fix_update(after, numbers)
                middle = fixed[len(fixed) // 2]
                sum_of_fixed_middles += middle
    return sum_of_correct_middles, sum_of_fixed_middles


def fix_update(after: set[int], update: list[int]) -> list[int]:
    compare = functools.partial(cmp_updates, after=after)
    return sorted(update, key=functools.cmp_to_key(compare))


def cmp_updates(a: int, b: int, after: set[int]) -> int:
    if b in after.get(a, set()):
        return -1
    if a in after.get(b, set()):
        return 1
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str)
    args = parser.parse_args()
    input_file = args.input
    sum_of_correct_middles, sum_of_fixed_middles = sum_of_middles(input_file)
    print(f"Day 5, Part 1: {sum_of_correct_middles}")
    print(f"Day 5, Part 2: {sum_of_fixed_middles}")
