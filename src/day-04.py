import argparse
import os


def read_input(input_file: os.PathLike) -> list[str]:
    grid = []
    with open(input_file, "r") as f:
        grid = [line.strip("\n") for line in f]
    return grid


def count_line(
    grid: list[str], start: tuple[int, int], step: tuple[int, int], searched: str
) -> int:
    count = 0
    min_row = 0
    min_col = 0
    max_row = len(grid) - 1
    max_col = len(grid[0]) - 1
    row, col = start
    searched_idx = 0
    while min_col <= col <= max_col and min_row <= row <= max_row:
        letter = grid[row][col]
        if letter == searched[searched_idx]:
            searched_idx += 1
            if searched_idx == len(searched):
                count += 1
                searched_idx = 0
        elif letter == searched[0]:
            searched_idx = 1
        else:
            searched_idx = 0
        row += step[0]
        col += step[1]
    return count


def a_coords(
    grid: list[str], start: tuple[int, int], step: tuple[int, int], searched: str
) -> set[tuple[int, int]]:
    coords = set()
    a_coords = (0, 0)
    min_row = 0
    min_col = 0
    max_row = len(grid) - 1
    max_col = len(grid[0]) - 1
    row, col = start
    searched_idx = 0
    while min_col <= col <= max_col and min_row <= row <= max_row:
        letter = grid[row][col]
        if letter == searched[searched_idx]:
            if letter == "A":
                a_coords = (row, col)
            searched_idx += 1
            if searched_idx == len(searched):
                coords.add(a_coords)
                searched_idx = 0
        elif letter == searched[0]:
            searched_idx = 1
        else:
            searched_idx = 0
        row += step[0]
        col += step[1]
    return coords


def count_xmas(grid: list[str]) -> int:
    searched = "XMAS"
    xmas_count = 0
    # Horizontal
    for row in range(len(grid)):
        start = (row, 0)
        step = (0, 1)
        xmas_count += count_line(grid, start, step, searched)
        # Backwards
        xmas_count += count_line(grid, start, step, searched[-1::-1])
    # Vertical
    for col in range(len(grid)):
        start = (0, col)
        step = (1, 0)
        xmas_count += count_line(grid, start, step, searched)
        # Backwards
        xmas_count += count_line(grid, start, step, searched[-1::-1])
    # Diagonal (top left - bottom right)
    # Start from left column
    for row in range(len(grid)):
        start = (row, 0)
        step = (1, 1)
        xmas_count += count_line(grid, start, step, searched)
        # Backwards
        xmas_count += count_line(grid, start, step, searched[-1::-1])
    # Start from top row
    # Make sure not to count the main diagonal twice
    for col in range(1, len(grid)):
        start = (0, col)
        step = (1, 1)
        xmas_count += count_line(grid, start, step, searched)
        # Backwards
        xmas_count += count_line(grid, start, step, searched[-1::-1])
    # Anti-diagonal (bottom left - top right)
    # Start from left column
    for row in range(len(grid)):
        start = (row, 0)
        step = (-1, 1)
        xmas_count += count_line(grid, start, step, searched)
        # Backwards
        xmas_count += count_line(grid, start, step, searched[-1::-1])
    # Start from bottom row
    # Make sure not to count the main diagonal twice
    for col in range(1, len(grid)):
        start = (len(grid) - 1, col)
        step = (-1, 1)
        xmas_count += count_line(grid, start, step, searched)
        # Backwards
        xmas_count += count_line(grid, start, step, searched[-1::-1])
    return xmas_count


def count_cross_mas(grid: list[str]) -> int:
    # Idea:
    # For each "X-MAS", there is a "MAS" in both the diagonal and the
    # anti-diagonal with matching "A" coordinates. So we store the "A"
    # coordinates for each "MAS" that we find in the diagonals and intersect
    # them with the anti-diagonal ones. Finally, we count them to get the
    # solution.
    searched = "MAS"
    # Diagonal (top left - bottom right)
    # Start from left column
    diag_coords = set()
    for row in range(len(grid)):
        start = (row, 0)
        step = (1, 1)
        diag_coords |= a_coords(grid, start, step, searched)
        # Backwards
        diag_coords |= a_coords(grid, start, step, searched[-1::-1])
    # Start from top row
    # Make sure not to count the main diagonal twice
    for col in range(1, len(grid)):
        start = (0, col)
        step = (1, 1)
        diag_coords |= a_coords(grid, start, step, searched)
        # Backwards
        diag_coords |= a_coords(grid, start, step, searched[-1::-1])
    # Anti-diagonal (bottom left - top right)
    # Start from left column
    antidiag_coords = set()
    for row in range(len(grid)):
        start = (row, 0)
        step = (-1, 1)
        antidiag_coords |= a_coords(grid, start, step, searched)
        # Backwards
        antidiag_coords |= a_coords(grid, start, step, searched[-1::-1])
    # Start from bottom row
    # Make sure not to count the main diagonal twice
    for col in range(1, len(grid)):
        start = (len(grid) - 1, col)
        step = (-1, 1)
        antidiag_coords |= a_coords(grid, start, step, searched)
        # Backwards
        antidiag_coords |= a_coords(grid, start, step, searched[-1::-1])
    intersection = diag_coords & antidiag_coords
    return len(intersection)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str)
    args = parser.parse_args()
    grid = read_input(args.input)
    print(f"Day 4, Part 1: {count_xmas(grid)}")
    print(f"Day 4, Part 2: {count_cross_mas(grid)}")
