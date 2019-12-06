"""
This creates program that executes `intcode` programs used in Santa's space shuttle.

Intcode program overview:
- A list of comma seperated integers
- Using the following opcodes to indicate operations
    - 1, parameters 3, (num1, num2, sum_position)
        - Sum num1 and num2 and store in sum_position
    - 2, parameters 3, (num1, num2, mul_position)
        - Multiply num1 and num2 and store in mul_position
    - 3, parameters 1, (input_store_position)
        - Request user input for single int, store in input_store_position
    - 4, parameters 1, (output_position)
        - Print out value in output_positoin
    - 99, parameters 0
        - Program finish, halt.

- Parameter modes are stored in the same value as instruction's opcode
    - ABCDE
    - DE = opcode (2 digit)
    - ABC = parameter modes for each parameter position
        - A = parameter 3
        - B = parameter 2
        - C = parameter 1
    - Parameter modes:
        - 1 = immediate mode (use the parameter value as it is)
        - 0 = position mode (parameter value is a position to the requested value)
"""
import pytest

test_cases = [
    ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
    ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
    ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
    ([1, 1, 1, 4, 88, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
    ([1002, 4, 3, 4, 33], [1002, 4, 3, 4, 99]),
]


@pytest.mark.parametrize("input, output", test_cases)
def test_intcode(input, output):
    assert parse_intcode(input) == output


def read_intcode(intcode_file):
    intcode = []
    with open(intcode_file, "r") as int_f:
        intcode = int_f.read().split(",")

    return list(map(int, intcode))


def process_op_code(opcode):
    """
    - Validate op code
    - Determine instructions and parameter mode
    """
    op_mode = opcode % 100
    para_mode = opcode // 100

    param = []

    if op_mode not in (1, 2, 3, 4, 99):
        raise ValueError(f"Invalid op code: {op_mode}")

    for _ in range(3):
        param.append(para_mode % 10)
        para_mode //= 10

    return (op_mode, param)

def parse_intcode(intcode):
    i = 0

    def param_value(id, mode):
        if mode == 0:
            return intcode[intcode[id]]
        if mode == 1:
            return intcode[id]

    def intcode_op(index, op, param):
        step = 0
        if op == 1 or op == 2:
            value_1 = param_value(index + 1, param[0])
            value_2 = param_value(index + 2, param[1])
            value_3 = intcode[index + 3]
            step = 4
        elif op == 3 or op == 4:
            value_1 = param_value(index + 1, param[0])
            step = 2

        if op == 1:
            intcode[value_3] = value_1 + value_2
        elif op == 2:
            intcode[value_3] = value_1 * value_2
        elif op == 3:
            in_int = int(input("Input single int:"))
            if not 0 < in_int < 10:
                raise ValueError(f"Invalid input provided: {in_int}")
            intcode[value_1] = in_int
        elif op == 4:
            print(f"Output: {value_1}")
        else:
            raise ValueError(f"Invalid op code provided: {op}")

        return step

    while i < len(intcode):
        print("Before:", intcode)
        op_mode, param = process_op_code(intcode[i])
        if op_mode == 99:
            return intcode
        else:
            steps = intcode_op(i, op_mode, param)
        print(op_mode, param)
        print(intcode)

        i += steps


def intcode_executor(intcode_file, noun, verb):
    intcode = read_intcode(intcode_file)
    intcode[1] = noun
    intcode[2] = verb
    processed_intcode = parse_intcode(intcode)

    return processed_intcode[0]


def brute_force_intcode(intcode_file, expected_value):
    for noun in range(99):
        for verb in range(99):
            result = intcode_executor(intcode_file, noun, verb)
            if result == expected_value:
                return noun, verb

    return None


if __name__ == "__main__":
    print(intcode_executor("./input", 12, 2))
    print(brute_force_intcode("./input", 19690720))
