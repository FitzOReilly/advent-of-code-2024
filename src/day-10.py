import argparse
import os


def read_input(
    input_file: os.PathLike,
) -> list[list[int]]:
    grid = []
    with open(input_file, "r") as f:
        for line in f:
            grid.append([int(n) for n in line.strip("\n")])
    return grid


def sum_of_trailhead_scores_and_ratings(grid: list[list[int]]) -> tuple[int, int]:
    sum_of_scores = 0
    sum_of_ratings = 0
    for row, line in enumerate(grid):
        for col, height in enumerate(line):
            if height != 0:
                continue
            nines_reached, trail_count = find_trails(grid, (row, col), height)
            sum_of_scores += len(nines_reached)
            sum_of_ratings += trail_count
    return sum_of_scores, sum_of_ratings


def find_trails(
    grid: list[list[int]], curr_square: tuple[int, int], curr_height: int
) -> tuple[set[tuple[int, int]], int]:
    if curr_height == 9:
        return {curr_square}, 1
    nines_reached = set()
    trail_count = 0
    for neighbor in get_neighbors(curr_square, grid):
        neighbor_height = grid[neighbor[0]][neighbor[1]]
        if neighbor_height != curr_height + 1:
            continue
        diff_nines_reached, diff_trail_count = find_trails(
            grid, neighbor, neighbor_height
        )
        nines_reached |= diff_nines_reached
        trail_count += diff_trail_count
    return nines_reached, trail_count


def get_neighbors(
    square: tuple[int, int], grid: list[list[int]]
) -> list[tuple[int, int]]:
    neighbors = []
    row = square[0]
    col = square[1]
    top = (row - 1, col)
    right = (row, col + 1)
    bottom = (row + 1, col)
    left = (row, col - 1)
    neighbors = [n for n in [top, right, bottom, left] if is_within_bounds(n, grid)]
    return neighbors


def is_within_bounds(square: tuple[int, int], grid: list[list[int]]) -> bool:
    grid_size = (len(grid), len(grid[0]))
    return 0 <= square[0] < grid_size[0] and 0 <= square[1] < grid_size[1]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str)
    args = parser.parse_args()
    input_file = args.input
    grid = read_input(input_file)
    sum_of_scores, sum_of_ratings = sum_of_trailhead_scores_and_ratings(grid)
    print(f"Day 10, Part 1: {sum_of_scores}")
    print(f"Day 10, Part 2: {sum_of_ratings}")
