import os
from collections import deque

currentdir = os.path.dirname(os.path.abspath(__file__))


def parse_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        values = [int(line) for line in lines]
        return values


def mix(values, repeats=1):
    values = list(enumerate(values))
    queue = deque(values)
    for _ in range(repeats):
        for value in values:
            pos = queue.index(value)
            queue.rotate(-pos)
            queue.popleft()
            queue.rotate(-value[1])
            queue.appendleft(value)

    return queue


def grove_coordinates(queue):
    for value in queue:
        if value[1] == 0:
            zero = value
            break
    pos = queue.index(zero)
    length = len(queue)
    return (
        queue[(pos + 1000) % length][1],
        queue[(pos + 2000) % length][1],
        queue[(pos + 3000) % length][1],
    )


def part1(filename):
    values = parse_input(filename)
    result = grove_coordinates(mix(values))
    return sum(result)


def part2(filename):
    values = parse_input(filename)
    values = [811589153 * value for value in values]
    result = grove_coordinates(mix(values, 10))
    return sum(result)


assert part1(os.path.join(currentdir, "test_input.txt")) == 3

print("Part 1: ", part1(os.path.join(currentdir, "input.txt")))

assert part2(os.path.join(currentdir, "test_input.txt")) == 1623178306

print("Part 1: ", part2(os.path.join(currentdir, "input.txt")))
