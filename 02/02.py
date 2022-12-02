import os

currentdir = os.path.dirname(os.path.abspath(__file__))

scores1 = {
    ("A", "X"): 4,
    ("A", "Y"): 8,
    ("A", "Z"): 3,
    ("B", "X"): 1,
    ("B", "Y"): 5,
    ("B", "Z"): 9,
    ("C", "X"): 7,
    ("C", "Y"): 2,
    ("C", "Z"): 6,
}


scores2 = {
    ("A", "X"): 3,
    ("A", "Y"): 4,
    ("A", "Z"): 8,
    ("B", "X"): 1,
    ("B", "Y"): 5,
    ("B", "Z"): 9,
    ("C", "X"): 2,
    ("C", "Y"): 6,
    ("C", "Z"): 7,
}


def parse_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        moves = [tuple(line.split(" ")) for line in lines]

    return moves


def play(filename, scores):
    moves = parse_input(filename)

    score = sum(scores[move] for move in moves)

    return score


assert play(os.path.join(currentdir, "test_input.txt"), scores1) == 15

print("Part 1: ", play(os.path.join(currentdir, "input.txt"), scores1))

assert play(os.path.join(currentdir, "test_input.txt"), scores2) == 12

print("Part 2: ", play(os.path.join(currentdir, "input.txt"), scores2))
