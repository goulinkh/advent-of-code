characters = ["a", "b", "c", "d", "e", "f", "g"]


def parse(segments, mapping):
    zero = {"a", "b", "c", "e", "f", "g"}
    one = {"c", "f"}
    two = {"a", "c", "d", "e", "g"}
    three = {"a", "c", "d", "f", "g"}
    four = {"b", "c", "d", "f"}
    five = {"a", "b", "d", "f", "g"}
    six = {"a", "b", "d", "f", "e", "g"}
    seven = {"a", "c", "f"}
    eight = {"a", "b", "c", "d", "e", "f", "g"}
    nine = {"a", "b", "c", "d", "f", "g"}
    numbers = [zero, one, two, three, four, five, six, seven, eight, nine]
    corrected_signal = set()
    for c in segments:
        corrected_signal.add([c2 for c2 in mapping if mapping[c2] == c][0])
    for i in range(10):
        number = numbers[i]
        if number == (corrected_signal):
            return i


input_data = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""
input_data = open("./input.txt", "r").read()

input_data = map(lambda e: e.split("|"), input_data.split("\n"))
input_values, output_values = [], []
for e in input_data:
    input_values.append(e[0].split())
    output_values.append(e[1].split())

uniques = 0
for line in output_values:
    for segments in line:
        if len(segments) != 5 and len(segments) != 6:
            uniques += 1
print("part1", uniques)
outputs_sum = 0
for i in range(len(output_values)):
    input_segements = input_values[i]
    output_segements = output_values[i]

    mapping = {}
    counts = {}

    for segments in input_segements:
        for segement in segments:
            counts[segement] = counts.get(segement, 0) + 1
        size = len(segments)
        if size == 2:
            # One
            one = segments
        elif size == 3:
            # Seven
            seven = segments
        elif size == 4:
            # Four
            four = segments
    # Unique numbers
    # 1: 2 segemnts on
    # 7: 3 segemnts on
    # 4: 4 segemnts on
    # 8: 7 segemnts on (all)
    #
    # Common
    # 2: 5 segments
    # 3: 5 segments
    # 5: 5 segments
    #
    # 0: 6 segments
    # 6: 6 segments
    # 9: 6 segemnts
    mapping["a"] = (set(seven) - set(one)).pop()
    # There is only f that exist in 9 numbers
    mapping["f"] = [c for c in counts if counts[c] == 9][0]
    # There is only e that exist in 4 numbers
    mapping["e"] = [c for c in counts if counts[c] == 4][0]
    # There is only b that exist in 6 numbers
    mapping["b"] = [c for c in counts if counts[c] == 6][0]
    # Onlu a and c occures 8 times
    mapping["c"] = (
        set([c for c in counts if counts[c] == 8]) - set(mapping["a"])
    ).pop()
    zero = set(
        [
            mapping["a"],
            mapping["c"],
            mapping["f"],
            mapping["b"],
            mapping["e"],
        ]
    )
    four2 = set(
        [
            mapping["b"],
            mapping["c"],
            mapping["f"],
        ]
    )
    mapping["d"] = set(four) - four2
    mapping["g"] = set([c for c in counts if counts[c] == 7]) - mapping["d"]
    mapping["d"] = mapping["d"].pop()
    mapping["g"] = mapping["g"].pop()
    # fix the signals
    numbers = ""
    for segments in output_segements:
        numbers += str(parse(segments, mapping))
    outputs_sum += int(numbers)
    # output_values[i] = map(lambda e:, )
print("part2", outputs_sum)
