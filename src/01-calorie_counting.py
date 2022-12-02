test_data = """
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""
test_answer = 24000
test_answer_2 = 45000

def most_calories(inventories):
    most_so_far = 0
    lines = inventories.split("\n")
    elf_calories = 0
    for line in lines:
        if line == "":
            if elf_calories > most_so_far:
                most_so_far = elf_calories
            elf_calories = 0
        else:
            line_calories = int(line)
            elf_calories += line_calories

    return most_so_far

assert most_calories(test_data) == test_answer


test_elf = """
1000
2000
3000
"""

def calories_per_elf(elf):
    return sum(int(x) for x in elf.strip().split("\n"))

assert calories_per_elf(test_elf) == 6000

def top_three_sum(text):
    elves = text.split("\n\n")
    calories = [calories_per_elf(elf) for elf in elves]
    calories.sort(reverse=True)
    return sum(calories[:3])

assert top_three_sum(test_data) == test_answer_2

with open("./data/01-calorie_counting.txt", "r", encoding="utf-8") as file:
    input = file.read()

answer = most_calories(input)
print(answer)

answer_2 = top_three_sum(input)
print(answer_2)

