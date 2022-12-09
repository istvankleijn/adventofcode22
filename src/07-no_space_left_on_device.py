example_terminal = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
""".strip().split(
    "\n"
)


def parse_terminal(text):
    files = [File("/.")]
    working_directory = ""
    for line in text:
        words = line.rstrip().split()
        if words[0] == "$":
            if words[1] == "cd":
                if words[2] == "..":
                    working_directory, _, _ = working_directory.rpartition("/")
                elif words[2] != "/":
                    working_directory += "/" + words[2]
            continue
        elif words[0] == "dir":
            files.append(File(f"{working_directory}/{words[1]}/."))
        else:
            files.append(File(f"{working_directory}/{words[1]}", int(words[0])))
    return Filesystem(files)


class File:
    def __init__(self, path, size=0):
        self.path = path
        self.size = size
        self.type = "dir" if path.endswith("/.") else "file"

    def __repr__(self):
        return f"File({self.path!r}, {self.size!r})"

    def __str__(self):
        indent = "  " * self.depth()
        size_description = f", size={self.size}" if self.type == "file" else ""
        return indent + f"- {self.name()} ({self.type}{size_description})"

    def __eq__(self, other):
        return self.path == other.path

    def __lt__(self, other):
        return self.path < other.path

    def __hash__(self) -> int:
        return hash(self.path)

    def name(self):
        if self.path == "/.":
            return "/"
        name = self.path.removesuffix("/.") if self.type == "dir" else self.path
        _, _, name = name.rpartition("/")
        return name

    def depth(self):
        d = self.path.count("/")
        return d - 1 if self.type == "dir" else d


class Filesystem:
    def __init__(self, files, total_size=70000000):
        self.files = sorted(set(files))
        self.directories = [
            file.path.removesuffix("/.")
            for file in self.files
            if file.path.endswith("/.")
        ]
        self.total_size = total_size

    def __repr__(self):
        return f"Filesystem([{self.files}])"

    def __str__(self):
        return "\n".join(str(file) for file in self.files)

    def __iter__(self):
        return iter(self.files)

    def __eq__(self, other):
        return self.files == other.files

    def size(self, file):
        if file.type == "file":
            return file.size
        else:
            dirname = file.path.removesuffix("/.")
            return self.size_dir(dirname)

    def size_dir(self, dir):
        children = [f for f in self.files if f.type == "file" and dir in f.path]
        return sum(self.size(child) for child in children)

    def small_dirs(self, max_size=100000):
        total_size = 0
        small_dirs = []
        for dir in self.directories:
            size = self.size_dir(dir)
            if size <= max_size:
                total_size += size
                small_dirs.append(dir)
        return total_size, small_dirs

    def unused(self):
        return self.total_size - self.size(File("/."))


example_parsed = parse_terminal(example_terminal)

example_files = Filesystem(
    [
        File("/."),
        File("/a/."),
        File("/a/e/."),
        File("/a/e/i", 584),
        File("/a/f", 29116),
        File("/a/g", 2557),
        File("/a/h.lst", 62596),
        File("/b.txt", 14848514),
        File("/c.dat", 8504156),
        File("/d/."),
        File("/d/j", 4060174),
        File("/d/d.log", 8033020),
        File("/d/d.ext", 5626152),
        File("/d/k", 7214296),
    ]
)

assert str(example_files) == str(example_parsed)
assert example_files == example_parsed

assert example_parsed.small_dirs() == (95437, ["/a", "/a/e"])

assert example_parsed.unused() == 21618835

with open("./data/07-no_space_left_on_device.txt", "r", encoding="utf-8") as handle:
    text = [line.rstrip() for line in handle.readlines()]

filesystem = parse_terminal(text)

answer1 = filesystem.small_dirs()[0]


def get_answer2(filesystem, size_required=30000000):
    to_be_deleted = size_required - filesystem.unused()
    possible_dirs = [
        (file.path, filesystem.size(file))
        for file in filesystem.files
        if file.type == "dir" and filesystem.size(file) > to_be_deleted
    ]
    return min(possible_dirs, key=lambda x: x[1])[1]


assert get_answer2(example_parsed) == 24933642

answer2 = get_answer2(filesystem)

print(answer1, answer2)
