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


def start_of_packet(iter, n_characters=4):
    chars_from_start = 0
    last_four = collections.deque(maxlen=n_characters)
    while char := next(iter):
        last_four.append(char)
        chars_from_start += 1
        if len(set(last_four)) == last_four.maxlen:
            return chars_from_start


assert list(map(lambda s: start_of_packet(iter(s)), test_buffers)) == expected_markers


with open("./data/06-tuning_trouble.txt", "r", encoding="utf-8") as file:
    answer1 = start_of_packet(itertools.chain.from_iterable(file))

answer2 = None

print(answer1, answer2)
