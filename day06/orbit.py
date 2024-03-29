"""
Orbit

Computes the total number of direct and indirect orbits of
objects.
"""
import pytest

test_cases = [
    (
        [
            ("COM", "B"),
            ("B", "C"),
            ("C", "D"),
            ("D", "E"),
            ("E", "F"),
            ("B", "G"),
            ("G", "H"),
            ("D", "I"),
            ("E", "J"),
            ("J", "K"),
            ("K", "L"),
        ],
        42,
    )
]


class SpaceObject:
    def __init__(self, name=None, orbit=None):
        self.name = name
        self.orbit_around = orbit

    def __repr__(self):
        return self.name


@pytest.mark.parametrize("orbits, result", test_cases)
def test_count_orbits(orbits, result):
    orbit_map = map_orbits(orbits)
    assert count_orbits(orbit_map) == result


def test_orbital_transfer():
    orbits = [
        ("COM", "B"),
        ("B", "C"),
        ("C", "D"),
        ("D", "E"),
        ("E", "F"),
        ("B", "G"),
        ("G", "H"),
        ("D", "I"),
        ("E", "J"),
        ("J", "K"),
        ("K", "L"),
        ("K", "YOU"),
        ("I", "SAN")
    ]
    orbit_map = map_orbits(orbits)
    assert 4 == orbital_transfers(orbit_map, "YOU", "SAN")


def parse_orbit_input(orbit_file):
    orbits = []
    with open(orbit_file, "r") as orbit_f:
        for line in orbit_f:
            line = line.strip()
            orbits.append(tuple(line.split(")")))

    return orbits


def debug_spaceobj(obj):
    print("name:", obj.name)
    print("orbitting:", obj.orbit_around)


def map_orbits(orbits):
    space_objects = {}
    for orbit_target, orbitting_object in orbits:
        if orbit_target not in space_objects:
            space_objects[orbit_target] = SpaceObject(orbit_target)
        if orbitting_object not in space_objects:
            space_objects[orbitting_object] = SpaceObject(
                orbitting_object, space_objects[orbit_target]
            )
        else:
            space_objects[orbitting_object].orbit_around = space_objects[orbit_target]

    return space_objects


def count_orbits(orbit_map):
    count = 0
    for obj in orbit_map.values():
        next_obj = obj.orbit_around
        while next_obj:
            next_obj = next_obj.orbit_around
            count += 1

    return count


def orbital_transfers(orbit_map, target, dest):
    for name in (target, dest):
        if name not in orbit_map:
            raise KeyError(f"Name not found in map: {name}")

    target_orb_dist = {}
    transfers = 0
    next_obj = orbit_map[target].orbit_around
    while next_obj:
        target_orb_dist[next_obj.name] = transfers
        transfers += 1
        next_obj = next_obj.orbit_around

    next_obj = orbit_map[dest].orbit_around
    transfers = 0
    while next_obj:
        if next_obj.name in target_orb_dist:
            return transfers + target_orb_dist[next_obj.name]
        transfers += 1
        next_obj = next_obj.orbit_around

    return None


if __name__ == "__main__":
    orbits = parse_orbit_input("./input")
    orbit_map = map_orbits(orbits)
    print("Orbit count:", count_orbits(orbit_map))
    print("Transfers for YOU to SAN:", orbital_transfers(orbit_map, "YOU", "SAN"))
