import collections
import string


# useful strings:
# string.ascii_lowercase == "abcdefghijklmnopqrstuvwxyz"
# string.ascii_uppercase == "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# string.ascii_letters == string.ascii_lowercase + string.ascii_uppercase

test_input = """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""


class Rucksack:
    item_priorities = {x: i for i, x in enumerate(string.ascii_letters, start=1)}

    def __init__(self, contents):
        size = len(contents)
        if size % 2 != 0:
            raise ValueError(
                f"Size of contents should be divisible by 2. {contents=}, {size=}."
            )
        middle = len(contents) // 2
        self.compartment1 = contents[:middle]
        self.compartment2 = contents[middle:]
        self.empty = True if size == 0 else False

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

assert sum(r.shared_item_priority() for r in test_rucksacks) == 157

with open("./data/03-rucksack_reorganization.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()
    rucksacks = [Rucksack(line.rstrip()) for line in lines]

answers = sum(r.shared_item_priority() for r in rucksacks), None

print(answers)
