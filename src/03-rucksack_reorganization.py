import string


test_input = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""


class Rucksack:
    item_priorities = {x: i for i, x in enumerate(string.ascii_letters, start=1)}

    def __init__(self, contents):
        self.contents = contents
        size = len(contents)
        if size % 2 != 0:
            raise ValueError(
                f"Size of contents should be divisible by 2. {contents=}, {size=}."
            )
        middle = len(contents) // 2
        self.compartment1 = contents[:middle]
        self.compartment2 = contents[middle:]
        self.empty = True if size == 0 else False

    def __repr__(self):
        return f"Rucksack({self.contents!r})"

    def shared_item_type(self):
        if self.empty:
            return None
        intersection = set(self.compartment1) & set(self.compartment2)
        if len(intersection) > 1:
            raise IndexError(
                "More than one shared item type.\n"
                f"{self.compartment1=}\n{self.compartment2=}\n{intersection=}"
            )
        return intersection.pop()

    def shared_item_priority(self, default=0):
        cls = type(self)
        item_type = self.shared_item_type()
        return cls.item_priorities.get(item_type, default)


test_rucksacks = [Rucksack(contents) for contents in test_input.split("\n")]


def get_answer1(sacks):
    return sum(r.shared_item_priority() for r in sacks)


assert get_answer1(test_rucksacks) == 157


def groups(sacks):
    all_groups = []
    current_group = []
    for elf, sack in enumerate(sacks):
        current_group.append(sack)
        if elf % 3 == 2:
            all_groups.append(current_group)
            current_group = []
    return all_groups


def badge(group):
    items = [set(sack.contents) for sack in group]
    shared_items = items[0].intersection(*items[1:])
    if len(shared_items) > 1:
        raise IndexError(
            "More than one shared item type.\n" f"{items=}\n{shared_items=}"
        )
    return shared_items.pop()


def get_answer2(sacks):
    return sum(Rucksack.item_priorities[badge(group)] for group in groups(sacks))


assert get_answer2(test_rucksacks) == 70

with open("./data/03-rucksack_reorganization.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()
    rucksacks = [Rucksack(line.rstrip()) for line in lines]

answers = get_answer1(rucksacks), get_answer2(rucksacks)

print(answers)
