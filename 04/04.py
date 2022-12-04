import os
import re

currentdir = os.path.dirname(os.path.abspath(__file__))


def parse_line(line):
    values = re.split("[-,]", line)
    return [int(value) for value in values]


def parse_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        pairs = [parse_line(line) for line in lines]
        return pairs


def full_overlap(pair):
    a1, b1, a2, b2 = pair
    if a1 <= a2 and b1 >= b2:
        return True

    if a2 <= a1 and b2 >= b1:
        return True

    return False


def count_full_overlaps(filename):
    pairs = parse_input(filename)
    full_overlaps = [pair for pair in pairs if full_overlap(pair) is True]
    return len(full_overlaps)


def overlap(pair):
    a1, b1, a2, b2 = pair
    if a1 >= a2 and a1 <= b2:
        return True

    if b1 >= a2 and b1 <= b2:
        return True

    if a2 >= a1 and a2 <= b1:
        return True

    if b2 >= a1 and b2 <= b1:
        return True

    return False


def count_overlaps(filename):
    pairs = parse_input(filename)
    overlaps = [pair for pair in pairs if overlap(pair) is True]
    return len(overlaps)


assert count_full_overlaps(os.path.join(currentdir, "test_input.txt")) == 2

print("Part 1: ", count_full_overlaps(os.path.join(currentdir, "input.txt")))

assert count_overlaps(os.path.join(currentdir, "test_input.txt")) == 4

print("Part 2: ", count_overlaps(os.path.join(currentdir, "input.txt")))
