import argparse
import heapq
import os


def read_input(
    input_file: os.PathLike,
) -> tuple[tuple[int, int], tuple[int, int], set[tuple[int, int]]]:
    walls = set()
    with open(input_file, "r") as f:
        for row, line in enumerate(f):
            for col, char in enumerate(line.strip("\n")):
                match char:
                    case "S":
                        start = (row, col)
                    case "E":
                        end = (row, col)
                    case "#":
                        walls.add((row, col))
                    case _:
                        pass
    return start, end, walls


def find_lowest_score(
    start: tuple[int, int], end: tuple[int, int], walls: set[tuple[int, int]]
) -> tuple[dict, dict]:
    # Nodes: ((row, col), axis), with axis: 0 vertical, 1 horizontal
    start_with_axis = (start, 1)
    score = {start_with_axis: 0}
    came_from = {start: set()}
    frontier = [(score[start_with_axis], start_with_axis)]
    while frontier:
        _, current = heapq.heappop(frontier)
        if (current[0][0], current[0][1]) == end:
            break
        for neighbor in get_neighbors(current, walls):
            new_score = score[current] + 1 + (neighbor[1] ^ current[1]) * 1000
            if neighbor in score and new_score == score[neighbor]:
                came_from[neighbor] = came_from.get(neighbor, set()) | {current}
            if neighbor not in score or new_score < score[neighbor]:
                score[neighbor] = new_score
                came_from[neighbor] = {current}
                heapq.heappush(frontier, (score[neighbor], neighbor))
    return score, came_from


def get_neighbors(
    tile: tuple[tuple[int, int], int], walls: set[tuple[int, int]]
) -> list[tuple[tuple[int, int], int]]:
    row = tile[0][0]
    col = tile[0][1]
    neighbors = []
    top = (row - 1, col)
    if top not in walls:
        neighbors.append((top, 0))
    right = (row, col + 1)
    if right not in walls:
        neighbors.append((right, 1))
    bottom = (row + 1, col)
    if bottom not in walls:
        neighbors.append((bottom, 0))
    left = (row, col - 1)
    if left not in walls:
        neighbors.append((left, 1))
    return neighbors


def tiles_on_best_paths(
    score: dict, came_from: dict, start: tuple[int, int], end: tuple[int, int]
) -> set[tuple[int, int]]:
    if (end, 0) not in score:
        to_visit = [(end, 1)]
    elif (end, 1) not in score:
        to_visit = [(end, 0)]
    elif score[(end, 0)] < score[(end, 1)]:
        to_visit = [(end, 0)]
    elif score[(end, 0)] > score[(end, 1)]:
        to_visit = [(end, 1)]
    elif score[(end, 0)] == score[(end, 1)]:
        to_visit = [(end, 0), (end, 1)]
    best_paths = {end}
    visited = set()
    while to_visit:
        current = to_visit.pop()
        if current in visited:
            continue
        prev = came_from.get(current, set())
        best_paths |= {p[0] for p in prev}
        to_visit.extend(prev)
        visited.add(current)
    return best_paths


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str)
    args = parser.parse_args()
    input_file = args.input
    start, end, walls = read_input(input_file)
    score, came_from = find_lowest_score(start, end, walls)
    end_score = score.get((end, 0), score.get((end, 1), None))
    best_paths = tiles_on_best_paths(score, came_from, start, end)
    print(f"Day 16, Part 1: {end_score}")
    print(f"Day 16, Part 2: {len(best_paths)}")
