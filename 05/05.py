import os
import re

currentdir = os.path.dirname(os.path.abspath(__file__))


def parse_stacks(lines):
    count_line = lines[-1].strip()
    numbers = count_line.split(" ")
    count = int(numbers[-1])
    stacks = []
    for _ in range(count):
        stacks.append([])

    for row in range(len(lines) - 2, -1, -1):
        for col in range(count):
            if col*4 + 1 < len(lines[row]):
                crate = lines[row][col*4 + 1]
                if crate != " ":
                    stacks[col].append(crate)

    return stacks


def parse_command(line):
    matches = re.match("move ([0-9]+) from ([0-9]+) to ([0-9]+)", line)
    return (
        int(matches.group(1)),
        int(matches.group(2)) - 1,
        int(matches.group(3)) - 1
    )


def parse_commands(lines):
    return [parse_command(line) for line in lines]


def parse_input(filename):
    stack_lines = []
    command_lines = []

    with open(filename) as f:
        lines = f.read().splitlines()

        parsing_stack = True
        for line in lines:
            if line == "":
                parsing_stack = False
                continue
            if parsing_stack is True:
                stack_lines.append(line)
            else:
                command_lines.append(line)

    stacks = parse_stacks(stack_lines)
    commands = parse_commands(command_lines)

    return stacks, commands


def top_crates(stacks):
    return [stack[-1] for stack in stacks]


def perform_command(stacks, command, cm9001=False):
    count = command[0]
    from_stack = command[1]
    to_stack = command[2]
    if cm9001 is True:
        crates = []
        for _ in range(count):
            crate = stacks[from_stack].pop()
            crates.insert(0, crate)
        stacks[to_stack].extend(crates)
    else:
        for _ in range(count):
            crate = stacks[from_stack].pop()
            stacks[to_stack].append(crate)
    return stacks


def perform_commands(stacks, commands, cm9001=False):
    for command in commands:
        stacks = perform_command(stacks, command, cm9001)
    return stacks


def determine_top_crates(filename, cm9001=False):
    stacks, commands = parse_input(filename)
    stacks = perform_commands(stacks, commands, cm9001)
    return "".join(top_crates(stacks))


assert determine_top_crates(os.path.join(currentdir, "test_input.txt")) == "CMZ"

print("Part 1: ", determine_top_crates(os.path.join(currentdir, "input.txt")))

assert determine_top_crates(os.path.join(currentdir, "test_input.txt"), True) == "MCD"

print("Part 2: ", determine_top_crates(os.path.join(currentdir, "input.txt"), True))
