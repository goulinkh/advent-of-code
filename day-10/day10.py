import queue

broken_c_score_table = {")": 3, "]": 57, "}": 1197, ">": 25137}
missing_c_score_table = {")": 1, "]": 2, "}": 3, ">": 4}
mapping = {"[": "]", "{": "}", "<": ">", "(": ")"}

input_data = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""
input_data = open("./input.txt", "r").read()

lines = input_data.split("\n")


score = 0

corropted_lines = []

for i in range(len(lines)):
    line = lines[i]
    q = queue.LifoQueue()
    for c in line:
        if c in {"[", "{", "<", "("}:
            q.put(c)
        else:
            opening_c = q.get()
            if mapping[opening_c] != c:
                # corrupted line
                corropted_lines.append(i)
                score += broken_c_score_table[c]
print("part1", score)

# Iterate through the incomplete lines only
scores = []
for line in [lines[i] for i in range(len(lines)) if i not in corropted_lines]:
    q = queue.LifoQueue()
    for c in line:
        if c in {"[", "{", "<", "("}:
            q.put(c)
        else:
            q.get()
    p_score = 0
    while not q.empty():
        p_score *= 5
        p_score += missing_c_score_table[mapping[q.get()]]
    scores.append(p_score)

print("part2", sorted(scores)[len(scores) // 2])
