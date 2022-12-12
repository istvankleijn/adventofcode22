SHORTEST = 0
TALLEST = 9

example_heights = [
    [3, 0, 3, 7, 3],
    [2, 5, 5, 1, 2],
    [6, 5, 3, 3, 2],
    [3, 3, 5, 4, 9],
    [3, 5, 3, 9, 0],
]


def from_left(a):
    m = len(a[0])
    n = len(a)
    visible = [[False for i in range(m)] for row in a]
    for i, row in enumerate(a):
        max_height = SHORTEST - 1
        j = 0
        while j < m and max_height < TALLEST:
            if (height := row[j]) > max_height:
                visible[i][j] = True
                max_height = height
            j += 1
    return visible


def from_right(a):
    m = len(a[0])
    n = len(a)
    visible = [[False for i in range(m)] for row in a]
    for i, row in enumerate(a):
        max_height = SHORTEST - 1
        j = 0
        while j < m and max_height < TALLEST:
            if (height := row[m - j - 1]) > max_height:
                visible[i][m - j - 1] = True
                max_height = height
            j += 1
    return visible


def from_top(a):
    m = len(a[0])
    n = len(a)
    visible = [[False for i in range(m)] for row in a]
    max_heights = [SHORTEST - 1 for i in range(m)]
    for i, row in enumerate(a):
        for j, height in enumerate(row):
            if height > max_heights[j]:
                visible[i][j] = True
                max_heights[j] = height
        if max_heights == [TALLEST for i in range(m)]:
            break
    return visible


def from_bottom(a):
    return list(reversed(from_top(list(reversed(a)))))


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


print(from_left(example_heights))
print(from_right(example_heights))
print(from_top(example_heights))
print(from_bottom(example_heights))

print(visible(example_heights))

assert from_left(example_heights) == [
    [True, False, False, True, False],
    [True, True, False, False, False],
    [True, False, False, False, False],
    [True, False, True, False, True],
    [True, True, False, True, False],
]
assert from_right(example_heights) == [
    [False, False, False, True, True],
    [False, False, True, False, True],
    [True, True, False, True, True],
    [False, False, False, False, True],
    [False, False, False, True, True],
]
assert from_top(example_heights) == [
    [True, True, True, True, True],
    [False, True, True, False, False],
    [True, False, False, False, False],
    [False, False, False, False, True],
    [False, False, False, True, False],
]
assert from_bottom(example_heights) == [
    [False, False, False, False, False],
    [False, False, False, False, False],
    [True, False, False, False, False],
    [False, False, True, False, True],
    [True, True, True, True, True],
]
assert visible(example_heights) == [
    [True, True, True, True, True],
    [True, True, True, False, True],
    [True, True, False, True, True],
    [True, False, True, False, True],
    [True, True, True, True, True],
]
