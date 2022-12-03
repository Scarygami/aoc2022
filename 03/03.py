import os
import re

currentdir = os.path.dirname(os.path.abspath(__file__))

TYPES = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def score(type):
    return TYPES.index(type) + 1


def parse_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


def priority(rucksack):
    length = len(rucksack)
    compartment1 = rucksack[0 : length // 2]
    compartment2 = rucksack[length // 2 : length]
    regex = f"[{compartment1}]"
    matches = re.search(regex, compartment2)
    return score(matches.group(0))


def priorities(filename):
    rucksacks = parse_input(filename)
    return sum(priority(rucksack) for rucksack in rucksacks)


def group_priority(group):
    rucksack1, rucksack2, rucksack3 = group
    regex = f"[{rucksack1}]"
    matches = re.findall(regex, rucksack2)
    regex = f"[{''.join(matches)}]"
    matches = re.search(regex, rucksack3)
    return score(matches.group(0))


def group_priorities(filename):
    rucksacks = parse_input(filename)
    groups = [rucksacks[i : i + 3] for i in range(0, len(rucksacks), 3)]
    return sum(group_priority(group) for group in groups)


assert priority("vJrwpWtwJgWrhcsFMMfFFhFp") == 16
assert priority("jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL") == 38
assert priorities(os.path.join(currentdir, "test_input.txt")) == 157

print("Part 1: ", priorities(os.path.join(currentdir, "input.txt")))

assert group_priorities(os.path.join(currentdir, "test_input.txt")) == 70

print("Part 2: ", group_priorities(os.path.join(currentdir, "input.txt")))
