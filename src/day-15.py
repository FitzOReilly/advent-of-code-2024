import argparse
import os


def read_input(
    input_file: os.PathLike,
) -> tuple[tuple[int, int], set[tuple[int, int]], set[tuple[int, int]], str]:
    boxes = set()
    walls = set()
    with open(input_file, "r") as f:
        row = 0
        while (line := f.readline().strip("\n")) != "":
            for col, char in enumerate(line):
                match char:
                    case "@":
                        robot = (row, col)
                    case "O":
                        boxes.add((row, col))
                    case "#":
                        walls.add((row, col))
                    case _:
                        pass
            row += 1
        moves = "".join(line.strip("\n") for line in f.readlines())
    return robot, boxes, walls, moves


def make_moves(
    robot: tuple[int, int],
    boxes: set[tuple[int, int]],
    walls: set[tuple[int, int]],
    moves: str,
) -> tuple[tuple[int, int], set[tuple[int, int]]]:
    direction = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}
    for m in moves:
        step = direction[m]
        target = (robot[0] + step[0], robot[1] + step[1])
        if target in boxes:
            should_move = move_boxes(boxes, walls, target, step)
        elif target in walls:
            should_move = False
        else:
            # Empty space
            should_move = True
        if should_move:
            robot = target
    return robot, boxes


def move_boxes(
    boxes: set[tuple[int, int]],
    walls: set[tuple[int, int]],
    origin: tuple[int, int],
    step: tuple[int, int],
) -> bool:
    box_moved = False
    target = (origin[0] + step[0], origin[1] + step[1])
    while target in boxes:
        target = (target[0] + step[0], target[1] + step[1])
    if target not in walls:
        boxes.remove(origin)
        boxes.add(target)
        box_moved = True
    return box_moved


def calc_sum_of_gps(boxes: set[tuple[int, int]]) -> int:
    sum_of_gps = 0
    for box in boxes:
        sum_of_gps += 100 * box[0] + box[1]
    return sum_of_gps


def convert_to_wide_warehouse(
    robot: tuple[int, int], boxes: set[tuple[int, int]], walls: set[tuple[int, int]]
) -> tuple[tuple[int, int], set[tuple[int, int]], set[tuple[int, int]]]:
    wide_robot = (robot[0], 2 * robot[1])
    wide_boxes = set()
    wide_walls = set()
    for box in boxes:
        wide_boxes.add((box[0], 2 * box[1]))
    for wall in walls:
        wide_walls.add((wall[0], 2 * wall[1]))
        wide_walls.add((wall[0], 2 * wall[1] + 1))
    return wide_robot, wide_boxes, wide_walls


def make_moves_wide_warehouse(
    robot: tuple[int, int],
    boxes: set[tuple[int, int]],
    walls: set[tuple[int, int]],
    moves: str,
) -> tuple[tuple[int, int], set[tuple[int, int]]]:
    direction = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}
    for m in moves:
        step = direction[m]
        target = (robot[0] + step[0], robot[1] + step[1])
        left_target = (target[0], target[1] - 1)
        if target in boxes:
            should_move = move_boxes_wide_warehouse(boxes, walls, target, step)
        elif left_target in boxes:
            should_move = move_boxes_wide_warehouse(boxes, walls, left_target, step)
        elif target in walls:
            should_move = False
        else:
            # Empty space
            should_move = True
        if should_move:
            robot = target
    return robot, boxes


def move_boxes_wide_warehouse(
    boxes: set[tuple[int, int]],
    walls: set[tuple[int, int]],
    origin: tuple[int, int],
    step: tuple[int, int],
) -> bool:
    box_moved = False
    match step:
        case (0, -1):
            box_moved = move_wide_boxes_left(boxes, walls, origin)
        case (0, 1):
            box_moved = move_wide_boxes_right(boxes, walls, origin)
        case _:
            if box_moved := can_move_wide_boxes_vertically(
                boxes, walls, origin, step[0]
            ):
                move_wide_boxes_vertically(boxes, walls, origin, step[0])
    return box_moved


def move_wide_boxes_left(
    boxes: set[tuple[int, int]], walls: set[tuple[int, int]], origin: tuple[int, int]
) -> bool:
    box_moved = False
    target = (origin[0], origin[1] - 1)
    left_target = (target[0], target[1] - 1)
    if left_target in boxes:
        move_wide_boxes_left(boxes, walls, left_target)
    if target not in walls and left_target not in boxes:
        boxes.remove(origin)
        boxes.add(target)
        box_moved = True
    return box_moved


