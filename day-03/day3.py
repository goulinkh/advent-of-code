def most_common_bits(numbers_bin):
    total_sum = []
    for i in range(len(numbers_bin[0])):
        total_sum.append(0)
        for number in numbers_bin:
            total_sum[i] += number[i]
    gamma_rate, epsilon_rate = [], []
    for n in total_sum:
        # priority to 1 if both are equal
        gamma_rate.append(1 if n >= len(numbers_bin)/2 else 0)
        # priority to 0 if both are equal
        epsilon_rate.append(1 if n < len(numbers_bin)/2 else 0)
    return gamma_rate, epsilon_rate


def O_and_CO2_rating(numbers):
    numbers2 = [*numbers]
    i = 0
    while i < len(numbers[0]) and len(numbers) > 1:
        gamma_rate, _ = most_common_bits([[n[i]] for n in numbers])
        numbers = list(filter(lambda n:  (gamma_rate[0] == n[i]), numbers))
        i += 1
    oxygen_generator_rating = numbers[0]
    i = 0
    while i < len(numbers2[0]) and len(numbers2) > 1:
        _, epsilon_rate = most_common_bits([[n[i]] for n in numbers2])

        numbers2 = list(filter(lambda n:  (epsilon_rate[0] == n[i]), numbers2))
        i += 1
    CO2_scrubber_rating = numbers2[0]
    return oxygen_generator_rating, CO2_scrubber_rating


def n_to_int(n):
    return int("".join(list(map(str, n))), base=2)


numbers = open("./input.txt", "r").read().split("\n")
numbers = list(map(lambda e:  list(e), numbers))
numbers = [list(map(int, e)) for e in numbers]
gamma_rate, epsilon_rate = most_common_bits(numbers)
gamma_rate, epsilon_rate = n_to_int(gamma_rate), n_to_int(epsilon_rate)
print("gamma_rate=", gamma_rate, ", epsilon_rate=", epsilon_rate)

O, CO2 = (O_and_CO2_rating(numbers))
O, CO2 = n_to_int(O), n_to_int(CO2)
print("O=", O, ", CO2=", CO2, ", life support rating=", O*CO2)
