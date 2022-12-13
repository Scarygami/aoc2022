import os
from collections import defaultdict

currentdir = os.path.dirname(os.path.abspath(__file__))

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def parse_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()

        map = [list(line) for line in lines]

        for y in range(len(map)):
            for x in range(len(map[y])):
                if map[y][x] == "S":
                    start = (x, y)
                    map[y][x] = "a"
                if map[y][x] == "E":
                    end = (x, y)
                    map[y][x] = "z"

        map = [[ord(c) - 97 for c in line] for line in map]

    return map, start, end


def shortest_path(map, start, end):
    visited = defaultdict(lambda: 1000000)
    frontier = [(start, 0)]
    visited[start] = 0
    max_y = len(map)
    max_x = len(map[0])

    while len(frontier) > 0:
        new_frontier = []
        for ((x, y), steps) in frontier:

            for (dx, dy) in DIRECTIONS:
                nx = x + dx
                ny = y + dy
                nsteps = steps + 1
                if nx < 0 or nx >= max_x or ny < 0 or ny >= max_y:
                    continue

                if map[ny][nx] - map[y][x] > 1:
                    continue

                if visited[(nx, ny)] <= nsteps:
                    continue

                visited[(nx, ny)] = nsteps
                new_frontier.append(((nx, ny), nsteps))

        frontier = new_frontier

    return visited[end]


def part1(filename):
    map, start, end = parse_input(filename)

    return shortest_path(map, start, end)


def part2(filename):
    map, _, end = parse_input(filename)

    shortest = 1000000
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == 0:
                path = shortest_path(map, (x, y), end)
                if path < shortest:
                    shortest = path

    return shortest


assert part1(os.path.join(currentdir, "test_input.txt")) == 31

print("Part 1: ", part1(os.path.join(currentdir, "input.txt")))

assert part2(os.path.join(currentdir, "test_input.txt")) == 29

print("Part 2: ", part2(os.path.join(currentdir, "input.txt")))
