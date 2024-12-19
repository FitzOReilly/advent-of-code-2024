import argparse
import os
import re

type ClawMachine = tuple[tuple[int, int], tuple[int, int], tuple[int, int]]


def read_input(
    input_file: os.PathLike,
) -> list[ClawMachine]:
    claw_machines = []
    p_button = re.compile(r"Button \w: X\+(\d+), Y\+(\d+)")
    p_prize = re.compile(r"Prize: X=(\d+), Y=(\d+)")
    with open(input_file, "r") as f:
        while (line := f.readline().strip("\n")) != "":
            a = tuple(int(n) for n in p_button.match(line).groups())
            line = f.readline().strip("\n")
            b = tuple(int(n) for n in p_button.match(line).groups())
            line = f.readline().strip("\n")
            prize = tuple(int(n) for n in p_prize.match(line).groups())
            _ = f.readline().strip("\n")
            claw_machines.append((a, b, prize))
    return claw_machines


def calc_total_tokens(claw_machines: list[ClawMachine], prize_offset: int = 0) -> int:
    tokens = 0
    for button_a, button_b, prize in claw_machines:
        tokens += calc_tokens(
            button_a, button_b, (prize[0] + prize_offset, prize[1] + prize_offset)
        )
    return tokens


def calc_tokens(
    button_a: tuple[int, int], button_b: tuple[int, int], prize: tuple[int, int]
) -> int:
    ax, ay = button_a
    bx, by = button_b
    px, py = prize
    b = round((ax * py - ay * px) / (ax * by - ay * bx))
    a = round((px - b * bx) / ax)
    if a * ax + b * bx == px and a * ay + b * by == py:
        return 3 * a + b
    else:
        return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str)
    args = parser.parse_args()
    input_file = args.input
    claw_machines = read_input(input_file)
    tokens = calc_total_tokens(claw_machines)
    tokens_with_offset = calc_total_tokens(claw_machines, 10000000000000)
    print(f"Day 13, Part 1: {tokens}")
    print(f"Day 13, Part 2: {tokens_with_offset}")
