import itertools
import string


string.ascii_lowercase

example_input = """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
""".strip()

example_map = example_input.replace("S", "a").replace("E", "z").splitlines()


def height(i, j):
    char = example_map[j][i]
    return string.ascii_lowercase.index(char)


m, n = len(example_map[0]), len(example_map)
print(f"{m=}, {n=}")

linear_coord_S = example_input.replace("\n", "").index("S")
linear_coord_E = example_input.replace("\n", "").index("E")

y_beg, x_beg = divmod(linear_coord_S, m)
y_end, x_end = divmod(linear_coord_E, m)

distances = [[-1 for _ in range(m)] for _ in range(n)]


def pretty_print(arr):
    for row in arr:
        for x in row:
            print(f"{x:>3}", end="")
        print("\n", end="")
    print("\n")


current_distance = 0
distances[y_beg][x_beg] = current_distance
previous_coords = {(x_beg, y_beg)}

while current_distance < m * n:
    current_distance += 1
    next_coords = set()
    print(f"{previous_coords=}")
    for i_prev, j_prev in previous_coords:
        consider_next = set()
        if i_prev > 0:
            consider_next.add((i_prev - 1, j_prev))
        if i_prev < m - 1:
            consider_next.add((i_prev + 1, j_prev))
        if j_prev > 0:
            consider_next.add((i_prev, j_prev - 1))
        if j_prev < n - 1:
            consider_next.add((i_prev, j_prev + 1))

        print(f"{consider_next=}")

        curr_height = height(i_prev, j_prev)
        for i_next, j_next in consider_next:
            print(f"Considering {i_next=} and {j_next=}:")
            h = height(i_next, j_next)
            d = distances[j_next][i_next]
            print(f"{h=}, {curr_height=}; {d=}")
            if d == -1 and h <= curr_height + 1:
                next_coords.add((i_next, j_next))

    if len(next_coords) == 0:
        print("All distances set!")
        pretty_print(distances)
        break

    print(f"Setting {current_distance=} for {next_coords=}")
    for i, j in next_coords:
        distances[j][i] = current_distance

    pretty_print(distances)

    previous_coords = next_coords

pretty_print(distances)
