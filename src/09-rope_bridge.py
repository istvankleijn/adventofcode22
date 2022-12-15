import collections
import itertools


XYCoordinates = collections.namedtuple("XYCoordinates", "x y")


class RopeTrail:
    def __init__(
        self,
        rope=None,
        *,
        visited=None,
        rope_size=2,
        origin=XYCoordinates(0, 0),
        debug=False,
    ):
        self.origin = origin
        self.debug = debug
        if rope is None:
            self.rope = [self.origin for _ in range(rope_size)]
        else:
            self.rope = rope
        if visited is None:
            self.visited = {self.tail}
        else:
            self.visited = visited

    def __repr__(self):
        return (
            f"RopeTrail({self.head}, {self.tail}, "
            f"visited={self.visited}, origin={self.origin})"
        )

    def __str__(self):
        points_by_x = sorted(
            itertools.chain(self.rope, self.visited), key=lambda point: point.x
        )
        points_by_y = sorted(
            itertools.chain(self.rope, self.visited), key=lambda point: point.y
        )
        max_x, min_x = points_by_x[-1].x, points_by_x[0].x
        size_x = 1 + max_x - min_x
        max_y, min_y = points_by_y[-1].y, points_by_y[0].y
        size_y = 1 + max_y - min_y
        output_grid = [["." for _ in range(size_x)] for _ in range(size_y)]
        for x, y in self.visited:
            output_grid[y - min_y][x - min_x] = "#"
        output_grid[self.origin.y - min_y][self.origin.x - min_x] = "s"
        for i, (x, y) in enumerate(self.rope):
            output_grid[y - min_y][x - min_x] = str(i)
        output_grid[self.head.y - min_y][self.head.x - min_x] = "H"
        return "\n".join("".join(row) for row in reversed(output_grid))

    @property
    def head(self):
        return self.rope[0]

    @head.setter
    def head(self, value):
        self.rope[0] = value

    @property
    def tail(self):
        return self.rope[-1]

    @tail.setter
    def tail(self, value):
        self.rope[-1] = value

    def move(self, direction, steps):
        for _ in range(steps):
            self.move_head(direction)
            self.drag_tail()
            if self.debug:
                print(self, "\n")

    def move_head(self, direction):
        x, y = self.head
        if direction == "U":
            self.head = XYCoordinates(x, y + 1)
        elif direction == "D":
            self.head = XYCoordinates(x, y - 1)
        elif direction == "L":
            self.head = XYCoordinates(x - 1, y)
        elif direction == "R":
            self.head = XYCoordinates(x + 1, y)
        else:
            raise ValueError(f"Cannot move head in {direction=}")

    def drag_tail(self):
        for i in range(1, len(self.rope)):
            self.drag_knot(i)
        self.visited.add(self.tail)

    def drag_knot(self, index):
        following = self.rope[index]
        ahead = self.rope[index - 1]
        distance = following.x - ahead.x, following.y - ahead.y
        match distance:
            case (x, y) if abs(x) <= 1 and abs(y) <= 1:
                pass
            case (0, -2):
                self.rope[index] = XYCoordinates(following.x, following.y + 1)
            case (0, 2):
                self.rope[index] = XYCoordinates(following.x, following.y - 1)
            case (-2, 0):
                self.rope[index] = XYCoordinates(following.x + 1, following.y)
            case (2, 0):
                self.rope[index] = XYCoordinates(following.x - 1, following.y)
            case (x, y) if -2 <= x < 0 and -2 <= y < 0:
                self.rope[index] = XYCoordinates(following.x + 1, following.y + 1)
            case (x, y) if -2 <= x < 0 and 0 < y <= 2:
                self.rope[index] = XYCoordinates(following.x + 1, following.y - 1)
            case (x, y) if 0 < x <= 2 and -2 <= y < 0:
                self.rope[index] = XYCoordinates(following.x - 1, following.y + 1)
            case (x, y) if 0 < x <= 2 and 0 < y <= 2:
                self.rope[index] = XYCoordinates(following.x - 1, following.y - 1)
            case _:
                raise ValueError(
                    f"Head-to-tail {distance=} too large!\n"
                    f"{index=}, {ahead=}, {following=}\n"
                    f"{self}"
                )

    def __len__(self):
        return len(self.visited)

    def move_from_string(self, string):
        direction, steps = string.strip().split()
        self.move(direction, int(steps))


test_instructions = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
""".strip().splitlines()

test_rope = RopeTrail()
longer_rope = RopeTrail(rope_size=10, debug=True)
for instruction in test_instructions:
    test_rope.move_from_string(instruction)
    longer_rope.move_from_string(instruction)

print(test_rope, "\n")
assert len(test_rope) == 13
assert len(longer_rope) == 1

longer_instructions = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
""".strip().splitlines()

longer_rope = RopeTrail(rope_size=10)
for instruction in longer_instructions:
    longer_rope.move_from_string(instruction)
    print(longer_rope, "\n")

assert len(longer_rope) == 36

rope = RopeTrail()
rope10 = RopeTrail(rope_size=10)
with open("./data/09-rope_bridge.txt", "r", encoding="utf-8") as handle:
    for line in handle:
        instruction = line.strip()
        rope.move_from_string(instruction)
        rope10.move_from_string(instruction)

answer1 = len(rope)

answer2 = len(rope10)

print(answer1, answer2)
