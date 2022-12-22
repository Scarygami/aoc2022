import os
from collections import defaultdict
from itertools import permutations

currentdir = os.path.dirname(os.path.abspath(__file__))


def parse_input(filename):
    cubes = []
    with open(filename) as f:
        lines = f.read().splitlines()
        for line in lines:
            cubes.append(tuple([int(c) for c in line.split(",")]))

    return cubes


def total_surfaces(filename):
    cubes = parse_input(filename)
    surfaces = defaultdict(lambda: 6)

    for c, cube1 in enumerate(cubes):
        for cube2 in cubes[c + 1 :]:
            x1, y1, z1 = cube1
            x2, y2, z2 = cube2
            if abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2) == 1:
                surfaces[cube1] -= 1
                surfaces[cube2] -= 1

    return sum(surfaces[cube] for cube in cubes)


def total_exposed_surfaces(filename):
    cubes = parse_input(filename)

    max_x = max(cube[0] for cube in cubes)
    max_y = max(cube[1] for cube in cubes)
    max_z = max(cube[2] for cube in cubes)

    min_x = min(cube[0] for cube in cubes)
    min_y = min(cube[1] for cube in cubes)
    min_z = min(cube[2] for cube in cubes)

    steam = [(0, 0, 0)]
    frontier = [(0, 0, 0)]
    directions = set(list(permutations([-1, 0, 0])) + list(permutations([1, 0, 0])))

    while len(frontier) > 0:
        new_frontier = []
        for x, y, z in frontier:
            for dx, dy, dz in directions:
                new_steam = (x + dx, y + dy, z + dz)
                if new_steam in steam:
                    continue
                if new_steam in cubes:
                    continue
                if new_steam in new_frontier:
                    continue
                if new_steam[0] > max_x + 1 or new_steam[0] < 0:
                    continue
                if new_steam[1] > max_y + 1 or new_steam[1] < 0:
                    continue
                if new_steam[2] > max_z + 1 or new_steam[2] < 0:
                    continue
                steam.append(new_steam)
                new_frontier.append(new_steam)

        frontier = new_frontier

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            for z in range(min_z, max_z + 1):
                cube = (x, y, z)
                if cube not in cubes and cube not in steam:
                    cubes.append(cube)

    surfaces = defaultdict(lambda: 6)

    for c, cube1 in enumerate(cubes):
        for cube2 in cubes[c + 1 :]:
            x1, y1, z1 = cube1
            x2, y2, z2 = cube2
            if abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2) == 1:
                surfaces[cube1] -= 1
                surfaces[cube2] -= 1

    return sum(surfaces[cube] for cube in cubes)


assert total_surfaces(os.path.join(currentdir, "test_input1.txt")) == 10
assert total_surfaces(os.path.join(currentdir, "test_input2.txt")) == 64

print("Part 1: ", total_surfaces(os.path.join(currentdir, "input.txt")))

assert total_exposed_surfaces(os.path.join(currentdir, "test_input2.txt")) == 58

print("Part 2: ", total_exposed_surfaces(os.path.join(currentdir, "input.txt")))
