"""
Asteroid Monitor

Takes in a map of asteroids in space and identify the best asteroid location to monitor the most asteroids
"""
import math
import sys
import collections

def get_angle(origin, location):
    o_x, o_y = origin
    l_x, l_y = location

    y_diff = o_y - l_y
    x_diff = l_x - o_x

    angle = math.degrees(math.atan2(abs(y_diff), abs(x_diff)))

    if y_diff == 0 and x_diff == 0:
        angle = 0
    elif y_diff >= 0 and x_diff > 0:
        angle = 90 - angle
    elif y_diff < 0 and x_diff >= 0:
        angle = 90 + angle
    elif y_diff < 0 and x_diff < 0:
        angle = 270 - angle
    else:
        angle = 270 + angle

    return angle % 360

def get_asteroid_grid(asteroid_file):
    asteroid_grid = []
    with open(asteroid_file, 'r') as asteroid_f:
        for line in asteroid_f.readlines():
            row = []
            for c in line.strip():
                row.append(c)
            asteroid_grid.append(row)

    return asteroid_grid


def get_distance(origin, location):
    return math.hypot(location[0] - origin[0], location[1] - origin[1])

def survey_surrounding_asteroids(ast_grid, origin):
    result = []

    for row in range(len(ast_grid)):
        for col in range(len(ast_grid[0])):
            if ast_grid[row][col] == "#":
                location = (col, row)
                dist = get_distance(origin, location)
                angle = get_angle(origin, location)
                if dist != 0:
                    result.append((dist, angle, location))

    return result


def count_seen_asteroids(ast_grid, origin):
    ast_dist = survey_surrounding_asteroids(ast_grid, origin)
    ast_dist = sorted(ast_dist, key=lambda x:x[0])
    count = 0
    seen_angles = {}
    for dst, angle, pos in ast_dist:
        if angle not in seen_angles:
            count += 1
            seen_angles[angle] = True

    return count


def vaporise_asteroid_order(ast_grid, station_loc):
    ast_profile = survey_surrounding_asteroids(ast_grid, station_loc)
    ast_at_angles = collections.defaultdict(list)

    for dst, angle, pos in ast_profile:
        ast_at_angles[angle].append((dst, pos))

    unique_angles = []
    for angle, values in ast_at_angles.items():
        unique_angles.append(angle)
        ast_at_angles[angle].sort(key=lambda x: x[0])

    unique_angles.sort()

    destroy_order = []
    while len(destroy_order) != len(ast_profile):
        for angle in unique_angles:
            if ast_at_angles[angle]:
                _, pos = ast_at_angles[angle].pop(0)
                destroy_order.append(pos)

    return destroy_order

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(f"To use: {sys.argv[0]} <input file>")
    input_file = sys.argv[1]
    ast_grid = get_asteroid_grid(input_file)

    max = 0
    max_pos = None
    for row in range(len(ast_grid)):
        for col in range(len(ast_grid[0])):
            if ast_grid[row][col] == "#":
                origin = (col, row)
                asteroids = count_seen_asteroids(ast_grid, origin)
                if asteroids > max:
                    max = asteroids
                    max_pos = origin

    print(max, max_pos)

    destroy_order = vaporise_asteroid_order(ast_grid, max_pos)
