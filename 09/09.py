import os

currentdir = os.path.dirname(os.path.abspath(__file__))

MOVES = {"L": (1, 0), "R": (-1, 0), "U": (0, -1), "D": (0, 1)}


def parse_line(line):
    direction, steps = line.split(" ")
    return (MOVES[direction], int(steps))


def parse_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        moves = [parse_line(line) for line in lines]

    return moves


def is_touching(head, tail):
    hx, hy = head
    tx, ty = tail
    if abs(hx - tx) <= 1 and abs(hy - ty) <= 1:
        return True
    return False


def adjust(head, tail):
    if is_touching(head, tail) is True:
        return tail

    tx, ty = tail
    hx, hy = head
    if tx == hx:
        if ty < hy:
            ty = ty + 1
        else:
            ty = ty - 1
    elif ty == hy:
        if tx < hx:
            tx = tx + 1
        else:
            tx = tx - 1
    else:
        if ty < hy:
            ty = ty + 1
        else:
            ty = ty - 1
        if tx < hx:
            tx = tx + 1
        else:
            tx = tx - 1

    return (tx, ty)


def perform_step(knots, direction):
    dx, dy = direction
    hx, hy = knots[0]
    knots[0] = (hx + dx, hy + dy)

    for i in range(len(knots) - 1):
        knots[i + 1] = adjust(knots[i], knots[i + 1])


def tail_visits(filename, count=2):
    moves = parse_input(filename)
    visited = {}
    knots = []
    for _ in range(count):
        knots.append((0, 0))

    visited[(0, 0)] = True
    for move in moves:
        direction, steps = move
        for _ in range(steps):
            perform_step(knots, direction)
            visited[knots[-1]] = True

    return len(visited)


assert tail_visits(os.path.join(currentdir, "test_input1.txt")) == 13

print("Part 1: ", tail_visits(os.path.join(currentdir, "input.txt")))

assert tail_visits(os.path.join(currentdir, "test_input1.txt"), 10) == 1
assert tail_visits(os.path.join(currentdir, "test_input2.txt"), 10) == 36

print("Part 2: ", tail_visits(os.path.join(currentdir, "input.txt"), 10))
