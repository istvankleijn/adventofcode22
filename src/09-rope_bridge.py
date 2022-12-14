import collections


XYCoordinates = collections.namedtuple("XYCoordinates", "x y")


class RopeTrail:
    def __init__(self, rope=None, *, visited=None, rope_size=2):
        if rope is None:
            self.rope = [XYCoordinates(0, 0) for _ in range(rope_size)]
        else:
            self.rope = rope
        if visited is None:
            self.visited = {self.tail}
        else:
            self.visited = visited

    def __repr__(self):
        return f"RopeTrail({self.head}, {self.tail}, visited={self.visited})"

    @property
    def head(self):
        return self.rope[0]

    @property
    def tail(self):
        return self.rope[-1]

    def move(self, direction, steps):
        for _ in range(steps):
            self.move_head(direction)
            tail_too_far = (
                abs(self.head.x - self.tail.x) > 1 or abs(self.head.y - self.tail.y) > 1
            )
            if tail_too_far:
                self.drag_tail()
                self.visited.add(self.tail)

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
        distance = XYCoordinates(self.tail.x - self.head.x, self.tail.y - self.head.y)
        match distance:
            case XYCoordinates(-2, y):
                self.tail = XYCoordinates(self.head.x - 1, self.head.y)
            case XYCoordinates(2, y):
                self.tail = XYCoordinates(self.head.x + 1, self.head.y)
            case XYCoordinates(x, -2):
                self.tail = XYCoordinates(self.head.x, self.head.y - 1)
            case XYCoordinates(x, 2):
                self.tail = XYCoordinates(self.head.x, self.head.y + 1)
            case _:
                raise ValueError(f"Head-to-tail {distance=} too large!")

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
for instruction in test_instructions:
    test_rope.move_from_string(instruction)

print(test_rope)
assert len(test_rope) == 13

rope = RopeTrail()
with open("./data/09-rope_bridge.txt", "r", encoding="utf-8") as handle:
    for line in handle:
        rope.move_from_string(line.strip())

answer1 = len(rope)

answer2 = None

print(answer1, answer2)
