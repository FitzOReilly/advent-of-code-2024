import argparse
import collections
import os


def read_input(
    input_file: os.PathLike,
) -> list[int]:
    numbers = []
    with open(input_file, "r") as f:
        for line in f:
            numbers.append(int(line.strip("\n")))
    return numbers


def calc_sum_of_secret_numbers_and_max_bananas(
    initial_numbers: list[int], generated_numbers_count: int, sequence_len: int
) -> tuple[int, int]:
    sum_of_secret_numbers = 0
    banana_count = {}
    for n in initial_numbers:
        price_changes = collections.deque(maxlen=sequence_len)
        seen_sequences = set()
        curr_price = n % 10
        # Use two separate loops to avoid checking
        # `if len(price_changes) == sequence_len` in the second one, which would
        # make the code slightly slower
        for _ in range(sequence_len - 1):
            n = next_secret_number(n)
            next_price = n % 10
            price_changes.append(next_price - curr_price)
            curr_price = next_price
        for _ in range(generated_numbers_count - sequence_len + 1):
            n = next_secret_number(n)
            next_price = n % 10
            price_changes.append(next_price - curr_price)
            curr_price = next_price
            sequence = ",".join(str(pc) for pc in price_changes)
            if sequence not in seen_sequences:
                banana_count[sequence] = banana_count.get(sequence, 0) + next_price
                seen_sequences.add(sequence)
        sum_of_secret_numbers += n
    max_bananas = max(bc for bc in banana_count.values())
    return sum_of_secret_numbers, max_bananas


def next_secret_number(number: int) -> int:
    number ^= number * 64
    number %= 16777216
    number ^= number // 32
    number %= 16777216
    number ^= number * 2048
    number %= 16777216
    return number


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str)
    args = parser.parse_args()
    input_file = args.input
    initial_numbers = read_input(input_file)
    generated_numbers_count = 2000
    sequence_len = 4
    sum_of_secret_numbers, max_bananas = calc_sum_of_secret_numbers_and_max_bananas(
        initial_numbers, generated_numbers_count, sequence_len
    )
    print(f"Day 22, Part 1: {sum_of_secret_numbers}")
    print(f"Day 22, Part 2: {max_bananas}")
