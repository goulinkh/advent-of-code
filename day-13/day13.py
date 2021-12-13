def fold_paper(fold_details, points, paper):
    direction, value = fold_details

    for i in range(len(points)):
        (x, y) = points[i]

        if direction == "y" and y >= value:
            points[i] = (x, value - abs(value - y))
            paper["y"] = value
        elif direction == "x" and x >= value:
            points[i] = (value - abs(value - x), y)
            paper["x"] = value
    return points, paper


def prnt():
    for line in paper["grid"]:
        for c in line:
            print(c, end="")
        print("")


def fill_paper(points, paper):

    new_grid = []
    for i in range(paper["y"]):
        line = []
        for j in range(paper["x"]):
            line.append("." if (j, i) not in points else "#")
        new_grid.append(line)
    paper["grid"] = new_grid
    return paper


def count_dots(grid):
    total_sum = 0
    for line in grid:
        for c in line:
            if c == "#":
                total_sum += 1
    return total_sum


data_input = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""
data_input = open("./input.txt", "r").read()

fst_section, snd_section = tuple(data_input.split("\n\n"))
fst_section = [tuple(map(int, e.split(","))) for e in fst_section.split("\n")]
folds = [
    tuple(line.replace("fold along ", "").split("="))
    for line in snd_section.split("\n")
]

folds = [(direction, int(value)) for (direction, value) in folds]


max_x, max_y = 0, 0
for (x, y) in fst_section:
    if x > max_x:
        max_x = x
    if y > max_y:
        max_y = y

paper = {"grid": [], "y": max_y + 1, "x": max_x + 1}
for i in range(len(folds)):
    fold = folds[i]

    fst_section, paper = fold_paper(fold, fst_section, paper)
    if i == 0:
        paper = fill_paper(fst_section, paper)
        print(
            "part1",
            count_dots(paper["grid"]),
        )
paper = fill_paper(fst_section, paper)
print("Part2")
prnt()
