"""
This creates program that executes `intcode` programs used in Santa's space shuttle.

Intcode program overview:
- A list of comma seperated integers
- Using the following opcodes to indicate operations
   - 1: Sum values of next 2 index's values, total stored in position indiciated by 3rd integer.
   - 2: Multiply values of next 2 index's values, total stored in position indiciated by 3rd integer.
   - 99: Program finish, halt.
"""
import pytest

test_cases = [
    ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
    ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
    ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
    ([1, 1, 1, 4, 88, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
]


@pytest.mark.parametrize("input, output", test_cases)
def test_intcode(input, output):
    assert parse_intcode(input) == output


def read_intcode(intcode_file):
    intcode = []
    with open(intcode_file, "r") as int_f:
        intcode = int_f.read().split(",")

    return list(map(int, intcode))


def parse_intcode(intcode):
    i = 0

    def intcode_op(num1, num2, total, op):
        num1_value = intcode[intcode[num1]]
        num2_value = intcode[intcode[num2]]
        total_position = intcode[total]
        if op == 1:
            intcode[total_position] = num1_value + num2_value
        if op == 2:
            intcode[total_position] = num1_value * num2_value

    while i < len(intcode):
        op_mode = intcode[i]
        if op_mode not in (1, 2, 99):
            raise ValueError(f"Invalid op code: {op_mode}")
        elif op_mode == 1 or op_mode == 2:
            intcode_op(i + 1, i + 2, i + 3, op_mode)
        else:
            return intcode

        i += 4


def intcode_executor(intcode_file):
    intcode = read_intcode(intcode_file)
    processed_intcode = parse_intcode(intcode)

    return processed_intcode


print(intcode_executor("./input"))
