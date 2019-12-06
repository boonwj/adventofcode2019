"""
Rocket Fuel, computes the fuel required to launch all modules
on Santa's spacecraft.

Advent of Code 2019: Day 1
"""

def required_fuel(mass):
    """
    Computes the fuel required.
    Fuel required is where mass, divide by three, round down, and subtract 2.
    """
    return mass // 3 - 2


def calculate_fuel(mass_file):
    total_fuel = 0
    with open(mass_file) as mass_f:
        for mass in mass_f:
            total_fuel += required_fuel(int(mass))

    return total_fuel


print(calculate_fuel("./input"))