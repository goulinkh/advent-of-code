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

# Again I'd like thank my fellow redditers for this amazing solution

template, rules = data_input.split("\n\n")
rules = dict(rule.split(" -> ") for rule in rules.splitlines())
pairs = {pair: template.count(pair) for pair in rules}
chars = {char: template.count(char) for char in rules.values()}

for i in range(40):
    for pair, value in pairs.copy().items():
        pairs[pair] -= value
        pairs[pair[0] + rules[pair]] += value
        pairs[rules[pair] + pair[1]] += value
        chars[rules[pair]] += value
print("part2", max(chars.values()) - min(chars.values()))
