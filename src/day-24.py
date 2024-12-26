import argparse
import os

type Gate = tuple[str, str, str, str]


def read_input(
    input_file: os.PathLike,
) -> tuple[dict, list[Gate]]:
    initial_values = {}
    gates = []
    with open(input_file, "r") as f:
        # Read the first section of the input until the blank line
        # (initial wire values)
        while (line := f.readline().strip("\n")) != "":
            wire, value = line.split(": ")
            initial_values[wire] = int(value)
        # Read the second section of the input (gates with connected wires)
        while (line := f.readline().strip("\n")) != "":
            in1, op, in2, _, out = line.split()
            gates.append((in1, op, in2, out))
    return initial_values, gates


def process_all_gates(initial_values: dict, gates: list[Gate]) -> dict:
    remaining = set(gates)
    values = initial_values.copy()
    while remaining:
        to_remove = set()
        for gate in remaining:
            in1, op, in2, out = gate
            if in1 in values and in2 in values:
                values[out] = process_gate(values[in1], op, values[in2])
                to_remove.add(gate)
        remaining -= to_remove
    return values


def process_gate(val1: int, op, val2: int) -> int:
    match op:
        case "AND":
            return val1 & val2
        case "OR":
            return val1 | val2
        case "XOR":
            return val1 ^ val2


def get_output(values: dict, prefix: str) -> int:
    result = 0
    for k, v in values.items():
        if k.startswith(prefix) and v == 1:
            result += 2 ** int(k.strip(prefix))
    return result


# Detect swapped gate outputs in the inner bits, i.e. all bits except the least
# and most significant one (LSB, MSB)
def detect_swapped(gates: list[Gate]) -> set[tuple[str, str]]:
    bit_count = sum(1 for gate in gates if gate[3].startswith("z"))
    swapped = set()
    _, _, _, c = find_gate(gates, "x00", "AND", "y00", None)
    for bit in range(1, bit_count - 1):
        c, bit_swapped = check_bit(gates, bit, c)
        swapped |= bit_swapped
    return swapped


# The gates form a full adder with inputs x, y and c_in (carry in) and outputs z
# and c_out (carry out), calculated as follows:
# - z = (x XOR y) XOR c_in
# - c_out = (x AND y) OR ((x XOR y) AND c_in)
# We define intermediate values
# - s = x XOR y
# - a = x AND y
# - b = s AND c_in
# We end up with 5 gates
# -     s = x XOR y
# -     z = s XOR c_in
# -     a = x AND y
# -     b = s AND c_in
# - c_out = a OR b
# This function checks for errors by comparing the expected vs the actual gate outputs.
# It does not work for the least and most significant bits (LSB, MSB).
def check_bit(
    gates: list[Gate], bit: int, c_in: str
) -> tuple[str, set[tuple[str, str]]]:
    swapped = set()
    x = f"x{bit:02}"
    y = f"y{bit:02}"

    # s gate should always exist, the output may be wrong though
    s_gate = find_gate(gates, x, "XOR", y, None)
    s = s_gate[3]

    fixed_s, fixed_c_in, z_swapped = check_z_gate(gates, bit, s, c_in)
    swapped |= z_swapped

    # a gate should always exist, the output may be wrong though
    a_gate = find_gate(gates, x, "AND", y, None)
    a = a_gate[3]

    # The inputs are the same as in the z gate, so possible errors in s or c_in
    # should already have been detected and fixed. The output (b) may still be
    # wrong.
    b_gate = find_gate(gates, fixed_s, "AND", fixed_c_in, None)
    b = b_gate[3]

    c_out, c_swapped = check_c_gate(gates, bit, a, b)
    swapped |= c_swapped

    return c_out, swapped


def check_z_gate(
    gates: list[Gate], bit: int, s: str, c_in: str
) -> tuple[str, str, set[tuple[str, str]]]:
    swapped = set()
    exp_z = f"z{bit:02}"
    fixed_s = s
    fixed_c_in = c_in
    z_gate = find_gate(gates, s, "XOR", c_in, None)
    if not z_gate:
        # One of the inputs is wrong, find out which (s or c_in)
        z_gate = find_gate(gates, None, "XOR", None, exp_z)
        z_in1, _, z_in2, _ = z_gate
        z_inputs = {z_in1, z_in2}
        if s not in z_inputs:
            z_inputs.remove(c_in)
            fixed_s = z_inputs.pop()
            swapped.add(tuple(sorted((s, fixed_s))))
        elif c_in not in z_inputs:
            z_inputs.remove(s)
            fixed_c_in = z_inputs.pop()
            swapped.add(tuple(sorted((c_in, fixed_c_in))))
    z = z_gate[3]
    if exp_z != z:
        # The output (z) is wrong
        swapped.add(tuple(sorted((exp_z, z))))
    return fixed_s, fixed_c_in, swapped


def check_c_gate(
    gates: list[Gate], bit: int, a: str, b: str
) -> tuple[str, set[tuple[str, str]]]:
    swapped = set()
    c_gate = find_gate(gates, a, "OR", b, None)
    if not c_gate:
        # One of the inputs is wrong, find out which (a or b)
        # The carry we're looking for will be XORed to calculate the next z, so
        # it must be one of the inputs of the next z gate
        next_z = f"z{bit+1:02}"
        next_z_gate = find_gate(gates, None, "XOR", None, next_z)
        next_z_in1, _, next_z_in2, _ = next_z_gate
        c_gate = find_gate(gates, a, "OR", None, next_z_in1)
        if not c_gate:
            c_gate = find_gate(gates, a, "OR", None, next_z_in2)
        if c_gate:
            c_in1, _, c_in2, c_out = c_gate
            c_inputs = {c_in1, c_in2} - {a}
            fixed_b = c_inputs.pop()
            swapped.add(tuple(sorted((b, fixed_b))))
            return c_out, swapped
        c_gate = find_gate(gates, None, "OR", b, next_z_in1)
        if not c_gate:
            c_gate = find_gate(gates, None, "OR", b, next_z_in2)
        if c_gate:
            c_in1, _, c_in2, c_out = c_gate
            c_inputs = {c_in1, c_in2} - {b}
            fixed_a = c_inputs.pop()
            swapped.add(tuple(sorted((a, fixed_a))))
            return c_out, swapped
    c_out = c_gate[3]
    return c_out, swapped


def find_gate(
    gates: list[Gate],
    exp_in1: str,
    exp_op: str,
    exp_in2: str,
    exp_out: str,
) -> Gate | None:
    for gate in gates:
        act_in1, act_op, act_in2, act_out = gate
        act_inputs = (act_in1, act_in2)
        if (
            exp_in1 in (None, *act_inputs)
            and exp_op in (None, act_op)
            and exp_in2 in (None, *act_inputs)
            and exp_out in (None, act_out)
        ):
            return gate
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str)
    args = parser.parse_args()
    input_file = args.input
    initial_values, gates = read_input(input_file)
    values = process_all_gates(initial_values, gates)
    output = get_output(values, "z")
    print(f"Day 24, Part 1: {output}")
    swapped = detect_swapped(gates)
    password = ",".join(sorted(elem for pair in swapped for elem in pair))
    print(f"Day 24, Part 2: {password}")
