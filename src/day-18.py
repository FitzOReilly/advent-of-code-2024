import argparse
import heapq
import os


def read_input(
    input_file: os.PathLike,
) -> list[tuple[int, int]]:
    blocked = []
    with open(input_file, "r") as f:
        for line in f:
            blocked.append(tuple(int(n) for n in line.strip("\n").split(",")))
    return blocked


def shortest_path(
    start: tuple[int, int],
    end: tuple[int, int],
    blocked: set[tuple[int, int]],
    grid_size: tuple[int, int],
) -> int | None:
    # Dijkstra's algorithm
    steps = {start: 0}
    current = start
    frontier = [(steps[current], current)]
    while frontier:
        current_steps, current = heapq.heappop(frontier)
        if current == end:
            break
        for neighbor in get_neighbors(current):
            if is_within_bounds(neighbor, grid_size) and neighbor not in blocked:
                neighbor_steps = current_steps + 1
                if neighbor not in steps or neighbor_steps < steps[neighbor]:
                    steps[neighbor] = neighbor_steps
                    heapq.heappush(frontier, (neighbor_steps, neighbor))
    return steps.get(end, None)


def find_first_preventing(
    start: tuple[int, int],
    end: tuple[int, int],
    blocked: set[tuple[int, int]],
    grid_size: tuple[int, int],
) -> tuple[int, int]:
    # Binary search
    lo = 0
    hi = len(blocked)
    while lo < hi - 1:
        mid = lo + (hi - lo) // 2
        first_n_blocked = set(blocked[:mid])
        if shortest_path(start, end, first_n_blocked, grid_size) is None:
            hi = mid
        else:
            lo = mid
    return blocked[lo]


def get_neighbors(square: tuple[int, int]) -> tuple[tuple[int, int]]:
    row = square[0]
    col = square[1]
    top = (row - 1, col)
    right = (row, col + 1)
    bottom = (row + 1, col)
    left = (row, col - 1)
    return top, right, bottom, left


def is_within_bounds(square: tuple[int, int], grid_size: tuple[int, int]) -> bool:
    return 0 <= square[0] < grid_size[0] and 0 <= square[1] < grid_size[1]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str)
    args = parser.parse_args()
    input_file = args.input
    blocked = read_input(input_file)
    grid_size = (71, 71)
    first_1024_blocked = set(blocked[:1024])
    start = (0, 0)
    end = (grid_size[0] - 1, grid_size[1] - 1)
    steps_to_end = shortest_path(start, end, first_1024_blocked, grid_size)
    first_preventing = find_first_preventing(start, end, blocked, grid_size)
    print(f"Day 18, Part 1: {steps_to_end}")
    print(f"Day 18, Part 2: {",".join(f"{n}" for n in first_preventing)}")
