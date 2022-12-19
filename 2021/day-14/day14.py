data_input = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""
data_input = open("./input.txt", "r").read()


template, inputs = tuple(data_input.split("\n\n"))
insertion_rules = {}
for e in inputs.split("\n"):
    rule = e.split(" -> ")
    insertion_rules[rule[0]] = rule[1]


def step(template, insertion_rules):
    new_template = template[0]
    for i in range(len(template) - 1):
        w = template[i] + template[i + 1]
        if w in insertion_rules:
            new_template += insertion_rules[w] + template[i + 1]
        else:
            new_template += template[i + 1]
    return new_template

def count(template):
    counts = {}
    for c in template:
        counts[c] = counts.get(c, 0) + 1
    return counts


for i in range(40):
    print(i)
    template = step(template, insertion_rules)

counts = count(template)
max_count, min_count = None, None
for c in counts:
    if not max_count or counts[c] > max_count:
        max_count = counts[c]
    if not min_count or counts[c] < min_count:
        min_count = counts[c]
print("part1", max_count - min_count)

