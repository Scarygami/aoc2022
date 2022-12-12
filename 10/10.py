import os

currentdir = os.path.dirname(os.path.abspath(__file__))


def parse_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        commands = [line.split(" ") for line in lines]

    return commands


def run(commands):
    cycles = []
    x = 1

    cycles.append(x)
    cycles.append(x)

    for command in commands:
        if command[0] == "noop":
            cycles.append(x)

        if command[0] == "addx":
            cycles.append(x)
            x = x + int(command[1])
            cycles.append(x)

    return cycles


def part1(filename):
    commands = parse_input(filename)
    cycles = run(commands)
    strength = 0
    for cycle in range(20, 221, 40):
        strength = strength + cycle * cycles[cycle]

    return strength


def part2(filename):
    commands = parse_input(filename)
    cycles = run(commands)
    output = []
    for cycle in range(240):
        x = cycles[cycle + 1]
        if abs(x - cycle % 40) <= 1:
            output.append("#")
        else:
            output.append(".")

    lines = []
    for line in range(0, 201, 40):
        lines.append("".join(output[line : line + 40]))

    return "\n".join(lines)


assert part1(os.path.join(currentdir, "test_input.txt")) == 13140

print("Part 1: ", part1(os.path.join(currentdir, "input.txt")))

assert part2(os.path.join(currentdir, "test_input.txt")) == (
    "##..##..##..##..##..##..##..##..##..##..\n"
    + "###...###...###...###...###...###...###.\n"
    + "####....####....####....####....####....\n"
    + "#####.....#####.....#####.....#####.....\n"
    + "######......######......######......####\n"
    + "#######.......#######.......#######....."
)

print("Part 2:")
print(part2(os.path.join(currentdir, "input.txt")))
