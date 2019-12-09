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
        - Print out value in output_position
    - 5, paramters 2, (t/f, position)
        - jump-if-true:
            - if the first parameter is non-zero, sets the instruction pointer to the value from the second parameter.
            - Otherwise, nothing.
    - 6, parameters 2, (t/f, position)
        - jump-if-false:
            - if the first parameter is zero, it sets the instruction pointer to the value from the second parameter.
            - Otherwise, it does nothing.
    - 7, parameters 3, (num1, num2, position)
        - is less than:
            - if the first parameter is less than the second parameter,
            - it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
    - 8, parameters 3, (num1, num2, position)
        - is equals:
            - if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter.
            - Otherwise, it stores 0.
    - 9, parameters 1, (num1)
        - adjust relative base by value of num1 (+ or -)
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
        - 0 = position mode (parameter value is a position to the requested value)
        - 1 = immediate mode (use the parameter value as it is)
        - 2 = relative mode (similar to position mode, but parameters count from a relative base, starting from 0)
            - relative base 0 == position mode
            - relative base value is changed by opmode 9
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
    # assert parse_intcode(input) == output
    pass

class IntCode:
    def __init__(self, program):
        self.program = program
        self.addr = 0
        self.rel_base = 0
        self.output = []
        self.input = []
        self.op_modes = {
            1: "SUM",
            2: "MUL",
            3: "IN",
            4: "OUT",
            5: "JUMP_T",
            6: "JUMP_F",
            7: "LESS",
            8: "EQUALS",
            9: "ADJ_REL",
            99: "END",
        }
        self.param_modes = {
            0: "POS",
            1: "IMM",
            2: "REL",
        }

    @classmethod
    def from_ext_file(cls, program_file):
        intcode = []
        with open(program_file, "r") as int_f:
            intcode = int_f.read().split(",")

        return cls(list(map(int, intcode)))

    def _compute_op_code(self, op_code):
        op_mode = op_code % 100
        param_mode = op_code // 100

        param_mode_map = {}

        if op_mode not in self.op_modes:
            raise ValueError(f"Invalid op code: {op_mode} - {op_code}")

        i = 0
        while param_mode:
            i += 1
            param_mode_map[i] = param_mode % 10
            param_mode //= 10

        return (op_mode, param_mode_map)

    def _get_value(self, offset, mode_map):
        mode = mode_map.get(offset, 0)
        mode_name = self.param_modes[mode]
        addr = self.addr + offset

        if mode_name == "POS":
            pt_addr = self.program[addr]
            if pt_addr >= len(self.program):
                return 0
            else:
                return self.program[pt_addr]
        elif mode_name == "IMM":
            return self.program[addr]
        elif mode_name == "REL":
            return self.program[self.rel_base + self.program[addr]]
        else:
            raise KeyError(f"Invalid parameter mode: {mode_name}")

    def _assign(self, tgt_addr, value):
        if tgt_addr < 0:
            raise IndexError(f"Negative address error: {tgt_addr}")
        if tgt_addr >= len(self.program):
            diff = tgt_addr - len(self.program) + 1
            self.program.extend([0] * diff)
        self.program[tgt_addr] = value

    def _execute(self, op_mode, param_mode_map):
        op_name = self.op_modes[op_mode]
        ref = self.addr

        if op_name == "SUM":
            p1 = self._get_value(1, param_mode_map)
            p2 = self._get_value(2, param_mode_map)
            p3 = self.program[ref + 3]
            self._assign(p3, p1 + p2)
            self.addr += 4

        elif op_name == "MUL":
            p1 = self._get_value(1, param_mode_map)
            p2 = self._get_value(2, param_mode_map)
            p3 = self.program[ref + 3]
            self._assign(p3, p1 * p2)
            self.addr += 4

        elif op_name == "IN":
            p1 = self.program[self.addr + 1]
            if not self.input:
                self.input.append(int(input("Input: ")))
            self._assign(p1, self.input.pop(0))
            self.addr += 2

        elif op_name == "OUT":
            p1 = self._get_value(1, param_mode_map)
            self.output.append(p1)
            self.addr += 2

        elif op_name == "JUMP_T":
            p1 = self._get_value(1, param_mode_map)
            if p1 != 0:
                self.addr = self._get_value(2, param_mode_map)
            else:
                self.addr += 3

        elif op_name == "JUMP_F":
            p1 = self._get_value(1, param_mode_map)
            if p1 == 0:
                self.addr = self._get_value(2, param_mode_map)
            else:
                self.addr += 3

        elif op_name == "LESS":
            p1 = self._get_value(1, param_mode_map)
            p2 = self._get_value(2, param_mode_map)
            p3 = self.program[ref + 3]
            value = 1 if p1 < p2 else 0
            self._assign(p3, value)
            self.addr += 4

        elif op_name == "EQUALS":
            p1 = self._get_value(1, param_mode_map)
            p2 = self._get_value(2, param_mode_map)
            p3 = self.program[ref + 3]
            value = 1 if p1 == p2 else 0
            self._assign(p3, value)
            self.addr += 4

        elif op_name == "ADJ_REL":
            p1 = self._get_value(1, param_mode_map)
            self.rel_base += p1
            self.addr += 2

        elif op_name == "END":
            print("Program reached its end!")

        else:
            raise ValueError(f"Invalid op code provided: {op}")

        return op_name

    def run(self, pause_on_output=False):
        exec = True
        while exec:
            if self.addr >= len(self.program):
                raise OverflowError(f"Current address ({self.addr}) exceeds program size ({len(self.program)})")

            op_mode, param_mode_map = self._compute_op_code(self.program[self.addr])
            exec_op = self._execute(op_mode, param_mode_map)

            if exec_op == "END" or (exec_op == "OUT" and pause_on_output):
                exec = False

        return self.output

    def add_input(self, value):
        self.input.append(value)


if __name__ == "__main__":
    program = "./input"
    if len(sys.argv) > 1:
        program = sys.argv[1]

    intcode_prog = IntCode.from_ext_file(program)
    output = intcode_prog.run()

    print(output)
