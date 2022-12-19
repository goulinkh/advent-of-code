input_data = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

input_data = open("./input.txt", "r").read()


def adjacent(coordinates, grid):
    (x, y) = coordinates
    coordinations = []
    if x > 0:
        # left
        coordinations.append((x - 1, y))
    if x < len(grid[0]) - 1:
        # right
        coordinations.append((x + 1, y))
    if y > 0:
        # up
        coordinations.append((x, y - 1))
    if y < len(grid) - 1:
        # down
        coordinations.append((x, y + 1))
    # diagonals
    if x > 0 and y > 0:
        # top left
        coordinations.append((x - 1, y - 1))
    if x > 0 and y < len(grid) - 1:
        # down left
        coordinations.append((x - 1, y + 1))
    if x < len(grid[0]) - 1 and y > 0:
        # top right
        coordinations.append((x + 1, y - 1))
    if x < len(grid[0]) - 1 and y < len(grid) - 1:
        # down right
        coordinations.append((x + 1, y + 1))
    return coordinations


def incr(v):
    if v < 9:
        return v + 1
    else:
        return v


def prnt(grid):
    for line in grid:
        for e in line:
            print(e, end="")
        print()


def step(grid):
    flashed_octopuses = []
    count = {}
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            e = grid[i][j]
            count[e] = count.get(e, []) + [(i, j)]
    while count.get(9, []):
        c = count[9].pop()
        flashed_octopuses.append(c)
        grid[c[0]][c[1]] = 0
        siblings = adjacent(c, grid)
        for sibling in siblings:
            if (
                sibling in flashed_octopuses
                or grid[sibling[0]][sibling[1]] == 9
            ):
                continue
            grid[sibling[0]][sibling[1]] = incr(grid[sibling[0]][sibling[1]])
            if grid[sibling[0]][sibling[1]] == 9:
                count[9].append(sibling)

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (i, j) not in flashed_octopuses:
                grid[i][j] = incr(grid[i][j])

    return grid, len(flashed_octopuses)


flashes = 0
grid = [list(map(int, line)) for line in input_data.split("\n")]

for _ in range(100):
    grid, f = step(grid)
    flashes += f
print("step1", flashes)


grid = [list(map(int, line)) for line in input_data.split("\n")]

all_flashed = False
step_number = 1
while not all_flashed:
    grid, flashes = step(grid)
    if flashes == len(grid) * len(grid[0]):
        print("step2", step_number)
        break
    step_number += 1
