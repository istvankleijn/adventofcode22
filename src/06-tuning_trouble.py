import collections
import itertools


test_buffers = [
    "mjqjpqmgbljsphdztnvjfqwrcgsmlb",
    "bvwbjplbgvbhsrlpgdmjqwftvncz",
    "nppdvjthqldpwncqszvftbrmjlhg",
    "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",
    "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw",
]
expected_markers = [7, 5, 6, 10, 11]
expected_messages = [19, 23, 23, 29, 26]


def start_of_packet(iter, n_characters=4):
    chars_from_start = 0
    last_n = collections.deque(maxlen=n_characters)
    while char := next(iter):
        last_n.append(char)
        chars_from_start += 1
        if len(set(last_n)) == last_n.maxlen:
            return chars_from_start


assert list(map(lambda s: start_of_packet(iter(s)), test_buffers)) == expected_markers

assert (
    list(map(lambda s: start_of_packet(iter(s), n_characters=14), test_buffers))
    == expected_messages
)

with open("./data/06-tuning_trouble.txt", "r", encoding="utf-8") as file:
    answer1 = start_of_packet(itertools.chain.from_iterable(file))

with open("./data/06-tuning_trouble.txt", "r", encoding="utf-8") as file:
    answer2 = start_of_packet(itertools.chain.from_iterable(file), n_characters=14)


print(answer1, answer2)
