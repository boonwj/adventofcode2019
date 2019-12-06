"""
Rocket Fuel v2, computes the fuel required to launch all modules
on Santa's spacecraft.

This implementation takes into account the fuel required to carry the fuel
necessary to carry the modules.
"""


def required_fuel(mass):
    """
    Computes the fuel required.
    Fuel required is where mass, divide by three, round down, and subtract 2.
    """
    fuel = mass // 3 - 2

    if fuel < 0:
        return 0

    return fuel + required_fuel(fuel)


def calculate_fuel(mass_file):
    total_fuel = 0
    with open(mass_file) as mass_f:
        for mass in mass_f:
            total_fuel += required_fuel(int(mass))

    return total_fuel


print(calculate_fuel("../input/modules_mass.txt"))
