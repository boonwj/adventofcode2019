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
import sys
from itertools import permutations

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

    if op_mode not in (1, 2, 3, 4, 5, 6, 7, 8, 99):
        raise ValueError(f"Invalid op code: {op_mode}")

    for _ in range(3):
        param.append(para_mode % 10)
        para_mode //= 10

    return (op_mode, param)


def parse_intcode(intcode, input_list, index=0, pause_on_output=False):
    i = index
    output = []

    def param_value(id, mode):
        if mode == 0:
            return intcode[intcode[id]]
        if mode == 1:
            return intcode[id]

    def intcode_op(index, op, param):
        next_index = index
        if op == 1:
            next_index += 4
            value_1 = param_value(index + 1, param[0])
            value_2 = param_value(index + 2, param[1])
            value_3 = param_value(index + 3, 1)
            intcode[value_3] = value_1 + value_2
        elif op == 2:
            next_index += 4
            value_1 = param_value(index + 1, param[0])
            value_2 = param_value(index + 2, param[1])
            value_3 = param_value(index + 3, 1)
            intcode[value_3] = value_1 * value_2
        elif op == 3:
            next_index += 2
            value_1 = param_value(index + 1, 1)
            if input_list:
                in_int = input_list.pop(0)
            else:
                in_int = int(input("Input: "))
            intcode[value_1] = in_int
        elif op == 4:
            next_index += 2
            value_1 = param_value(index + 1, param[0])
            output.append(value_1)
            print(f"Output: {value_1}")
        elif op == 5:
            value_1 = param_value(index + 1, param[0])
            if value_1 != 0:
                next_index = param_value(index + 2, param[1])
            else:
                next_index += 3
        elif op == 6:
            value_1 = param_value(index + 1, param[0])
            if value_1 == 0:
                next_index = param_value(index + 2, param[1])
            else:
                next_index += 3
        elif op == 7:
            next_index += 4
            value_1 = param_value(index + 1, param[0])
            value_2 = param_value(index + 2, param[1])
            value_3 = param_value(index + 3, 1)
            intcode[value_3] = 1 if value_1 < value_2 else 0
        elif op == 8:
            next_index += 4
            value_1 = param_value(index + 1, param[0])
            value_2 = param_value(index + 2, param[1])
            value_3 = param_value(index + 3, 1)
            intcode[value_3] = 1 if value_1 == value_2 else 0
        else:
            raise ValueError(f"Invalid op code provided: {op}")

        return next_index

    while i < len(intcode):
        op_mode, param = process_op_code(intcode[i])
        if op_mode == 99:
            return output, intcode, -1
        else:
            i = intcode_op(i, op_mode, param)
        if op_mode == 4 and pause_on_output:
            return output, intcode, i


def intcode_executor(intcode_file, input_list=[]):
    intcode = read_intcode(intcode_file)
    output, intcode, index = parse_intcode(intcode, input_list, index=0)

    return output


def run_amplifier(program, phase_settings):
    signal = 0
    for i in range(5):
        input_list = [phase_settings[i], signal]
        output = intcode_executor(program, input_list)
        signal = output[0]

    return signal


def run_loopback(program, phase_settings):
    signal = 0
    intcode = read_intcode(program)
    amps = len(phase_settings)

    prog_states = [intcode.copy() for _ in range(amps)]
    index_states = [0] * amps
    input_states = [[x] for x in phase_settings]
    input_states[0].append(0)
    last_output = None

    while index_states[-1] != -1:
        for i in range(amps):
            output, intcode, index = parse_intcode(
                prog_states[i],
                input_list=input_states[i],
                index=index_states[i],
                pause_on_output=True,
            )
            input_states[i] = []
            prog_states[i] = intcode
            index_states[i] = index
            if index != -1:
                input_states[(i+1) % amps].append(output[0])
                last_output = output[0]

    return last_output

if __name__ == "__main__":
    program = "./input"
    if len(sys.argv) > 1:
        program = sys.argv[1]

    output = 0
    possible_settings = [5,6,7,8,9]
    for phase_settings in permutations(possible_settings):
        output = max(run_loopback(program, phase_settings), output)
    print(output)

    """
    output = 0
    setting_values = [0, 1, 2, 3, 4]
    for phase_settings in permutations(setting_values):
        result = run_amplifier(program, phase_settings)
        output = max(output, result)
    """