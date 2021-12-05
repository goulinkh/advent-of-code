def diagonal_line(line):
    left = line[0]
    right = line[1]
    return abs(left["x"] - right["x"]) == abs(left["y"] - right["y"])


def draw_diagram(lines):
    # Leave horizontal and verticals and diagonal 45° only
    h_and_v_only = filter(
        lambda line: line[0]["x"] == line[1]["x"]
        or line[0]["y"] == line[1]["y"]
        # Diagonals
        or diagonal_line(line),
        lines,
    )
    lines = list(h_and_v_only)
    # Find diagram's size
    diagram_size = 0
    for line in lines:
        diagram_size = max(
            diagram_size,
            line[0]["x"],
            line[0]["y"],
            line[1]["x"],
            line[1]["y"],
        )
    # Fill the diagram with zeros
    diagram = []
    for _ in range(diagram_size + 1):
        diagram_line = []
        for __ in range(diagram_size + 1):
            diagram_line.append(0)
        diagram.append(diagram_line)
    for line in lines:
        left, right = line[0], line[1]
        same_x = left["x"] == right["x"]
        is_diagonal_line = diagonal_line(line)
        if not is_diagonal_line:
            # swap from small -> big
            if same_x and left["y"] > right["y"]:
                t = left
                left = right
                right = t
            elif not same_x and left["x"] > right["x"]:
                t = left
                left = right
                right = t
            # Fill vertically
            if same_x:
                for i in range(left["y"], right["y"] + 1):
                    diagram[i][left["x"]] += 1
            # Fill horizontally
            else:
                for i in range(left["x"], right["x"] + 1):
                    diagram[left["y"]][i] += 1
        # Fill diagonal
        else:
            distance = abs(left["x"] - right["x"])
            for i in range(distance + 1):
                min_y = left if left["y"] < right["y"] else right
                max_y = left if min_y == right else right
                y = min_y["y"] + i
                if min_y["x"] < max_y["x"]:
                    x = i + min_y["x"]
                else:
                    x = min_y["x"] - i
                diagram[y][x] += 1
    return diagram


def print_diagram(diagram):
    for line in diagram:
        for e in line:
            if e == 0:
                print(".", end="")
            else:
                print(e, end="")
        print("")


data_input = open("./input.txt", "r").read()
# Parse input data
lines = data_input.split("\n")
lines = [
    list(map(lambda e: e.strip().split(","), line.split("->")))
    for line in lines
]
lines = [
    [
        {"x": int(line[0][0]), "y": int(line[0][1])},
        {"x": int(line[1][0]), "y": int(line[1][1])},
    ]
    for line in lines
]
# Fill the diagram
diagram = draw_diagram(lines)
# Count n > 2
twos = 0
for line in diagram:
    for e in line:
        if e >= 2:
            twos += 1
print(twos)
