import itertools


SHORTEST = 0
TALLEST = 9

example_heights = [
    [3, 0, 3, 7, 3],
    [2, 5, 5, 1, 2],
    [6, 5, 3, 3, 2],
    [3, 3, 5, 4, 9],
    [3, 5, 3, 9, 0],
]


def visible(a):
    m = len(a[0])
    n = len(a)
    visible = [[False for i in range(m)] for row in a]

    def from_side(side="left"):
        for i, row in enumerate(a):
            max_height = SHORTEST - 1
            j = 0
            while j < m and max_height < TALLEST:
                k = m - j - 1 if side == "right" else j
                if (height := row[k]) > max_height:
                    visible[i][k] = True
                    max_height = height
                j += 1

    def from_top(b):
        max_heights = [SHORTEST - 1 for i in range(m)]
        for i, row in enumerate(b):
            for j, height in enumerate(row):
                if height > max_heights[j]:
                    visible[i][j] = True
                    max_heights[j] = height
            if max_heights == [TALLEST for i in range(m)]:
                break

    def from_bottom(b):
        nonlocal visible
        visible = list(reversed(visible))
        from_top(list(reversed(b)))
        visible = list(reversed(visible))

    from_side("left")
    from_side("right")
    from_top(a)
    from_bottom(a)

    return visible


assert visible(example_heights) == [
    [True, True, True, True, True],
    [True, True, True, False, True],
    [True, True, False, True, True],
    [True, False, True, False, True],
    [True, True, True, True, True],
]


def get_answer1(a):
    return sum(sum(row) for row in visible(a))


assert get_answer1(example_heights) == 21

heights = []
with open("./data/08-treetop_tree_house.txt", "r") as handle:
    for line in handle:
        row = [int(x) for x in line.strip()]
        heights.append(row)

answer1 = get_answer1(heights)

answer2 = None

print(answer1, answer2)
