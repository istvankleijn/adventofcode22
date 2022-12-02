test_input = """
A Y
B X
C Z
"""

decrypt = {
    "A": "Rock",
    "B": "Paper",
    "C": "Scissors",
    "X": "Rock",
    "Y": "Paper",
    "Z": "Scissors",
}
choice_score = {
    "Rock": 1,
    "Paper": 2,
    "Scissors": 3,
}
result_score = {
    "win": 6,
    "draw": 3,
    "loss": 0,
}


def parse_line(line):
    choices = line.split(" ")
    opponent, me = tuple(decrypt[choice] for choice in choices)
    return opponent, me


assert parse_line("A Y") == ("Rock", "Paper")


def result(opponent, me):
    losses = (
        ("Rock", "Scissors"),
        ("Scissors", "Paper"),
        ("Paper", "Rock"),
    )
    wins = (
        ("Rock", "Paper"),
        ("Scissors", "Rock"),
        ("Paper", "Scissors"),
    )
    if opponent == me:
        return "draw"
    elif (opponent, me) in wins:
        return "win"
    elif (opponent, me) in losses:
        return "loss"


assert result("Rock", "Scissors") == "loss"
assert result("Rock", "Rock") == "draw"
assert result("Rock", "Paper") == "win"


def score(opponent, me):
    res = result(opponent, me)
    return choice_score[me] + result_score[res]


assert score("Rock", "Paper") == 8


def total_score(text):
    lines = text.strip().split("\n")
    scores = [score(*parse_line(line)) for line in lines]
    return sum(scores)


assert total_score(test_input) == 15

with open("./data/02-rock_paper_scissors.txt", "r", encoding="utf-8") as file:
    input = file.read()

answer = total_score(input)
print(answer)
