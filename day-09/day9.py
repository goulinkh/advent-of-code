input_data = """2199943210
3987894921
9856789892
8767896789
9899965678"""
input_data = open("./input.txt", "r").read()

locations = list(
    map(lambda e: list(map(int, list(e))), input_data.split("\n"))
)

low_points = []

for i in range(len(locations)):
    for j in range(len(locations[0])):
        # Up
        if i > 0 and locations[i][j] >= locations[i - 1][j]:
            continue
        # Down
        if i < len(locations) - 1 and locations[i][j] >= locations[i + 1][j]:
            continue
        # Left
        if j > 0 and locations[i][j] >= locations[i][j - 1]:
            continue
        # Right
        if (
            j < len(locations[0]) - 1
            and locations[i][j] >= locations[i][j + 1]
        ):
            continue
        low_points.append([i, j])

print("part1", sum(map(lambda e: locations[e[0]][e[1]] + 1, low_points)))


def surrounding_points(point, excludes, locations):
    surroundings = []
    i = point[0]
    j = point[1]
    # Up
    if i > 0 and locations[i][j] < locations[i - 1][j]:
        point = [i - 1, j]
        if point not in excludes and g(point, locations) != 9:
            surroundings.append(point)
    # Down
    if i < len(locations) - 1 and locations[i][j] < locations[i + 1][j]:
        point = [i + 1, j]
        if point not in excludes and g(point, locations) != 9:
            surroundings.append(point)
    # Left
    if j > 0 and locations[i][j] < locations[i][j - 1]:
        point = [i, j - 1]
        if point not in excludes and g(point, locations) != 9:
            surroundings.append(point)
    # Right
    if j < len(locations[0]) - 1 and locations[i][j] < locations[i][j + 1]:
        point = [i, j + 1]
        if point not in excludes and g(point, locations) != 9:
            surroundings.append(point)
    return surroundings


low_points_flows = [
    {
        "points": [point],
        "excludes": [],
    }
    for point in low_points
]


def g(p, locations):
    return locations[p[0]][p[1]]


while (
    len(
        list(
            filter(
                lambda e: len(e["points"]) > len(e["excludes"]),
                low_points_flows,
            )
        )
    )
    > 0
):
    for area in low_points_flows:
        for point in area["points"]:
            if point in area["excludes"]:
                continue
            area["excludes"].append(point)
            neighbors_point = surrounding_points(
                point, area["excludes"], locations
            )
            for e in neighbors_point:
                if all(
                    map(lambda area: e not in area["points"], low_points_flows)
                ):
                    area["points"].append(e)

basins_size = []

for e in low_points_flows:
    basins_size.append(len(e["excludes"]))

result = 1
for e in sorted(basins_size)[-3:]:
    result *= e
print("part2", result)
