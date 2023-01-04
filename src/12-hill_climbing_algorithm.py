import string


example_input = """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
""".strip()


def pretty_print(arr):
    for row in arr:
        for x in row:
            print(f"{x:>4}", end="")
        print("\n", end="")
    print("\n")


class Hill:
    def __init__(self, input):
        self.input = input
        self.map = input.replace("S", "a").replace("E", "z").splitlines()
        self.m, self.n = len(self.map[0]), len(self.map)
        linear_coord_S = input.replace("\n", "").index("S")
        linear_coord_E = input.replace("\n", "").index("E")
        self.y_beg, self.x_beg = divmod(linear_coord_S, self.m)
        self.y_end, self.x_end = divmod(linear_coord_E, self.m)

    def __repr__(self):
        return repr(self.input)

    def height(self, i, j):
        char = self.map[j][i]
        return string.ascii_lowercase.index(char)

    def calculate_distances(self):
        self.distances = [[-1 for _ in range(self.m)] for _ in range(self.n)]

        current_distance = 0
        self.distances[self.y_beg][self.x_beg] = current_distance
        previous_coords = {(self.x_beg, self.y_beg)}

        while current_distance < self.m * self.n:
            current_distance += 1
            next_coords = set()
            for i_prev, j_prev in previous_coords:
                consider_next = set()
                if i_prev > 0:
                    consider_next.add((i_prev - 1, j_prev))
                if i_prev < self.m - 1:
                    consider_next.add((i_prev + 1, j_prev))
                if j_prev > 0:
                    consider_next.add((i_prev, j_prev - 1))
                if j_prev < self.n - 1:
                    consider_next.add((i_prev, j_prev + 1))

                curr_height = self.height(i_prev, j_prev)
                for i_next, j_next in consider_next:
                    h = self.height(i_next, j_next)
                    d = self.distances[j_next][i_next]
                    if d == -1 and h <= curr_height + 1:
                        next_coords.add((i_next, j_next))

            if len(next_coords) == 0:
                print("All distances set!")
                pretty_print(self.distances)
                break

            for i, j in next_coords:
                self.distances[j][i] = current_distance

            previous_coords = next_coords

    def S_to_E_distance(self):
        return self.distances[self.y_end][self.x_end]


example_hill = Hill(example_input)
example_hill.calculate_distances()
assert example_hill.S_to_E_distance() == 31


with open("./data/12-hill_climbing_algorithm.txt", "r", encoding="utf-8") as handle:
    input = handle.read().strip()


hill = Hill(input)
hill.calculate_distances()

answer1 = hill.S_to_E_distance()

answer2 = None

print(answer1, answer2)
