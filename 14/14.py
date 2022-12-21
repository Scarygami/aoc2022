import os
from collections import defaultdict

currentdir = os.path.dirname(os.path.abspath(__file__))

DIRS = [(0, 1), (-1, 1), (1, 1)]


def update_grid_line(grid, coord1, coord2):
    x1, y1 = coord1.split(",")
    x2, y2 = coord2.split(",")
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)

    if x1 > x2:
        x1, x2 = x2, x1

    if y1 > y2:
        y1, y2 = y2, y1

    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            grid[(x, y)] = "#"

    return grid


def update_grid(grid, line):
    coords = line.split(" -> ")
    for c in range(len(coords) - 1):
        grid = update_grid_line(grid, coords[c], coords[c + 1])

    return grid


def print_grid(grid):
    min_x = min(key[0] for key in grid.keys())
    max_x = max(key[0] for key in grid.keys())
    max_y = max(key[1] for key in grid.keys())

    for y in range(0, max_y + 1):
        line = ""
        for x in range(min_x, max_x + 1):
            line = line + grid[(x, y)]
        print(line)


def parse_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        grid = defaultdict(lambda: ".")

        for line in lines:
            grid = update_grid(grid, line)

    return grid


def simulate(filename, part2=False):
    grid = parse_input(filename)
    sand = 0
    max_y = max(key[1] for key in grid.keys())
    x, y = 500, 0
    grid[(x, y)] = "*"
    while True:
        for dx, dy in DIRS:
            nx = x + dx
            ny = y + dy
            if grid[(nx, ny)] == ".":
                grid[(x, y)] = "."
                grid[(nx, ny)] = "+"
                x, y = nx, ny
                break
        else:
            grid[(x, y)] = "o"
            sand = sand + 1
            if part2 is True and (x, y) == (500, 0):
                break
            x, y = 500, 0
            continue

        if part2 is True:
            if y == max_y + 1:
                grid[(x, y)] = "o"
                sand = sand + 1
                x, y = 500, 0
                continue

        else:
            if y > max_y:
                break

    return sand


assert simulate(os.path.join(currentdir, "test_input.txt")) == 24

print("Part 1: ", simulate(os.path.join(currentdir, "input.txt")))

assert simulate(os.path.join(currentdir, "test_input.txt"), True) == 93

print("Part 2: ", simulate(os.path.join(currentdir, "input.txt"), True))
