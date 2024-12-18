import argparse
import os


def read_input(
    input_file: os.PathLike,
) -> list[str]:
    grid = []
    with open(input_file, "r") as f:
        for line in f:
            grid.append(line.strip("\n"))
    return grid


def calc_fencing_price(grid: list[str]) -> tuple[int, int]:
    price_area_perimeter = 0
    price_area_sides = 0
    visited = set()
    to_visit = {(0, 0)}
    while to_visit:
        current = to_visit.pop()
        same_plant, not_same_plant, perimeter, sides = calc_area_perimeter_sides(
            current, grid
        )
        area = len(same_plant)
        price_area_perimeter += area * perimeter
        price_area_sides += area * sides
        visited |= same_plant
        to_visit -= same_plant
        to_visit |= {
            d for d in not_same_plant if is_within_bounds(d, grid) and d not in visited
        }
    return price_area_perimeter, price_area_sides


def calc_area_perimeter_sides(
    square: tuple[int, int], grid: list[str]
) -> tuple[set[tuple[int, int]], set[tuple[int, int]], int, int]:
    plant_type = grid[square[0]][square[1]]
    # Used to calculate the area
    same_plant = {square}
    # Different plant or outside the grid
    not_same_plant = set()
    perimeter = 0
    sides = 0
    to_visit = {square}
    while to_visit:
        current = to_visit.pop()
        neighbors = get_neighbors(current)
        neighbors_outside_plant = []
        for neighbor in neighbors:
            if (
                is_within_bounds(neighbor, grid)
                and grid[neighbor[0]][neighbor[1]] == plant_type
            ):
                if neighbor not in same_plant:
                    same_plant.add(neighbor)
                    to_visit.add(neighbor)
            else:
                neighbors_outside_plant.append(neighbor)
                not_same_plant.add(neighbor)
        corner_count = count_corners(current, plant_type, neighbors, grid)
        perimeter += len(neighbors_outside_plant)
        # The number of sides equals the number of corners
        sides += corner_count
    return same_plant, not_same_plant, perimeter, sides


def get_neighbors(square: tuple[int, int]) -> tuple[tuple[int, int]]:
    row = square[0]
    col = square[1]
    top = (row - 1, col)
    right = (row, col + 1)
    bottom = (row + 1, col)
    left = (row, col - 1)
    return top, right, bottom, left


def get_diag_neighbors(square: tuple[int, int]) -> tuple[tuple[int, int]]:
    row = square[0]
    col = square[1]
    top_left = (row - 1, col - 1)
    top_right = (row - 1, col + 1)
    bottom_right = (row + 1, col + 1)
    bottom_left = (row + 1, col - 1)
    return top_left, top_right, bottom_right, bottom_left


def is_within_bounds(square: tuple[int, int], grid: list[str]) -> bool:
    grid_size = (len(grid), len(grid[0]))
    return 0 <= square[0] < grid_size[0] and 0 <= square[1] < grid_size[1]


def count_corners(
    square: tuple[int, int],
    plant_type: str,
    neighbors: tuple[tuple[int, int]],
    grid: list[str],
) -> int:
    t, r, b, l = neighbors
    tl, tr, br, bl = get_diag_neighbors(square)
    top_same = is_within_bounds(t, grid) and grid[t[0]][t[1]] == plant_type
    right_same = is_within_bounds(r, grid) and grid[r[0]][r[1]] == plant_type
    bottom_same = is_within_bounds(b, grid) and grid[b[0]][b[1]] == plant_type
    left_same = is_within_bounds(l, grid) and grid[l[0]][l[1]] == plant_type
    top_left_same = is_within_bounds(tl, grid) and grid[tl[0]][tl[1]] == plant_type
    top_right_same = is_within_bounds(tr, grid) and grid[tr[0]][tr[1]] == plant_type
    bottom_right_same = is_within_bounds(br, grid) and grid[br[0]][br[1]] == plant_type
    bottom_left_same = is_within_bounds(bl, grid) and grid[bl[0]][bl[1]] == plant_type
    corner_count = 0
    if top_same:
        # Inward facing corners
        if left_same:
            if not top_left_same:
                corner_count += 1
        if right_same:
            if not top_right_same:
                corner_count += 1
    else:
        # Outward facing corners
        if not left_same:
            corner_count += 1
        if not right_same:
            corner_count += 1
    if bottom_same:
        # Inward facing corners
        if left_same:
            if not bottom_left_same:
                corner_count += 1
        if right_same:
            if not bottom_right_same:
                corner_count += 1
    else:
        # Outward facing corners
        if not left_same:
            corner_count += 1
        if not right_same:
            corner_count += 1
    return corner_count


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str)
    args = parser.parse_args()
    input_file = args.input
    grid = read_input(input_file)
    price_area_perimeter, price_area_sides = calc_fencing_price(grid)
    print(f"Day 12, Part 1: {price_area_perimeter}")
    print(f"Day 12, Part 2: {price_area_sides}")
