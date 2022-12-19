import collections
import functools
import operator


def divides(n, x):
    return x % n == 0


def rpow(b, a):
    return operator.pow(a, b)


class Monkey:
    def __init__(
        self,
        items,
        op,
        val,
        test_divisor,
        *,
        bored=None,
        debug=False,
    ):
        self.items = collections.deque(items)
        self.operation = functools.partial(op, val)
        self.test = functools.partial(divides, test_divisor)
        if bored is None:
            self.bored = lambda x: x // 3
        else:
            self.bored = bored
        self.debug = debug
        self.items_inspected = 0

    def __repr__(self):
        return (
            f"Monkey({self.items!r}, {self.operation!r}, {self.test!r}, "
            + f"bored={self.bored!r})"
        )

    def take_turn(self):
        if self.debug:
            print(self.items, bool(self.items))
        while self.items:
            item = self.items.popleft()
            self.items_inspected += 1
            if self.debug:
                print(f"Monkey inspects an item with a worry level of {item}.")
            item = self.operation(item)
            if self.debug:
                print(f"Worry level increased to {item}.")
            item = self.bored(item)
            if self.debug:
                print(f"Monkey gets bored. Worry level decreased to {item}.")
            test_result = self.test(item)
            yield (item, test_result)


class MonkeyGame:
    def __init__(self, monkeys, ontrue, onfalse, *, debug=True):
        self.monkeys = list(monkeys)
        self.ontrue = dict(ontrue)
        self.onfalse = dict(onfalse)
        self.debug = debug

    def __repr__(self):
        return f"MonkeyGame({self.monkeys!r}, {self.ontrue!r}, {self.onfalse!r})"

    def __str__(self):
        out = []
        for index, monkey in enumerate(self.monkeys):
            monkey_out = f"Monkey {index}: "
            items = ", ".join(str(item) for item in monkey.items)
            monkey_out += items
            out.append(monkey_out)
        return "\n".join(out)

    @classmethod
    def from_text(cls, input, *, debug=False):
        monkeys = []
        ontrue = dict()
        onfalse = dict()
        for line in input:
            data = line.split()
            match data:
                case ["Monkey", other]:
                    index = int(other.strip(":"))
                    if debug:
                        print(f"Parsing monkey {index}")
                case ["Starting", "items:", *body]:
                    items = [int(item.strip(",")) for item in body]
                    if debug:
                        print(f"Starting {items=}")
                case ["Operation:", "new", "=", "old", "*", other]:
                    try:
                        val = int(other)
                        op = operator.mul
                        if debug:
                            print(f"Operation: multiplication, {val=}")
                    except ValueError:
                        if other == "old":
                            val = 2
                            op = rpow
                            if debug:
                                print(f"Operation: r-exponentiation, {val=}")
                        else:
                            raise ValueError("Must multiply by number or 'old'")
                case ["Operation:", "new", "=", "old", "+", other]:
                    val = int(other)
                    op = operator.add
                    if debug:
                        print(f"Operation: addition, {val=}")
                case ["Test:", "divisible", "by", other]:
                    test_divisor = int(other)
                    if debug:
                        print(f"Decision when value is divided by {test_divisor=}")
                case ["If", "true:", "throw", "to", "monkey", other]:
                    ontrue[index] = int(other)
                case ["If", "false:", "throw", "to", "monkey", other]:
                    onfalse[index] = int(other)
                case [str, *other]:
                    raise ValueError("Unexpected line data encountered.")
                case []:
                    monkeys.append(Monkey(items, op, val, test_divisor, debug=debug))
                case _:
                    raise ValueError("Unexpected line data encountered.")
        monkeys.append(Monkey(items, op, val, test_divisor, debug=debug))
        if debug:
            print("Creating Monkey")
        return cls(monkeys, ontrue, onfalse, debug=debug)

    def play_round(self):
        for index, monkey in enumerate(self.monkeys):
            if self.debug:
                print(index, monkey)
            for item, test in monkey.take_turn():
                throw_to = self.ontrue[index] if test else self.onfalse[index]
                if self.debug:
                    print(f"Item with worry level {item} thrown to monkey {throw_to}.")
                self.monkeys[throw_to].items.append(item)

    def play_rounds(self, n):
        for _ in range(n):
            self.play_round()

    def items_inspected(self):
        return sorted(
            ((i, m.items_inspected) for i, m in enumerate(self.monkeys)),
            key=lambda x: x[1],
            reverse=True,
        )

    def monkey_business(self):
        ii = self.items_inspected()
        return ii[0][1] * ii[1][1]


def get_answer1(monkeygame, n=20):
    monkeygame.play_rounds(n)
    return monkeygame.monkey_business()


m0 = Monkey([79, 98], operator.mul, 19, 23, debug=False)
m1 = Monkey([54, 65, 75, 74], operator.add, 6, 19)
m2 = Monkey([79, 60, 97], rpow, 2, 13)
m3 = Monkey([74], operator.add, 3, 17)
manual_test_game = MonkeyGame(
    [m0, m1, m2, m3], {0: 2, 1: 2, 2: 1, 3: 0}, {0: 3, 1: 0, 2: 3, 3: 1}, debug=False
)
manual_test_game.play_rounds(20)
assert manual_test_game.items_inspected() == [(3, 105), (0, 101), (1, 95), (2, 7)]


test_input = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
""".strip().splitlines()

test_game = MonkeyGame.from_text(test_input, debug=False)
test_game.play_rounds(20)
print(test_game)
assert str(test_game) == str(manual_test_game)
assert test_game.monkey_business() == 10605

with open("./data/11-monkey_in_the_middle.txt", "r", encoding="utf-8") as handle:
    lines = handle.read()

input = lines.strip().splitlines()
game = MonkeyGame.from_text(input)
game.play_rounds(20)

answer1 = game.monkey_business()

answer2 = None

print(answer1, answer2)
