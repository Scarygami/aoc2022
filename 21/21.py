import os
from operator import add, mul, sub, truediv

currentdir = os.path.dirname(os.path.abspath(__file__))

OPS = {"+": add, "*": mul, "/": truediv, "-": sub}


def parse_line(line):
    name, tmp = line.split(": ")
    tmp = tmp.split(" ")
    if len(tmp) == 1:
        yell = int(tmp[0])
    else:
        yell = (tmp[0], OPS[tmp[1]], tmp[2])

    return (name, yell)


def parse_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        monkeys = {}
        for line in lines:
            name, yell = parse_line(line)
            monkeys[name] = yell

        return monkeys


def yell(monkeys, monkey="root"):
    data = monkeys[monkey]
    if type(data) is tuple:
        monkey1, op, monkey2 = data
        value1 = yell(monkeys, monkey1)
        value2 = yell(monkeys, monkey2)
        return op(value1, value2)
    else:
        return data


def part1(filename):
    monkeys = parse_input(filename)
    return int(yell(monkeys))


def part2(filename):
    monkeys = parse_input(filename)
    monkey1, _, monkey2 = monkeys["root"]

    monkeys["humn"] = 1
    value1 = (yell(monkeys, monkey1), yell(monkeys, monkey2))

    monkeys["humn"] = 100
    value2 = (yell(monkeys, monkey1), yell(monkeys, monkey2))

    if value1[0] == value2[0]:
        affected = 1
        goal = value1[0]
        monkey = monkey2
    else:
        affected = 0
        goal = value1[1]
        monkey = monkey1

    if value1[affected] > value2[affected]:
        influence = -1
    else:
        influence = 1

    exponent = 11
    if value1[affected] < goal:
        direction = -1
    else:
        direction = 1

    humn = 1
    monkeys["humn"] = humn
    value = yell(monkeys, monkey)

    while value != goal:
        if (value < goal and direction < 0) or (value > goal and direction > 0):
            # surpassed the goal
            direction = -direction
            exponent = exponent - 1

        humn = humn + influence * direction * 10**exponent
        monkeys["humn"] = humn
        value = yell(monkeys, monkey)

    return humn


assert part1(os.path.join(currentdir, "test_input.txt")) == 152

print("Part 1: ", part1(os.path.join(currentdir, "input.txt")))

assert part2(os.path.join(currentdir, "test_input.txt")) == 301

print("Part 2: ", part2(os.path.join(currentdir, "input.txt")))
