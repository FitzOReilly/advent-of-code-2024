import argparse
import os


def count_unique_locations(
    input_file: os.PathLike,
) -> tuple[int, int]:
    grid = []
    with open(input_file, "r") as f:
        for line in f:
            grid.append(line.strip("\n"))
    grid_size = (len(grid), len(grid[0]))
    antennas = {}
    antinodes = set()
    antinodes_with_harmonics = set()
    for row, line in enumerate(grid):
        for col, symbol in enumerate(line):
            if symbol != ".":
                new_antenna = (row, col)
                antenna_locations = antennas.get(symbol, set())
                antinodes |= new_antinodes(new_antenna, antenna_locations, grid_size)
                antinodes_with_harmonics |= new_antinodes_with_harmonics(
                    new_antenna, antenna_locations, grid_size
                )
                antennas[symbol] = antenna_locations | {new_antenna}
    return len(antinodes), len(antinodes_with_harmonics)


def new_antinodes(
    new_antenna: tuple[int, int],
    antennas: set[tuple[int, int]],
    grid_size: tuple[int, int],
) -> set[tuple[int, int]]:
    antinodes = set()
    for old_antenna in antennas:
        diff = (new_antenna[0] - old_antenna[0], new_antenna[1] - old_antenna[1])
        new_location = (old_antenna[0] - diff[0], old_antenna[1] - diff[1])
        if is_within_bounds(new_location, grid_size):
            antinodes.add(new_location)
        new_location = (new_antenna[0] + diff[0], new_antenna[1] + diff[1])
        if is_within_bounds(new_location, grid_size):
            antinodes.add(new_location)
    return antinodes


def new_antinodes_with_harmonics(
    new_antenna: tuple[int, int],
    antennas: set[tuple[int, int]],
    grid_size: tuple[int, int],
) -> set[tuple[int, int]]:
    antinodes = set()
    for old_antenna in antennas:
        diff = (new_antenna[0] - old_antenna[0], new_antenna[1] - old_antenna[1])
        factor = 0
        while True:
            new_location = (
                old_antenna[0] - factor * diff[0],
                old_antenna[1] - factor * diff[1],
            )
            if is_within_bounds(new_location, grid_size):
                antinodes.add(new_location)
                factor += 1
            else:
                break
        factor = 0
        while True:
            new_location = (
                new_antenna[0] + factor * diff[0],
                new_antenna[1] + factor * diff[1],
            )
            if is_within_bounds(new_location, grid_size):
                antinodes.add(new_location)
                factor += 1
            else:
                break
    return antinodes


def is_within_bounds(position: tuple[int, int], grid_size: tuple[int, int]) -> bool:
    return 0 <= position[0] < grid_size[0] and 0 <= position[1] < grid_size[1]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str)
    args = parser.parse_args()
    input_file = args.input
    unique_location_count, unique_location_count_with_harmonics = (
        count_unique_locations(input_file)
    )
    print(f"Day 8, Part 1: {unique_location_count}")
    print(f"Day 8, Part 2: {unique_location_count_with_harmonics}")
