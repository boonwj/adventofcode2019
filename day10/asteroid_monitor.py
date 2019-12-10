"""
Asteroid Monitor

Takes in a map of asteroids in space and identify the best asteroid location to monitor the most asteroids
"""
import math
import sys

def get_angle(origin, location):
    o_x, o_y = origin
    l_x, l_y = location

    y_diff = l_y - o_y
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

    return angle

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

def count_seen_asteroids(ast_grid, origin):
    ast_dist = []

    for row in range(len(ast_grid)):
        for col in range(len(ast_grid[0])):
            if ast_grid[row][col] == "#":
                location = (col, row)
                dist = get_distance(origin, location)
                angle = get_angle(origin, location)
                ast_dist.append((dist, angle, location))
    ast_dist = sorted(ast_dist, key=lambda x:x[0])

    count = 0
    seen_angles = {}
    for dst, angle, pos in ast_dist:
        if dst != 0 and angle not in seen_angles:
            count += 1
            seen_angles[angle] = True

    return count



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
