import argparse
import os
import re


def sum_of_multiplications(input_file: os.PathLike) -> int:
    p = re.compile(r"mul\((\d+),(\d+)\)")
    sum_of_muls = 0
    with open(input_file, "r") as f:
        for line in f:
            for m in p.finditer(line):
                sum_of_muls += int(m.group(1)) * int(m.group(2))
    return sum_of_muls


def sum_of_enabled_multiplications(input_file: os.PathLike) -> int:
    # Filter everything between the start of the string or "do()"
    # and the end of the string or "don't()"
    p_do = re.compile(r"(?:^|do\(\)).*?(?:$|don't\(\))")
    # Then filter for "mul(...)"
    p_mul = re.compile(r"mul\((\d+),(\d+)\)")
    sum_of_muls = 0
    with open(input_file, "r") as f:
        # Make sure to strip the newline characters
        content = "".join(line.strip("\n") for line in f.readlines())
    enabled_only = "".join(m.group() for m in p_do.finditer(content))
    for m in p_mul.finditer(enabled_only):
        sum_of_muls += int(m.group(1)) * int(m.group(2))
    return sum_of_muls


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str)
    args = parser.parse_args()
    input_file = args.input
    print(f"Day 3, Part 1: {sum_of_multiplications(input_file)}")
    print(f"Day 3, Part 2: {sum_of_enabled_multiplications(input_file)}")
