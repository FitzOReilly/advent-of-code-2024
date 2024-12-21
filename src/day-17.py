import argparse
import os


def read_input(
    input_file: os.PathLike,
) -> tuple[int, int, int, list[int]]:
    with open(input_file, "r") as f:
        reg_a = int(f.readline().strip("\n").removeprefix("Register A: "))
        reg_b = int(f.readline().strip("\n").removeprefix("Register B: "))
        reg_c = int(f.readline().strip("\n").removeprefix("Register C: "))
        f.readline()
        program = [
            int(n)
            for n in f.readline().strip("\n").removeprefix("Program: ").split(",")
        ]
    return reg_a, reg_b, reg_c, program


def run_program(reg_a: int, reg_b: int, reg_c: int, program: list[int]) -> list[int]:
    instruction_pointer = 0
    full_output = []
    while instruction_pointer + 1 < len(program):
        opcode = program[instruction_pointer]
        operand = program[instruction_pointer + 1]
        reg_a, reg_b, reg_c, instruction_pointer, output = run_instruction(
            opcode, operand, reg_a, reg_b, reg_c, instruction_pointer
        )
        full_output.extend(output)
    return full_output


def find_self_producing(reg_b: int, reg_c: int, program: list[int]) -> set[int]:
    program_tail = []
    tail_start_idx = 0
    solutions = {}
    while len(program_tail) < len(program):
        tail_start_idx -= 1
        program_tail = program[tail_start_idx:]
        for tail_a in solutions.get(len(program_tail) - 1, {0}):
            for reg_a in (8 * tail_a + n for n in range(8)):
                output = run_program(reg_a, reg_b, reg_c, program)
                if output == program_tail:
                    solutions[len(output)] = solutions.get(len(output), set()) | {reg_a}
    initial_a = solutions.get(len(program), set())
    return initial_a


def run_instruction(
    opcode: int,
    operand: int,
    reg_a: int,
    reg_b: int,
    reg_c: int,
    instruction_pointer: int,
) -> tuple[int, int, int, int, list[int]]:
    instruction_pointer += 2
    output = []
    match opcode:
        case 0:  # adv
            reg_a = div(operand, reg_a, reg_b, reg_c)
        case 1:  # bxl
            reg_b = bxl(operand, reg_b)
        case 2:  # bst
            reg_b = bst(operand, reg_a, reg_b, reg_c)
        case 3:  # jnz
            instruction_pointer = jnz(operand, reg_a, instruction_pointer)
        case 4:  # bxc
            reg_b = bxc(reg_b, reg_c)
        case 5:  # out
            output.append(out(operand, reg_a, reg_b, reg_c))
        case 6:  # bdv
            reg_b = div(operand, reg_a, reg_b, reg_c)
        case 7:  # cdv
            reg_c = div(operand, reg_a, reg_b, reg_c)
    return reg_a, reg_b, reg_c, instruction_pointer, output


def div(operand: int, reg_a: int, reg_b: int, reg_c: int) -> int:
    denom = 2 ** combo(operand, reg_a, reg_b, reg_c)
    return reg_a // denom


def bxl(operand: int, reg_b: int) -> int:
    return reg_b ^ operand


def bst(operand: int, reg_a: int, reg_b: int, reg_c: int) -> int:
    return combo(operand, reg_a, reg_b, reg_c) % 8


def jnz(operand: int, reg_a: int, instruction_pointer: int) -> int:
    return instruction_pointer if reg_a == 0 else operand


def bxc(reg_b: int, reg_c: int) -> int:
    return reg_b ^ reg_c


def out(operand: int, reg_a: int, reg_b: int, reg_c: int) -> int:
    return combo(operand, reg_a, reg_b, reg_c) % 8


def combo(operand: int, reg_a: int, reg_b: int, reg_c: int) -> int:
    match operand:
        case 4:
            return reg_a
        case 5:
            return reg_b
        case 6:
            return reg_c
        case _:
            return operand


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str)
    args = parser.parse_args()
    input_file = args.input
    reg_a, reg_b, reg_c, program = read_input(input_file)
    output = run_program(reg_a, reg_b, reg_c, program)
    initial_a = find_self_producing(reg_b, reg_c, program)
    print(f"Day 17, Part 1: {",".join(f"{o}" for o in output)}")
    print(f"Day 17, Part 2: {min(initial_a)}")
