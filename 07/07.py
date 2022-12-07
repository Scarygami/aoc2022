import os

currentdir = os.path.dirname(os.path.abspath(__file__))


class Node(object):
    def __init__(self, name, is_folder=True, size=None):
        self.name = name
        self.is_folder = is_folder
        self.size = size
        self.children = []
        self.parent = None

    def add(self, child):
        self.children.append(child)
        child.parent = self

    def find(self, name):
        for child in self.children:
            if child.name == name:
                return child

        return None

    @property
    def total_size(self):
        if self.is_folder is False:
            return self.size

        return sum(child.total_size for child in self.children)

    @property
    def sub_folders(self):
        return [child for child in self.children if child.is_folder is True]


def handle_input(root, current, line):
    if line[0] == "$":
        if line == "$ ls":
            return current

        if line == "$ cd ..":
            return current.parent

        if line == "$ cd /":
            return root

        name = line[5:]
        return current.find(name)

    size, name = line.split(" ")
    if size == "dir":
        child = Node(name)
    else:
        child = Node(name, False, int(size))

    current.add(child)
    return current


def parse_input(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        root = Node("/")
        current = root

        for line in lines:
            current = handle_input(root, current, line)

    return root


def small_folders(folder):
    folders = []
    if folder.total_size <= 100000:
        folders.append(folder)

    for subfolder in folder.sub_folders:
        folders.extend(small_folders(subfolder))

    return folders


def part1(filename):
    root = parse_input(filename)
    folders = small_folders(root)
    total = sum(folder.total_size for folder in folders)
    return total


def all_folders(folder):
    folders = [folder]

    for subfolder in folder.sub_folders:
        folders.extend(all_folders(subfolder))

    return folders


def part2(filename):
    root = parse_input(filename)

    free = 70000000 - root.total_size
    cleanup = 30000000 - free

    folders = all_folders(root)
    candidates = [
        folder.total_size for folder in folders if folder.total_size >= cleanup
    ]

    return min(candidates)


assert part1(os.path.join(currentdir, "test_input.txt")) == 95437

print("Part 1: ", part1(os.path.join(currentdir, "input.txt")))


assert part2(os.path.join(currentdir, "test_input.txt")) == 24933642

print("Part 2: ", part2(os.path.join(currentdir, "input.txt")))