def move_wide_boxes_right(
    boxes: set[tuple[int, int]], walls: set[tuple[int, int]], origin: tuple[int, int]
) -> bool:
    box_moved = False
    target = (origin[0], origin[1] + 1)
    right_target = (target[0], target[1] + 1)
    if right_target in boxes:
        move_wide_boxes_right(boxes, walls, right_target)
    if right_target not in walls and right_target not in boxes:
        boxes.remove(origin)
        boxes.add(target)
        box_moved = True
    return box_moved


def move_wide_boxes_vertically(
    boxes: set[tuple[int, int]],
    walls: set[tuple[int, int]],
    origin: tuple[int, int],
    vert_step: int,
) -> None:
    target = (origin[0] + vert_step, origin[1])
    left_target = (target[0], target[1] - 1)
    right_target = (target[0], target[1] + 1)
    if left_target in boxes:
        move_wide_boxes_vertically(boxes, walls, left_target, vert_step)
    if target in boxes:
        move_wide_boxes_vertically(boxes, walls, target, vert_step)
    if right_target in boxes:
        move_wide_boxes_vertically(boxes, walls, right_target, vert_step)
    boxes.remove(origin)
    boxes.add(target)


def can_move_wide_boxes_vertically(
    boxes: set[tuple[int, int]],
    walls: set[tuple[int, int]],
    origin: tuple[int, int],
    vert_step: int,
) -> bool:
    can_move = True
    target = (origin[0] + vert_step, origin[1])
    left_target = (target[0], target[1] - 1)
    right_target = (target[0], target[1] + 1)
    if left_target in boxes:
        can_move &= can_move_wide_boxes_vertically(boxes, walls, left_target, vert_step)
    if target in boxes:
        can_move &= can_move_wide_boxes_vertically(boxes, walls, target, vert_step)
    if right_target in boxes:
        can_move &= can_move_wide_boxes_vertically(
            boxes, walls, right_target, vert_step
        )
    can_move &= target not in walls and right_target not in walls
    return can_move


def format_normal_warehouse(robot, boxes, walls):
    rows = (
        max(robot[0], max(box[0] for box in boxes), max(wall[0] for wall in walls)) + 1
    )
    cols = (
        max(robot[1], max(box[1] for box in boxes), max(wall[1] for wall in walls)) + 1
    )
    lines = []
    for row in range(rows):
        line = []
        for col in range(cols):
            pos = (row, col)
            if pos == robot:
                line.append("@")
            elif pos in boxes:
                line.append("O")
            elif pos in walls:
                line.append("#")
            else:
                line.append(".")
        lines.append("".join(l for l in line))
    return "\n".join(lines)


def format_wide_warehouse(robot, boxes, walls):
    rows = (
        max(robot[0], max(box[0] for box in boxes), max(wall[0] for wall in walls)) + 1
    )
    cols = (
        max(robot[1], max(box[1] for box in boxes), max(wall[1] for wall in walls)) + 1
    )
    lines = []
    for row in range(rows):
        line = []
        col = 0
        while col < cols:
            pos = (row, col)
            if pos == robot:
                line.append("@")
            elif pos in boxes:
                line.append("[]")
                col += 1
            elif pos in walls:
                line.append("##")
                col += 1
            else:
                line.append(".")
            col += 1
        lines.append("".join(l for l in line))
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str)
    args = parser.parse_args()
    input_file = args.input
    robot, boxes, walls, moves = read_input(input_file)
    wide_robot, wide_boxes, wide_walls = convert_to_wide_warehouse(robot, boxes, walls)
    robot, boxes = make_moves(robot, boxes, walls, moves)
    sum_of_gps = calc_sum_of_gps(boxes)
    print(f"Day 15, Part 1: {sum_of_gps}")
    wide_robot, wide_boxes = make_moves_wide_warehouse(
        wide_robot, wide_boxes, wide_walls, moves
    )
    sum_of_gps_wide_warehouse = calc_sum_of_gps(wide_boxes)
    print(f"Day 15, Part 2: {sum_of_gps_wide_warehouse}")
