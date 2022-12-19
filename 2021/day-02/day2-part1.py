
def move(current_position, direction, amount):
    if direction == "up":
        current_position["y"] -= amount
    elif direction == "down":
        current_position["y"] += amount
    elif direction == "forward":
        current_position["x"] += amount
    elif direction == "down":
        current_position["x"] -= amount
    else:
        raise ValueError(f"Wrong direction: {direction}")
    return current_position


# PART 1
commands = open("./input-part1.txt", "r").read().split("\n")
commands = list(map(lambda e: e.split(), commands))
position = {"x": 0, "y": 0}
for command in commands:
    position = move(position, command[0], int(command[1]))
print(position)
