def spawn(spawn_routine, days_left):
    for _ in range(days_left):
        # new day time to work...
        d0 = spawn_routine.pop(0)
        spawn_routine[6] += d0
        spawn_routine.append(d0)
    return sum(spawn_routine)


input_data = open("./input.txt", "r").read()

# Input parsing
fish_spawn_list = input_data.split(",")
fish_spawn_list = [int(e) for e in fish_spawn_list]

spawn_routine = []
for i in range(9):
    spawn_routine.append(0)
for fish in fish_spawn_list:
    spawn_routine[fish] += 1
print(spawn(spawn_routine, 256))
