import argparse
import os


def read_input(
    input_file: os.PathLike,
) -> tuple[dict, list[tuple[str, str, str, str]]]:
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


def process_all_gates(
    initial_values: dict, gates: list[tuple[str, str, str, str]]
) -> dict:
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str)
    args = parser.parse_args()
    input_file = args.input
    initial_values, gates = read_input(input_file)
    values = process_all_gates(initial_values, gates)
    output = get_output(values, "z")
    password = "ddn,kqh,nhs,nnf,wrc,z09,z20,z34"
    print(f"Day 24, Part 1: {output}")
    print(f"Day 24, Part 2: {password} (solved by hand)")
