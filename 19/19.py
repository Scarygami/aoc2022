import os
import re
from operator import add, sub

currentdir = os.path.dirname(os.path.abspath(__file__))


def parse_line(line):
    matches = re.match(
        ".* ([0-9]+):.* ([0-9]+) .* ([0-9]+) .* ([0-9]+) "
        + ".* ([0-9]+) .* ([0-9]+) .* ([0-9]+) .*",
        line,
    )

    return (
        int(matches.group(1)),
        (int(matches.group(2)), 0, 0, 0),
        (int(matches.group(3)), 0, 0, 0),
        (int(matches.group(4)), int(matches.group(5)), 0, 0),
        (int(matches.group(6)), 0, int(matches.group(7)), 0),
    )


def parse_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()

        blueprints = [parse_line(line) for line in lines]

    return blueprints


def can_afford(resources, costs):
    for i in range(3):
        if resources[i] < costs[i]:
            return False

    return True


def simulate(robots, resources, costs, time, ignored_robots=[], best=0):
    if time == 0:
        return resources[3]

    best_geodes = best

    # Maximum geodes we could get
    # if building a geode-robot in each of the future minutes
    max_geodes = resources[3] + robots[3] * time + (time * (time + 1) / 2)
    if max_geodes < best_geodes:
        return 0

    tmp_resources = list(map(add, resources, robots))

    possible_robots = ignored_robots.copy()
    for robot in range(3, -1, -1):
        # In theory building a geode-robot should be better than building others
        # Therefore trying this path first

        if robot in possible_robots:
            # didn't build this one previously when I had the chance
            continue

        if robot < 3:
            if resources[robot] + time * robots[robot] >= time * max(
                cost[robot] for cost in costs
            ):
                # Producing more resources than we would ever need
                continue

        robot_cost = costs[robot]

        if can_afford(resources, robot_cost):
            possible_robots.append(robot)
            new_resources = list(map(sub, tmp_resources, robot_cost))
            new_robots = robots.copy()
            new_robots[robot] = new_robots[robot] + 1
            geodes = simulate(
                new_robots, new_resources, costs, time - 1, [], best_geodes
            )
            if geodes > best_geodes:
                best_geodes = geodes

    geodes = simulate(
        robots, tmp_resources, costs, time - 1, possible_robots, best_geodes
    )
    if geodes > best_geodes:
        best_geodes = geodes

    return best_geodes


def max_geodes(costs, time):
    robots = [1, 0, 0, 0]
    resources = [0, 0, 0, 0]
    return simulate(robots, resources, costs, time)


def quality_level(blueprint):
    id, ore, clay, obsidian, geode = blueprint
    costs = [ore, clay, obsidian, geode]
    geodes = max_geodes(costs, 24)
    return id * geodes


def part1(filename):
    blueprints = parse_input(filename)
    return sum(quality_level(bp) for bp in blueprints)


def part2(filename):
    blueprints = parse_input(filename)
    if len(blueprints) > 3:
        blueprints = blueprints[:3]

    geodes = 1
    for bp in blueprints:
        _, ore, clay, obsidian, geode = bp
        costs = [ore, clay, obsidian, geode]
        geodes = geodes * max_geodes(costs, 32)

    return geodes


assert part1(os.path.join(currentdir, "test_input.txt")) == 33

print("Part 1: ", part1(os.path.join(currentdir, "input.txt")))

assert part2(os.path.join(currentdir, "test_input.txt")) == 56 * 62

print("Part 2: ", part2(os.path.join(currentdir, "input.txt")))
