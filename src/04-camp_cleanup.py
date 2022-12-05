test_lines = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
""".strip().split(
    "\n"
)


class Pair:
    def __init__(self, elf1, elf2):
        self.elf1 = elf1
        self.elf2 = elf2

    @classmethod
    def from_string(cls, string):
        elf1, elf2 = (cls.elf_from_string(x) for x in string.split(","))
        return cls(elf1, elf2)

    @staticmethod
    def elf_from_string(string):
        left, right = string.split("-")
        return range(int(left) - 1, int(right))

    def __repr__(self):
        return f"Pair({self.elf1!r}, {self.elf2!r})"

    def overlap(self):
        start = max(self.elf1.start, self.elf2.start)
        stop = min(self.elf1.stop, self.elf2.stop)
        return range(start, stop) if start < stop else range(0)

    def is_contained(self):
        shared = self.overlap()
        return shared == self.elf1 or shared == self.elf2

    def has_overlap(self):
        return True if self.overlap() != range(0) else False


test_pairs = [Pair.from_string(line) for line in test_lines]


def get_answer_1(pairs):
    return sum(pair.is_contained() for pair in pairs)


assert get_answer_1(test_pairs) == 2


def get_answer_2(pairs):
    return sum(pair.has_overlap() for pair in pairs)


assert get_answer_2(test_pairs) == 4


with open("./data/04-camp_cleanup.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()
    pairs = [Pair.from_string(line.rstrip()) for line in lines]

answers = get_answer_1(pairs), get_answer_2(pairs)

print(answers)
