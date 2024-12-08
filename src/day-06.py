import argparse
import os


def read_input(
    input_file: os.PathLike,
) -> tuple[tuple[int, int], tuple[int, int], set[tuple[int, int]]]:
    with open(input_file, "r") as f:
        start = None
        blocked = set()
        for row, line in enumerate(f):
            for col, square in enumerate(line.strip("\n")):
                if square == "#":
                    blocked.add((row, col))
                if square == "^":
                    start = (row, col)
        grid_size = (row + 1, col + 1)
    return grid_size, start, blocked


def count_visited_squares(
    grid_size: tuple[int, int], start: tuple[int, int], blocked: set[tuple[int, int]]
) -> int:
    # We start walking up, i.e. decrease the row number
    step = (-1, 0)
    square = start
    visited = set()
    while is_within_bounds(square, grid_size):
        visited.add(square)
        square, step = move_or_turn(square, step, blocked)
    return len(visited)


def count_obstructions_with_cycles(
    grid_size: tuple[int, int],
    start: tuple[int, int],
    blocked: set[tuple[int, int]],
) -> int:
    # We start walking up, i.e. decrease the row number
    step = (-1, 0)
    square = start
    obstructions_tried = set()
    cycle_count = 0
    while is_within_bounds(square, grid_size):
        next_square, next_step = move_or_turn(square, step, blocked)
        if next_square not in obstructions_tried and contains_cycle(
            grid_size, square, step, blocked | {next_square}
        ):
            cycle_count += 1
        obstructions_tried.add(next_square)
        square, step = next_square, next_step
    return cycle_count


def is_within_bounds(square: tuple[int, int], grid_size: tuple[int, int]) -> bool:
    return 0 <= square[0] < grid_size[0] and 0 <= square[1] < grid_size[1]


def move_or_turn(
    square: tuple[int, int], step: tuple[int, int], blocked: set[tuple[int, int]]
) -> tuple[tuple[int, int], tuple[int, int]]:
    next_ = (square[0] + step[0], square[1] + step[1])
    if next_ in blocked:
        step = rotate_right(step)
    else:
        square = next_
    return square, step


def rotate_right(step: tuple[int, int]) -> tuple[int, int]:
    next_step = {
        (-1, 0): (0, 1),  # Up -> right
        (0, 1): (1, 0),  # Right -> down
        (1, 0): (0, -1),  # Down -> left
        (0, -1): (-1, 0),  # Left -> up
    }
    return next_step[step]


def contains_cycle(
    grid_size: tuple[int, int],
    start: tuple[int, int],
    step: tuple[int, int],
    blocked: set[tuple[int, int]],
) -> bool:
    fast = (start, step)
    slow = (start, step)
    has_cycle = False
    while is_within_bounds(fast[0], grid_size):
        fast = move_or_turn(fast[0], fast[1], blocked)
        fast = move_or_turn(fast[0], fast[1], blocked)
        slow = move_or_turn(slow[0], slow[1], blocked)
        if fast == slow:
            has_cycle = True
            break
    return has_cycle


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str)
    args = parser.parse_args()
    input_file = args.input
    grid_size, start, blocked = read_input(input_file)
    print(f"Day 6, Part 1: {count_visited_squares(grid_size, start, blocked)}")
    print(f"Day 6, Part 2: {count_obstructions_with_cycles(grid_size, start, blocked)}")
