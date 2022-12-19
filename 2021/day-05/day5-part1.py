data_input = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""
# PART 1
data_input = open("./input.txt", "r").read()


def draw_diagram(lines):
    # Leave horizontal and verticals only
    h_and_v_only = filter(
        lambda line: line[0]["x"] == line[1]["x"]
        or line[0]["y"] == line[1]["y"],
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
        # Normalize all the cases
        left, right = line[0], line[1]
        same_x = left["x"] == right["x"]
        if same_x and left["y"] > right["y"]:
            t = left
            left = right
            right = t
        elif not same_x and left["x"] > right["x"]:
            t = left
            left = right
            right = t
        # Fill vertically
        # 7,0 -> 7,4
        # 9,4 -> 3,4

        if same_x:
            for i in range(left["y"], right["y"] + 1):
                diagram[i][left["x"]] += 1
        # Fill horizontally
        else:
            for i in range(left["x"], right["x"] + 1):
                diagram[left["y"]][i] += 1
    return diagram


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
diagram = draw_diagram(lines)
twos = 0
for line in diagram:
    for e in line:
        if e >= 2:
            twos += 1
print(twos)
