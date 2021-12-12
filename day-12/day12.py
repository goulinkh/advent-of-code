raw_data = open("input.txt", "r").read()

# I'd like to thank reddit for the huge inspiration
# for the cleanest solution that I've done so fare xD


def parse_input(raw_data):
    res = {}
    for row in raw_data.split("\n"):
        u, v = row.split("-")
        res[u] = res.get(u, []) + [v]
        res[v] = res.get(v, []) + [u]
    return res


GRAPH = parse_input(raw_data)


def iterate(node, seen, two=False):
    if seen:
        if node == "end":
            return 1
        if node == "start":
            return 0
    if node.islower() and node in seen:
        if two:
            two = False
        else:
            return 0
    seen = seen | {node}
    res = 0
    for children in GRAPH[node]:
        res += iterate(children, seen, two)
    return res


print("part1", iterate("start", set()))
print("part2", iterate("start", set(), True))
