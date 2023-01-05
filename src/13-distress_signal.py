import logging


# logging.basicConfig(level=logging.INFO)


test_input = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
""".strip()

# use None for unknown answer
def signals_ordered(left, right):
    logging.info(f"Compare {left} vs {right}")
    match left, right:
        case int(), int() if left < right:
            logging.info("Left side smaller so inputs in *right order*.")
            return True
        case int(), int() if left > right:
            logging.info("Right side smaller, so inputs *not* ordered.")
            return False
        case int(), int() if left == right:
            return None
        case list(), list():
            for l, r in zip(left, right):
                if (result := signals_ordered(l, r)) is not None:
                    return result
            else:  # all results are None
                if len(left) < len(right):
                    logging.info(
                        "Left side ran out of items, so inputs in *right order*."
                    )
                    return True
                elif len(left) > len(right):
                    logging.info(
                        "Right side ran out of items, so inputs *not* ordered."
                    )
                    return False
                else:
                    return None

        case int(), list():
            logging.info(f"Mixed types, convert left to [{left}] and retry")
            return signals_ordered([left], right)
        case list(), int():
            logging.info(f"Mixed types, convert right to [{right}] and retry")
            return signals_ordered(left, [right])
        case _:
            raise TypeError("Signals must be 'list's or 'int's")


def pairs_in_order(input):
    result = []
    for i, signal in enumerate(input.split("\n\n"), start=1):
        left, right = eval(signal.replace("\n", ", "))
        logging.info(f"== Pair {i} ==")
        result.append(signals_ordered(left, right))
    return result


assert pairs_in_order(test_input) == [
    True,
    True,
    False,
    True,
    False,
    True,
    False,
    False,
]


def sum_of_indices_where_truthy(sequence):
    return sum(i for i, val in enumerate(sequence, start=1) if val)


def get_answer1(input):
    return sum_of_indices_where_truthy(pairs_in_order(input))


assert get_answer1(test_input) == 13


with open("./data/13-distress_signal.txt", "r", encoding="utf-8") as handle:
    input = handle.read().strip()


answer1 = get_answer1(input)

answer2 = None

print(answer1, answer2)
