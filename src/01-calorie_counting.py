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

repr(test_data)

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

with open("./data/01-calorie_counting.txt", "r", encoding="utf-8") as file:
    input = file.read()

answer = most_calories(input)
print(answer)
