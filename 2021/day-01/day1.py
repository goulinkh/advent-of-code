def measure_depth_increases(depths):
    """
    :returns number of increases that occurred in the given depths
    """
    previous_depth = depths.pop(0)
    increases = 0
    for depth_measurement in depths:
        if depth_measurement > previous_depth:
            increases += 1
        previous_depth = depth_measurement
    return increases


def with_sliding_windows(depths):
    """
    :returns depths where each one is the sum of 3 successive given depths
    """
    slide_size = 3
    sliding_depths = []

    z = []
    z.append([0, 0])

    for i in range(len(depths)):
        depth = depths[i]
        for j in range(len(z)):
            z[j][0] += 1
            z[j][1] += depth

        # Check for end of slides
        for j in range(slide_size):
            if j < len(z) and z[j][0] == slide_size:
                sliding_depths.append(z.pop(0)[1])
                # Only one element will end at each iteration
                break
        if len(z) < slide_size and len(depths) - i > slide_size:
            z.append([0, 0])
    return sliding_depths


# PART 1
depth_inputs = open("./input-part1.txt", "r").read().split("\n")
depth_inputs.pop()
depth_inputs = list(map(int, depth_inputs))
print(measure_depth_increases(depth_inputs))


# PART 2
depth_inputs = open("./input-part2.txt", "r").read().split("\n")
depth_inputs.pop()
depth_inputs = list(map(int, depth_inputs))
print(measure_depth_increases(with_sliding_windows(depth_inputs)))
