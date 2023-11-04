def create_dna():
    import random
    dna = []
    for i in range(64):
        gene = random.randint(0, 255)
        dna.append(bin(gene)[2:].zfill(8))
    return dna


def create_generation(size):
    generation = []
    for i in range(size):
        dna = create_dna()
        generation.append(dna)
    return generation


def mutate(dna, mutation_chance):
    import random
    mutated_dna = []
    for gene in dna:
        gene_list = list(gene)  # Convert the string to a list of characters
        for index in range(8):
            if random.random() < mutation_chance:
                if gene_list[index] == '0':
                    gene_list[index] = '1'
                elif gene_list[index] == '1':
                    gene_list[index] = '0'
        mutated_dna.append(''.join(gene_list))  # Convert the list back to a string
    return mutated_dna


def order_cross(parent1, parent2):
    import random
    index1 = random.randint(4, 15)
    index2 = random.randint(48, 63)
    child = parent2[:index1] + parent1[index1:index2] + parent2[index2:]
    return child


def reset_playing_field(playing_field_size, treasure_locations, player_location):
    playing_field = [[' ' for _ in range(playing_field_size)] for _ in range(playing_field_size)]
    for location in treasure_locations:
        playing_field[location[0]][location[1]] = 't'
    playing_field[player_location[0][0]][player_location[0][1]] = 'p'
    return playing_field


def find_player(playing_field_size, playing_field):
    for i in range(playing_field_size):
        for j in range(playing_field_size):
            if playing_field[i][j] == 'p':
                return i, j


def create_move(suffix):
    vypis = ''
    if suffix == "00":
        vypis += 'H'
    elif suffix == "01":
        vypis += 'D'
    elif suffix == "10":
        vypis += 'L'
    elif suffix == "11":
        vypis += 'P'
    return vypis


def pohyb(move, playing_field_size, playing_field):
    treasures = 0
    suradnice = find_player(playing_field_size, playing_field)
    if move == 'H':
        if suradnice[0] == 0:
            return -1
        else:
            if playing_field[suradnice[0] - 1][suradnice[1]] == 't':
                treasures = 1
            playing_field[suradnice[0] - 1][suradnice[1]] = 'p'
            playing_field[suradnice[0]][suradnice[1]] = ' '
    elif move == 'D':
        if suradnice[0] == playing_field_size - 1:
            return -1
        else:
            if playing_field[suradnice[0] + 1][suradnice[1]] == 't':
                treasures = 1
            playing_field[suradnice[0] + 1][suradnice[1]] = 'p'
            playing_field[suradnice[0]][suradnice[1]] = ' '
    elif move == 'L':
        if suradnice[1] == 0:
            return -1
        else:
            if playing_field[suradnice[0]][suradnice[1] - 1] == 't':
                treasures = 1
            playing_field[suradnice[0]][suradnice[1] - 1] = 'p'
            playing_field[suradnice[0]][suradnice[1]] = ' '
    elif move == 'P':
        if suradnice[1] == playing_field_size - 1:
            return -1
        else:
            if playing_field[suradnice[0]][suradnice[1] + 1] == 't':
                treasures = 1
            playing_field[suradnice[0]][suradnice[1] + 1] = 'p'
            playing_field[suradnice[0]][suradnice[1]] = ' '
    return treasures


def fitness(dna, playing_field_size, playing_field):
    index = 0
    counter = 0
    treasures = 1.000
    path = ""
    while index < len(dna) and counter < 500:
        binary_prefix = dna[index][:2]
        binary_address = dna[index][2:]
        decimal_address = int(binary_address, 2)
        if binary_prefix in ("00", "01"):
            if binary_prefix == "00":
                temp = int(dna[decimal_address], 2)
                if temp == 255:
                    dna[decimal_address] = bin(0)[2:].zfill(8)
                else:
                    dna[decimal_address] = bin(temp + 1)[2:].zfill(8)
                index += 1
            elif binary_prefix == "01":
                temp = int(dna[decimal_address], 2)
                if temp == 0:
                    dna[decimal_address] = bin(255)[2:].zfill(8)
                else:
                    dna[decimal_address] = bin(temp - 1)[2:].zfill(8)
                index += 1
        elif binary_prefix == "10":
            index = int(dna[index][2:], 2)
        elif binary_prefix == "11":
            path += create_move(dna[decimal_address][6:])
            output = pohyb(create_move(dna[decimal_address][6:]), playing_field_size, playing_field)
            if output == -1:
                return treasures
            else:
                treasures += output
                index += 1
        counter += 1
        treasures -= 0.001
    if treasures > 5.000:
        print(path)
    return treasures


