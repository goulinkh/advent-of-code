def spawn(spawn_list, days_left):
    if days_left == 0:
        return len(spawn_list)
    spawn_list_with_fries = []
    for e in spawn_list:
        if e == 0:
            spawn_list_with_fries.append(6)
            spawn_list_with_fries.append(8)
        else:
            spawn_list_with_fries.append(e - 1)
    days_left -= 1
    return spawn(spawn_list_with_fries, days_left)


input_data = open("./input.txt", "r").read()


# Input parsing
fish_spawn_list = input_data.split(",")
fish_spawn_list = [int(e) for e in fish_spawn_list]
print(spawn(fish_spawn_list, 80))
