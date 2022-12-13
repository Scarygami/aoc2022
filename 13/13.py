import os
import json
import functools

currentdir = os.path.dirname(os.path.abspath(__file__))


def parse_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()

        pairs = []
        for line in range(0, len(lines), 3):
            pairs.append((json.loads(lines[line]), json.loads(lines[line + 1])))

    return pairs


def check_pair(pair):
    packet1, packet2 = pair

    packet1 = json.loads(json.dumps(packet1))
    packet2 = json.loads(json.dumps(packet2))

    if type(packet1) == list:
        if type(packet2) != list:
            packet2 = [packet2]
    else:
        if type(packet2) == list:
            packet1 = [packet1]

    if type(packet1) == list:
        while len(packet1) > 0:
            if len(packet2) == 0:
                return False

            part1 = packet1.pop(0)
            part2 = packet2.pop(0)

            result = check_pair([part1, part2])
            if result is not None:
                return result

        if len(packet2) > 0:
            return True

        return None

    else:
        if packet1 < packet2:
            return True
        if packet1 > packet2:
            return False
        return None


def part1(filename):
    pairs = parse_input(filename)

    checksum = 0

    for p, pair in enumerate(pairs):
        if check_pair(pair) is True:
            checksum = checksum + p + 1

    return checksum


def compare(packet1, packet2):
    result = check_pair((packet1, packet2))

    if result is True:
        return -1

    if result is False:
        return 1

    return 0


def part2(filename):
    pairs = parse_input(filename)

    packets = []
    for pair in pairs:
        packets.append(pair[0])
        packets.append(pair[1])

    packets.append([[2]])
    packets.append([[6]])

    packets.sort(key=functools.cmp_to_key(compare))

    decoder_key = 1
    for p, packet in enumerate(packets):
        if compare(packet, [[2]]) == 0 or compare(packet, [[6]]) == 0:
            decoder_key = decoder_key * (p + 1)

    return decoder_key


assert part1(os.path.join(currentdir, "test_input.txt")) == 13

print("Part 1: ", part1(os.path.join(currentdir, "input.txt")))

assert part2(os.path.join(currentdir, "test_input.txt")) == 140

print("Part 2: ", part2(os.path.join(currentdir, "input.txt")))
