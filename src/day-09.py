import argparse
import os


def read_numbers(
    input_file: os.PathLike,
) -> list[int]:
    with open(input_file, "r") as f:
        numbers = [int(n) for n in f.readline().strip("\n")]
    return numbers


def read_blocks(
    input_file: os.PathLike,
) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    with open(input_file, "r") as f:
        numbers = [int(n) for n in f.readline().strip("\n")]
    it = iter(numbers + [0])
    file_blocks = []
    free_blocks = []
    pos = 0
    for file_len, free_len in zip(it, it):
        file_blocks.append((pos, file_len))
        pos += file_len
        if free_len > 0:
            free_blocks.append((pos, free_len))
            pos += free_len
    return file_blocks, free_blocks


def calc_checksum_file_blocks_fast(numbers: list[int]) -> int:
    checksum = 0
    pos = 0
    l_idx = 0
    r_idx = len(numbers) - 1
    if r_idx % 2 == 1:
        r_idx -= 1
    r_remaining = numbers[r_idx]

    while l_idx < r_idx:
        # Next file from left
        length = numbers[l_idx]
        id_ = l_idx // 2
        checksum += calc_checksum_block(id_, pos, length)
        pos += length
        l_idx += 1
        # Move file from right to a free block
        free = numbers[l_idx]
        while free > 0 and l_idx < r_idx:
            length = min(free, r_remaining)
            id_ = r_idx // 2
            checksum += calc_checksum_block(id_, pos, length)
            pos += length
            free -= length
            r_remaining -= length
            if r_remaining == 0:
                r_idx -= 2
                if l_idx < r_idx:
                    r_remaining = numbers[r_idx]
        l_idx += 1
    # Last file, parts of which have possibly been moved
    id_ = l_idx // 2
    length = r_remaining
    checksum += calc_checksum_block(id_, pos, length)
    return checksum


def calc_checksum_file_blocks_readable(
    file_blocks: list[tuple[int, int]],
    free_blocks: list[tuple[int, int]],
) -> int:
    checksum = 0
    first_free_idx = 0
    for file_id, (file_pos, file_len) in reversed(list(enumerate(file_blocks))):
        for free_idx, (free_pos, free_len) in enumerate(free_blocks[first_free_idx:], first_free_idx):
            if file_pos < free_pos:
                break
            if free_len > 0:
                length = min(file_len, free_len)
                checksum += calc_checksum_block(file_id, free_pos, length)
                free_pos += length
                free_len -= length
                free_blocks[free_idx] = (free_pos, free_len)
                file_len -= length
                if file_len == 0:
                    break
            first_free_idx += 1
        checksum += calc_checksum_block(file_id, file_pos, file_len)
    return checksum


def calc_checksum_whole_files(
    file_blocks: list[tuple[int, int]],
    free_blocks: list[tuple[int, int]],
) -> int:
    checksum = 0
    for file_id, (file_pos, file_len) in reversed(list(enumerate(file_blocks))):
        for free_idx, (free_pos, free_len) in enumerate(free_blocks):
            if file_pos < free_pos:
                break
            if file_len <= free_len:
                file_pos = free_pos
                free_pos += file_len
                free_len -= file_len
                if free_len == 0:
                    del free_blocks[free_idx]
                else:
                    free_blocks[free_idx] = (free_pos, free_len)
                break
        checksum += calc_checksum_block(file_id, file_pos, file_len)
    return checksum


def calc_checksum_block(file_id: int, start_pos: int, length: int) -> int:
    return int(file_id * (start_pos + (length - 1) / 2) * length)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str)
    args = parser.parse_args()
    input_file = args.input
    # numbers = read_numbers(input_file)
    # print(f"Day 9, Part 1: {calc_checksum_file_blocks_fast(numbers)}")
    file_blocks, free_blocks = read_blocks(input_file)
    print(f"Day 9, Part 1: {calc_checksum_file_blocks_readable(file_blocks, free_blocks)}")
    file_blocks, free_blocks = read_blocks(input_file)
    print(f"Day 9, Part 2: {calc_checksum_whole_files(file_blocks, free_blocks)}")
