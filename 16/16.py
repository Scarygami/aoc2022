import os
import re
from collections import defaultdict
from itertools import product

currentdir = os.path.dirname(os.path.abspath(__file__))


def parse_valve(line):

    matches = re.match("Valve ([A-Z][A-Z]) .* rate=([0-9]+); .* valves? (.*)", line)

    valve = matches.group(1)
    rate = int(matches.group(2))
    tunnels = matches.group(3).split(", ")

    return valve, rate, tunnels


def parse_input(filename):
    valves = {}
    with open(filename) as f:
        lines = f.read().splitlines()

        for line in lines:
            valve, rate, tunnels = parse_valve(line)
            valves[valve] = (rate, tunnels)

    return valves


def interesting_distances(valves):
    interesting_valves = []
    for valve in valves.keys():
        if valves[valve][0] > 0:
            interesting_valves.append(valve)

    distances = {}

    for valve1 in ["AA"] + interesting_valves:
        for valve2 in interesting_valves:
            if valve1 == valve2:
                continue

            best = defaultdict(lambda: None)

            frontier = [(valve1, 0)]
            while len(frontier) > 0:
                new_frontier = []
                for valve, steps in frontier:
                    if best[valve] is None or steps < best[valve]:
                        best[valve] = steps
                    else:
                        continue

                    if valve == valve2:
                        continue

                    for new_valve in valves[valve][1]:
                        new_frontier.append((new_valve, steps + 1))

                frontier = new_frontier

            distances[(valve1, valve2)] = best[valve2]
            distances[(valve2, valve1)] = best[valve2]

    return distances, interesting_valves


def best_pressure(valves, distances, interesting_valves, minutes):
    frontier = [("AA", 0, 0, 0, [])]
    best = 0

    while len(frontier) > 0:
        new_frontier = []
        for valve, time, pressure, total, opened in frontier:
            final = total + (minutes - time) * pressure
            if final > best:
                best = final

            for new_valve in interesting_valves:
                if new_valve == valve or new_valve in opened:
                    continue

                dt = distances[(valve, new_valve)] + 1
                if time + dt >= minutes - 1:
                    continue

                new_total = total + pressure * dt
                new_pressure = pressure + valves[new_valve][0]
                new_opened = opened + [valve]

                new_frontier.append(
                    (new_valve, time + dt, new_pressure, new_total, new_opened)
                )

        frontier = new_frontier

    return best


def part1(filename):
    valves = parse_input(filename)
    distances, interesting_valves = interesting_distances(valves)

    return best_pressure(valves, distances, interesting_valves, 30)


def part2(filename):
    valves = parse_input(filename)
    distances, interesting_valves = interesting_distances(valves)

    best = 0

    for pattern in product([True, False], repeat=len(interesting_valves)):
        valves1 = [x[1] for x in zip(pattern, interesting_valves) if x[0]]
        valves2 = [x[1] for x in zip(pattern, interesting_valves) if not x[0]]

        if len(valves1) == 0 or len(valves2) == 0:
            continue

        pressure = best_pressure(valves, distances, valves1, 26) + best_pressure(
            valves, distances, valves2, 26
        )
        if pressure > best:
            best = pressure

    return best


assert part1(os.path.join(currentdir, "test_input.txt")) == 1651

print("Part 1: ", part1(os.path.join(currentdir, "input.txt")))

assert part2(os.path.join(currentdir, "test_input.txt")) == 1707

print("Part 2: ", part2(os.path.join(currentdir, "input.txt")))
