"""
Flawed frequency transmission
"""
import sys


def right_values(element_pos, max_size):
    base_pattern = [0, 1, 0 , -1]
    cur_value = 1
    mod_value = len(base_pattern) * element_pos
    size = 0

    while size != max_size:
        next = (cur_value % mod_value) / mod_value
        cur_value += 1
        size += 1
        result = None
        if next < 0.25:
            result = base_pattern[0]
        elif next < 0.50:
            result = base_pattern[1]
        elif next < 0.75:
            result = base_pattern[2]
        else:
            result = base_pattern[3]

        yield(result)


def fft(in_data, num_phases):
    in_data = [int(x) for x in str(in_data)]
    max_size = len(in_data)

    # loop in phase
    next_value = in_data
    for phase in range(num_phases):
        for i, _ in enumerate(in_data, start=1):
            sum = 0
            for x, y in zip(next_value, right_values(i, max_size)):
                sum += x * y
            next_value[i-1] = abs(sum) % 10

    leading_zeros = True
    result = 0
    for i in next_value:
        if not leading_zeros or i:
            leading_zeros = False
            result = result * 10 + i

    return result


def part2_calculation(offset, in_data, num_phases):
    in_data = [int(x) for x in str(in_data)]

    for phase in range(num_phases):
        print(f"Phase {phase+1}")
        partial_sum = sum(in_data[offset:])
        for i in range(offset, len(in_data)):
            temp = partial_sum
            partial_sum -= int(in_data[i])
            in_data[i] = abs(temp) % 10

    return in_data[offset:offset+8]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(f"To use: {sys.argv[0]} <input>")

    with open(sys.argv[1], "r") as in_f:
        in_data = in_f.read().strip()

    in_data = in_data * 10000
    offset = int(in_data[:7])
    print(offset)
    print(len(in_data))

    #print(fft(in_data, 1))
    print(part2_calculation(offset, in_data, 100))