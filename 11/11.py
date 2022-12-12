import os

currentdir = os.path.dirname(os.path.abspath(__file__))


class Monkey(object):
    def __init__(self, items, operation, test, target_true, target_false):
        self.items = items
        self.operation = operation
        self.test = test
        self.target_true = target_true
        self.target_false = target_false
        self.inspections = 0

    def turn(self, monkeys, divisor=None):
        for item in self.items:
            worry = self.inspect(item)
            if divisor is not None:
                worry = worry % divisor
            else:
                worry = worry // 3
            if worry % self.test == 0:
                target = self.target_true
            else:
                target = self.target_false
            monkeys[target].catch(worry)

        self.items = []

    def inspect(self, item):
        self.inspections = self.inspections + 1
        op, op2 = self.operation
        if op2 == "old":
            op2 = item
        else:
            op2 = int(op2)

        if op == "+":
            return item + op2

        if op == "*":
            return item * op2

    def catch(self, item):
        self.items.append(item)


def parse_monkey(lines):
    items = lines[0][18:].split(",")
    items = [int(item) for item in items]

    operation = tuple(lines[1][23:].split(" "))

    test = int(lines[2][21:])
    target_true = int(lines[3][29:])
    target_false = int(lines[4][30:])

    return Monkey(items, operation, test, target_true, target_false)


def parse_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        monkeys = []

        for i in range(0, len(lines), 7):
            monkeys.append(parse_monkey(lines[i + 1 : i + 6]))

    return monkeys


def part1(filename):
    monkeys = parse_input(filename)

    for _ in range(20):
        for monkey in monkeys:
            monkey.turn(monkeys)

    inspections = sorted([monkey.inspections for monkey in monkeys])

    return inspections[-1] * inspections[-2]


def part2(filename):
    monkeys = parse_input(filename)

    divisor = 1
    for monkey in monkeys:
        divisor = divisor * monkey.test

    for _ in range(10000):
        for monkey in monkeys:
            monkey.turn(monkeys, divisor)

    inspections = sorted([monkey.inspections for monkey in monkeys])

    return inspections[-1] * inspections[-2]


assert part1(os.path.join(currentdir, "test_input.txt")) == 10605

print("Part 1: ", part1(os.path.join(currentdir, "input.txt")))

assert part2(os.path.join(currentdir, "test_input.txt")) == 2713310158

print("Part 2: ", part2(os.path.join(currentdir, "input.txt")))
