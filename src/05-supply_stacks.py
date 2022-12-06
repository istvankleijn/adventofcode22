test_input = """
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""


def parse_start(text):
    from_ground_up = reversed(text.split("\n"))
    index_line = next(from_ground_up)
    stacks = [[] for index in index_line.split()]
    for line in from_ground_up:
        crates = line[1::4]
        for crate, stack in zip(crates, stacks):
            if crate != " ":
                stack += crate
    return stacks


def parse_moves(text):
    moves = []
    for line in text.strip().split("\n"):
        words = line.split()
        move = tuple(int(x) for x in words[1::2])
        moves.append(move)
    return moves


def parse(text):
    header, body = text.split("\n\n")
    start = parse_start(header)
    moves = parse_moves(body)
    return start, moves


expected_start = [["Z", "N"], ["M", "C", "D"], ["P"]]
expected_moves = [(1, 2, 1), (3, 1, 3), (2, 2, 1), (1, 1, 2)]
assert parse(test_input) == (expected_start, expected_moves)


class Crates:
    def __init__(self, stacks):
        self.stacks = [[]] + [list(stack) for stack in stacks]  # dummy for index 0

    def __repr__(self):
        return repr(self.stacks)

    def move_one(self, n, i, j):
        from_stack = self.stacks[i]
        to_stack = self.stacks[j]
        for i in range(n):
            to_stack.append(from_stack.pop())
        return self

    def move(self, moves):
        for move in moves:
            self.move_one(*move)

    def read_top(self):
        return "".join(stack[-1] if stack != [] else "" for stack in self.stacks)


test_crates = Crates(expected_start)
test_crates.move(expected_moves)
assert test_crates.read_top() == "CMZ"


with open("./data/05-supply_stacks.txt", "r", encoding="utf-8") as file:
    input = file.read()

start, moves = parse(input)
crates = Crates(start)
crates.move(moves)
answer1 = crates.read_top()


answer2 = None

print(answer1, answer2)
