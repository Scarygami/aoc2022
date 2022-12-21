import os
import re

currentdir = os.path.dirname(os.path.abspath(__file__))

DIRS = [(1, 1), (1, -1), (-1, 1), (-1, -1)]


def parse_sensor(line):
    matches = re.match(
        ".*x=(-?[0-9]+), y=(-?[0-9]+):.*x=(-?[0-9]+), y=(-?[0-9]+)", line
    )
    sensor = (int(matches.group(1)), int(matches.group(2)))
    beacon = (int(matches.group(3)), int(matches.group(4)))
    return (sensor, beacon)


def parse_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()

        sensors = []
        for line in lines:
            sensors.append(parse_sensor(line))

    return sensors


def manhattan(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)


def print_grid(grid):
    min_x = min(key[0] for key in grid.keys())
    max_x = max(key[0] for key in grid.keys())
    min_y = min(key[1] for key in grid.keys())
    max_y = max(key[1] for key in grid.keys())

    for y in range(min_y, max_y + 1):
        line = ""
        for x in range(min_x, max_x + 1):
            line = line + grid[(x, y)]
        print(y, line)


def locked_positions(filename, check_y):
    sensors = parse_input(filename)

    beacons = [beacon for _, beacon in sensors]

    ranges = []
    min_x = None
    max_x = None
    for (sx, sy), (bx, by) in sensors:
        distance = manhattan(sx, sy, bx, by)

        if manhattan(sx, sy, sx, check_y) > distance:
            continue

        dy = abs(sy - check_y)
        dx = distance - dy
        ranges.append((sx - dx, sx + dx))

        if min_x is None or sx - dx < min_x:
            min_x = sx - dx

        if max_x is None or sx + dx > max_x:
            max_x = sx + dx

    positions = 0
    for x in range(min_x, max_x + 1):
        if (x, check_y) in beacons:
            continue

        for (x1, x2) in ranges:
            if x >= x1 and x <= x2:
                positions = positions + 1
                break

    return positions


def frequency(filename, maximum=4000000):
    sensors = parse_input(filename)

    borders = []
    distances = []

    for (sx, sy), (bx, by) in sensors:
        distance = manhattan(sx, sy, bx, by)
        distances.append(((sx, sy), (bx, by), distance))

        for dx in range(0, distance + 2):
            dy = distance + 1 - dx

            for (ox, oy) in DIRS:
                x = sx + ox * dx
                y = sy + oy * dy
                if x >= 0 and x <= maximum and y >= 0 and y <= maximum:
                    borders.append((x, y))

    borders = set(borders)

    for (x, y) in borders:
        for (sx, sy), _, distance in distances:
            if manhattan(sx, sy, x, y) <= distance:
                break
        else:
            return x * 4000000 + y


assert locked_positions(os.path.join(currentdir, "test_input.txt"), 10) == 26

print("Part 1: ", locked_positions(os.path.join(currentdir, "input.txt"), 2000000))

assert frequency(os.path.join(currentdir, "test_input.txt"), 20) == 56000011

print("Part 2: ", frequency(os.path.join(currentdir, "input.txt")))
