import os
import numpy as np

currentdir = os.path.dirname(os.path.abspath(__file__))


def parse_line(line):
    return [int(n) for n in line]


def parse_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        trees = np.array([parse_line(line) for line in lines])

    return trees


def part1(filename):
    trees = parse_input(filename)
    w, h = trees.shape
    visible = 0
    for x in range(w):
        for y in range(h):
            if x == 0 or x == w - 1 or y == 0 or y == w - 1:
                visible = visible + 1
                continue

            tree = trees[x, y]
            if (trees[x, 0:y] >= tree).sum() == 0:
                visible = visible + 1
                continue

            if (trees[x, y + 1 :] >= tree).sum() == 0:
                visible = visible + 1
                continue

            if (trees[0:x, y] >= tree).sum() == 0:
                visible = visible + 1
                continue

            if (trees[x + 1 :, y] >= tree).sum() == 0:
                visible = visible + 1
                continue

    return visible


def partial_score(tree, neighbours):
    score = 0
    for neighbour in neighbours:
        score = score + 1
        if neighbour >= tree:
            break
    return score


def part2(filename):
    trees = parse_input(filename)
    w, h = trees.shape
    max_score = 1
    for x in range(w):
        for y in range(h):

            if x == 0 or x == w - 1 or y == 0 or y == w - 1:
                continue

            tree = trees[x, y]
            score = partial_score(tree, trees[x, y - 1 :: -1])
            score = score * partial_score(tree, trees[x, y + 1 :])
            score = score * partial_score(tree, trees[x - 1 :: -1, y])
            score = score * partial_score(tree, trees[x + 1 :, y])

            if score > max_score:
                max_score = score

    return max_score


assert part1(os.path.join(currentdir, "test_input.txt")) == 21

print("Part 1: ", part1(os.path.join(currentdir, "input.txt")))

assert part2(os.path.join(currentdir, "test_input.txt")) == 8

print("Part 2: ", part2(os.path.join(currentdir, "input.txt")))
