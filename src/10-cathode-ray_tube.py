import collections
import itertools
import queue


# def monitor_strengths(
#     input, *, at_time=20, period=40, x_init=1, noop_cycles=1, addx_cycles=2, max_cycles
# ):
#     x = x_init
#     # buffer = collections.deque(itertools.repeat(0, addx_cycles))
#     clock = 0
#     strengths = []
#     # padding = ("noop", "noop")
#     for clock in range(max_cycles):
#         # for line in itertools.chain(input.splitlines(), padding):
#         instruction = line.split()
#         if instruction[0] == "addx":
#             # buffer.appendleft(int(instruction[1]))
#             clock += 1
#         elif instruction[0] == "noop":
#             clock += 1
#             # buffer.appendleft(0)
#         if clock % period == at_time:
#             strengths.append((clock, clock * x))
#         x += buffer.pop()
#         clock += 1
#     return strengths

INSTRUCTION_TIMES = {"noop": 1, "addx": 2}


def parse_instructions(input, *, x_init=1):
    x = x_init
    time = 0
    xs = [(time, x)]
    for line in input:
        instruction = line.split()
        time += INSTRUCTION_TIMES[instruction[0]]
        if instruction[0] == "addx":
            x += int(instruction[1])
        xs.append((time, x))
    return xs


def calculate_strengths(xs, observation_times):
    strengths = []
    for observation_time in observation_times:
        for i, (t_next, _) in enumerate(xs):
            _, x_prev = xs[i - 1]
            if t_next >= observation_time:
                skip = i
                break
        strengths.append(observation_time * x_prev)
    return strengths


test_input = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
""".strip().splitlines()

test_xs = parse_instructions(test_input)
observe_at = range(20, 240, 40)
test_strengths = calculate_strengths(test_xs, observe_at)

assert test_strengths == [420, 1140, 1800, 2940, 2880, 3960]


with open("./data/10-cathode-ray_tube.txt", "r", encoding="utf-8") as handle:
    lines = handle.read()

input = lines.strip().splitlines()
xs = parse_instructions(input)

print(xs)

signal_strengths = calculate_strengths(xs, observe_at)

answer1 = sum(signal_strengths)

answer2 = None

print(answer1, answer2)
