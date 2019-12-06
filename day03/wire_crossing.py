"""
Wire crossing takes in 2 wires and determine if they cross
and return the manhattan distance of the closest intersection.
"""
import pytest

test_cases = [
    (["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"], 159),
    (
        [
            "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
            "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
        ],
        135,
    ),
]


@pytest.mark.parametrize("wires, dist", test_cases)
def test_min_dist(wires, dist):
    assert closest_distance(wires) == dist


def get_wires(wire_file):
    with open(wire_file, "r") as wire_f:
        wires = wire_f.readlines()
        wires = [w.strip() for w in wires]

    return wires


def map_wire_path(wire_movement):
    wire_map = {}
    total_steps = 0
    start_pt = [0, 0]
    for movement in wire_movement.split(","):
        direction, steps = movement[0], int(movement[1:])

        if direction not in ("UDLR"):
            raise ValueError(f"Invalid direction: {direction}")

        for i in range(steps):
            if direction == "U":
                start_pt[1] += 1
            elif direction == "D":
                start_pt[1] -= 1
            elif direction == "L":
                start_pt[0] -= 1
            elif direction == "R":
                start_pt[0] += 1
            total_steps += 1
            wire_map[(start_pt[0], start_pt[1])] = total_steps

    return wire_map


def get_intersect_pts(wire_maps):
    intersect_pts = []

    for coord in wire_maps[0]:
        if coord != (0, 0) and coord in wire_maps[1]:
            intersect_pts.append(coord)

    return intersect_pts


def closest_distance(wires, type="manhattan"):
    wire_maps = []
    for wire in wires:
        wire_maps.append(map_wire_path(wire))

    intersect_pts = get_intersect_pts(wire_maps)

    if type == "manhattan":
        return min([abs(x) + abs(y) for (x, y) in intersect_pts])
    elif type == "combined_steps":
        return min(
            [wire_maps[0][coord] + wire_maps[1][coord] for coord in intersect_pts]
        )


wires = get_wires("./input")
print("Manhattan Distance:", closest_distance(wires))
print("Combined Steps:", closest_distance(wires, "combined_steps"))
