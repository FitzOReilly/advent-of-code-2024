import argparse
import heapq
import os
import re

type Robot = tuple[int, int, int, int]


def read_input(
    input_file: os.PathLike,
) -> list[Robot]:
    robots = []
    p = re.compile(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)")
    with open(input_file, "r") as f:
        for line in f:
            robot = tuple(int(n) for n in p.match(line.strip("\n")).groups())
            robots.append(robot)
    return robots


def calc_safety_factor(
    robots: list[Robot], width: int, height: int, seconds: int
) -> int:
    quadrants = [0, 0, 0, 0]
    for robot in robots:
        pos = calc_position(robot, width, height, seconds)
        if pos[0] < width // 2 and pos[1] < height // 2:
            quadrants[0] += 1
        if pos[0] < width // 2 and pos[1] > height // 2:
            quadrants[1] += 1
        if pos[0] > width // 2 and pos[1] > height // 2:
            quadrants[2] += 1
        if pos[0] > width // 2 and pos[1] < height // 2:
            quadrants[3] += 1
    return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]


def find_christmas_tree(
    robots: list[Robot], width: int, height: int, max_seconds: int, print_count: int = 0
) -> int:
    # Since we expect a lot of robots in a small area, this should lead to a low
    # safety factor (unless the tree is centered). So we manually inspect the
    # images with the lowest safety factors to find the solution.
    safety_factors = []
    for n in range(max_seconds):
        safety_factors.append((n, calc_safety_factor(robots, width, height, n)))
    # Prnt the images with the lowest safety factors (optional)
    smallest = heapq.nsmallest(print_count, safety_factors, key=lambda sf: sf[1])
    for s in smallest:
        print(s)
        print(format_pos(robots, width, height, s[0]))
    return heapq.nsmallest(1, safety_factors, key=lambda sf: sf[1])[0][0]


def format_pos(robots: list[Robot], width: int, height: int, seconds: int) -> str:
    grid = {}
    for robot in robots:
        pos = calc_position(robot, width, height, seconds)
        grid[(pos[0], pos[1])] = grid.get((pos[0], pos[1]), 0) + 1
    lines = []
    for row in range(height):
        lines.append("".join(f"{grid.get((col, row), ".")}" for col in range(width)))
    return "\n".join(lines)


def calc_position(
    robot: Robot, width: int, height: int, seconds: int
) -> tuple[int, int]:
    px, py, vx, vy = robot
    x = (px + seconds * vx) % width
    y = (py + seconds * vy) % height
    return x, y


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str)
    args = parser.parse_args()
    input_file = args.input
    robots = read_input(input_file)
    width = 101
    height = 103
    elapsed_seconds = 100
    max_elapsed_seconds = width * height
    safety_factor = calc_safety_factor(robots, width, height, elapsed_seconds)
    seconds_to_christmas_tree = find_christmas_tree(
        robots, width, height, max_elapsed_seconds
    )
    print(f"Day 14, Part 1: {safety_factor}")
    print(f"Day 14, Part 2: {seconds_to_christmas_tree}")
