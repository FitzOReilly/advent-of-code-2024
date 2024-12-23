import argparse
import heapq
import os


def read_input(
    input_file: os.PathLike,
) -> tuple[tuple[int, int], tuple[int, int], set[tuple[int, int]], tuple[int, int]]:
    walls = set()
    grid_size = (None, None)
    height, width = 0, 0
    with open(input_file, "r") as f:
        for row, line in enumerate(f):
            height += 1
            width = 0
            for col, char in enumerate(line.strip("\n")):
                width += 1
                match char:
                    case "S":
                        start = (row, col)
                    case "E":
                        end = (row, col)
                    case "#":
                        walls.add((row, col))
                    case _:
                        pass
        grid_size = height, width
    return start, end, walls, grid_size


def get_cheats(
    start: tuple[int, int],
    end: tuple[int, int],
    walls: set[tuple[int, int]],
    grid_size: tuple[int, int],
    max_cheat_dist: int,
    min_saved: int,
) -> set[tuple[tuple[int, int], tuple[int, int]]]:
    dist_from_start = distances_between(start, end, walls, grid_size)
    dist_to_end = distances_between(end, start, walls, grid_size)
    legal_dist = dist_from_start[end]
    cheats = set()
    for current, current_dist in dist_from_start.items():
        if current_dist + min_saved <= legal_dist:
            for cheat, cheat_dist in possible_cheats(current, max_cheat_dist):
                if (
                    cheat in dist_to_end
                    and current_dist + cheat_dist + dist_to_end[cheat] + min_saved
                    <= legal_dist
                ):
                    cheats.add((current, cheat))
    return cheats


def distances_between(
    start: tuple[int, int],
    end: tuple[int, int],
    walls: set[tuple[int, int]],
    grid_size: tuple[int, int],
) -> dict:
    # Dijkstra's algorithm
    distance = {start: 0}
    current = start
    frontier = [(distance[current], current)]
    while frontier:
        current_dist, current = heapq.heappop(frontier)
        if current == end:
            break
        for neighbor in get_neighbors(current):
            if is_within_bounds(neighbor, grid_size) and neighbor not in walls:
                neighbor_dist = current_dist + 1
                if neighbor not in distance or neighbor_dist < distance[neighbor]:
                    distance[neighbor] = neighbor_dist
                    heapq.heappush(frontier, (neighbor_dist, neighbor))
    return distance


def get_neighbors(square: tuple[int, int]) -> tuple[tuple[int, int]]:
    row, col = square
    top = (row - 1, col)
    right = (row, col + 1)
    bottom = (row + 1, col)
    left = (row, col - 1)
    return top, right, bottom, left


def is_within_bounds(square: tuple[int, int], grid_size: tuple[int, int]) -> bool:
    return 0 <= square[0] < grid_size[0] and 0 <= square[1] < grid_size[1]


def possible_cheats(
    origin: tuple[int, int], max_cheat_dist: int
) -> list[tuple[tuple[int, int], int]]:
    row, col = origin
    cheats = []
    for row_diff in range(-max_cheat_dist, max_cheat_dist + 1):
        for col_diff in range(
            -max_cheat_dist + abs(row_diff), max_cheat_dist - abs(row_diff) + 1
        ):
            target = (row + row_diff, col + col_diff)
            target_dist = abs(row_diff) + abs(col_diff)
            cheats.append((target, target_dist))
    return cheats


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str)
    args = parser.parse_args()
    input_file = args.input
    start, end, walls, grid_size = read_input(input_file)
    cheats_2 = get_cheats(start, end, walls, grid_size, max_cheat_dist=2, min_saved=100)
    cheats_20 = get_cheats(
        start, end, walls, grid_size, max_cheat_dist=20, min_saved=100
    )
    print(f"Day 20, Part 1: {len(cheats_2)}")
    print(f"Day 20, Part 2: {len(cheats_20)}")