def roulette(generation):
    import random
    fitness_sum = 0.0
    for individual in generation:
        fitness_sum += individual[1]
    random_number = random.uniform(0.0, fitness_sum)
    index = 0
    for individual in generation:
        index += individual[1]
        if index >= random_number:
            return individual


def tournament(generation, size):
    import random
    contenders = []
    for i in range(size):
        contenders.append(generation[random.randint(0, len(generation) - 1)])
    winner_fitness = max_fitness(contenders)
    for individual in contenders:
        if individual[1] == winner_fitness:
            return individual


def solution(generation, generation_count, max_generations, k):
    if len(generation) == 0:
        return False
    maximum = max_fitness(generation)
    if maximum > 5:
        generation_count += k*max_generations
        print("Fitness sampiona: " + str(maximum) + " v generacii: " + str(generation_count))
        for individual in generation:
            if individual[1] == maximum:
                print("DNA sampiona: ")
                print(individual[0])
                path = make_path(individual[0])
                print("Cesta sampiona: " + path)
        return True
    else:
        print("Maximalna fitness: " + str(maximum))
        return False


def max_fitness(generation):
    max_value = 0
    for individual in generation:
        if individual[1] > max_value:
            max_value = individual[1]
    return max_value


def virtual_machine(dna):
    index = 0
    counter = 0
    while index < len(dna) and counter < 500:
        binary_prefix = dna[index][:2]
        binary_address = dna[index][2:]
        decimal_address = int(binary_address, 2)
        if binary_prefix in ("00", "01"):
            if binary_prefix == "00":
                temp = int(dna[decimal_address], 2)
                if temp == 255:
                    dna[decimal_address] = bin(0)[2:].zfill(8)
                else:
                    dna[decimal_address] = bin(temp + 1)[2:].zfill(8)
                index += 1
            elif binary_prefix == "01":
                temp = int(dna[decimal_address], 2)
                if temp == 0:
                    dna[decimal_address] = bin(255)[2:].zfill(8)
                else:
                    dna[decimal_address] = bin(temp - 1)[2:].zfill(8)
                index += 1
        elif binary_prefix == "10":
            index = int(dna[index][2:], 2)
        elif binary_prefix == "11":
            output = pohyb(create_move(dna[decimal_address][6:]), 10, playing_field)
            if output == -1:
                return treasures
            else:
                treasures += output
                index += 1
        counter += 1
        treasures -= 0.001
    return treasures

def make_path(dna):
    index = 0
    path = ""
    counter = 0
    while index < len(dna) and counter < 500:
        binary_prefix = dna[index][:2]
        binary_address = dna[index][2:]
        decimal_address = int(binary_address, 2)
        if binary_prefix in ("00", "01"):
            if binary_prefix == "00":
                temp = int(dna[decimal_address], 2)
                if temp == 255:
                    dna[decimal_address] = bin(0)[2:].zfill(8)
                else:
                    dna[decimal_address] = bin(temp + 1)[2:].zfill(8)
                index += 1
            elif binary_prefix == "01":
                temp = int(dna[decimal_address], 2)
                if temp == 0:
                    dna[decimal_address] = bin(255)[2:].zfill(8)
                else:
                    dna[decimal_address] = bin(temp - 1)[2:].zfill(8)
                index += 1
        elif binary_prefix == "10":
            index = int(dna[index][2:], 2)
        elif binary_prefix == "11":
            # path += create_move(binary_suffix)
            path += create_move(dna[decimal_address][6:])
            index += 1
        counter += 1
    return path
