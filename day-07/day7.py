data_input = """16,1,2,0,4,2,7,1,2,14"""
data_input = open("./input.txt", "r").read()
expected_response = 37
positions = list(map(int, data_input.split(",")))
counts = []
for i in range(max(positions) + 1):
    counts.append((i, 0))
for p in positions:
    counts[p] = (counts[p][0], counts[p][1] + 1)

# Calculate the cost#
costs = []
for count in counts:
    costs.append(sum((abs(count[0] - pos)) * length for pos, length in counts))

print("part1", min(costs))


def triangular_number(n):
    return sum(range(n + 1))


triangular_numbers = []
for i in range(max(positions) + 1):
    triangular_numbers.append(triangular_number(i))

costs = []
for count in counts:
    costs.append(
        sum(
            triangular_numbers[(abs(count[0] - pos))] * length
            for pos, length in counts
        )
    )

print("part2", min(costs))
