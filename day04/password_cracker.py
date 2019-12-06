"""
Password cracker

This program takes a range of values and tests if they fit the conditions
of venus fuel depot's password

- It is a six-digit number.
- The value is within the range given in your puzzle input (197487-673251)
- Two adjacent digits are the same (like 22 in 122345).
- Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
- 2 adjacent matching digits are not part of a larger group of matching digits
"""
import pytest

test_cases = [
    (111111, False),
    (223450, False),
    (123789, False),
    (12789, False),
    (112233, True),
    (123444, False),
    (111122, True),
    (111222, False),
    (112222, True),
]

@pytest.mark.parametrize("passwd, valid", test_cases)
def test_password(passwd, valid):
    assert validate_pass(passwd) == valid

def validate_pass(passwd):
    if len(str(passwd)) != 6:
        return False

    valid_adj = False
    repeat_count = 0
    last_char = str(passwd)[0]

    for char in str(passwd)[1:]:
        if last_char == char:
            repeat_count += 1
        else:
            if repeat_count == 1:
                valid_adj = True
            repeat_count = 0

        if int(char) < int(last_char):
            return False

        last_char = char

    if repeat_count == 1:
        valid_adj = True

    return valid_adj


def possible_passwords(start, end):
    possible_passwds = []
    for passwd in range(start, end + 1):
        if validate_pass(passwd):
            possible_passwds.append(passwd)

    return possible_passwds

if __name__ == "__main__":
    # 197487-673251
    print(len(possible_passwords(197487, 673251)))