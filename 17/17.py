import os
from collections import defaultdict

currentdir = os.path.dirname(os.path.abspath(__file__))

ROCKS = [
    [[1, 1, 1, 1]],
    [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [0, 0, 1], [0, 0, 1]],
    [[1], [1], [1], [1]],
    [[1, 1], [1, 1]],
]


def parse_input(filename):
    with open(filename) as f:
        line = f.read().splitlines()[0]

    return line


def top(chamber):
    return max(y for (y, x) in chamber.keys() if chamber[(y, x)] > 0)


def column_top(chamber, column):
    return max(y for (y, x) in chamber.keys() if chamber[(y, x)] > 0 and x == column)


def collide(chamber, rock, rock_x, rock_y):
    if rock_x < 0:
        return True

    if rock_x + len(ROCKS[rock][0]) > 7:
        return True

    for y in range(len(ROCKS[rock])):
        for x in range(len(ROCKS[rock][0])):
            if chamber[(rock_y + y, rock_x + x)] + ROCKS[rock][y][x] > 1:
                return True

    return False


def stop_rock(chamber, rock, rock_x, rock_y):
    for y in range(len(ROCKS[rock])):
        for x in range(len(ROCKS[rock][0])):
            chamber[(rock_y + y, rock_x + x)] += ROCKS[rock][y][x]

    return chamber


def draw(chamber):
    for y in range(top(chamber), 0, -1):
        line = "|"
        for x in range(7):
            if chamber[(y, x)] == 1:
                line = line + "@"
            else:
                line = line + "."
        line = line + "|"
        print(line)

    print("|-------|")
    print("")


def simulate(filename, max_rocks=2022):
    jets = parse_input(filename)
    chamber = defaultdict(lambda: 0)

    for x in range(7):
        chamber[(0, x)] = 1

    stopped_rocks = 0
    jet = 0
    rock_x = 2
    rock_y = top(chamber) + 4
    rock = 0
    cycle = False
    total_loop_height = 0
    states = {}

    while stopped_rocks < max_rocks:
        push = 1 if jets[jet] == ">" else -1
        jet = (jet + 1) % len(jets)
        if collide(chamber, rock, rock_x + push, rock_y):
            push = 0

        rock_x = rock_x + push

        if collide(chamber, rock, rock_x, rock_y - 1):
            chamber = stop_rock(chamber, rock, rock_x, rock_y)
            stopped_rocks = stopped_rocks + 1
            rock = (rock + 1) % len(ROCKS)
            rock_x = 2
            rock_y = top(chamber) + 4

            if cycle is False:
                columns = [column_top(chamber, column) for column in range(7)]
                reference = min(columns)
                columns = [column - reference for column in columns]
                this_state = (tuple(columns), jet, rock)

                if this_state in states:
                    cycle = True
                    cycle_rocks = stopped_rocks - states[this_state][0]
                    cycle_height = top(chamber) - states[this_state][1]
                    remaining_rocks = max_rocks - stopped_rocks
                    remaining_cycles = remaining_rocks // cycle_rocks
                    total_loop_height = remaining_cycles * cycle_height
                    total_loop_rocks = remaining_cycles * cycle_rocks
                    max_rocks = max_rocks - total_loop_rocks
                else:
                    states[this_state] = (stopped_rocks, top(chamber))
        else:
            rock_y = rock_y - 1

    return top(chamber) + total_loop_height


assert simulate(os.path.join(currentdir, "test_input.txt")) == 3068

print("Part 1: ", simulate(os.path.join(currentdir, "input.txt")))

assert (
    simulate(os.path.join(currentdir, "test_input.txt"), 1000000000000) == 1514285714288
)

print("Part 2: ", simulate(os.path.join(currentdir, "input.txt"), 1000000000000))
