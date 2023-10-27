mutation_chance = 0.01
generation_size = 20
playing_field_size = 7
treasure_locations = [(1, 4), (2, 2), (3, 6), (4, 1), (5, 4)]
player_location = [(6, 3)]


playing_field = [[' ' for _ in range(playing_field_size)] for _ in range(playing_field_size)]
for location in treasure_locations:
    playing_field[location[0]][location[1]] = 't'
playing_field[player_location[0][0]][player_location[0][1]] = 'p'


def generate_dna(count):
    import random
    generation = []
    for i in range(count):
        dna = ""
        for j in range(8):
            dna += random.choice("10")
        generation.append(dna)
    return generation


def mutate(dna):
    mutated_dna = []
    import random
    for gene in dna:
        mutated_gene = gene
        for index in range(len(gene)):
            mutated_bit = ""
            if random.random() < mutation_chance:
                if gene[index] == "0":
                    mutated_bit = "1"
                elif gene[index] == "1":
                    mutated_bit = "0"
            else:
                mutated_bit = gene[index]
            mutated_gene = mutated_gene[:index] + mutated_bit + mutated_gene[index + 1:]
        mutated_dna.append(mutated_gene)
    return mutated_dna


def find_player():
    for i in range(playing_field_size):
        for j in range(playing_field_size):
            if playing_field[i][j] == 'p':
                return i, j


def print_field():
    for i in range(playing_field_size):
        print(playing_field[i])


def pohyb(dna):
    binary_suffix = dna[6:]
    suradnice = find_player()
    if binary_suffix == "00":
        if suradnice[0] == 0:
            playing_field[playing_field_size-1][suradnice[1]] = 'p'
            playing_field[suradnice[0]][suradnice[1]] = ' '
        else:
            playing_field[suradnice[0]-1][suradnice[1]] = 'p'
            playing_field[suradnice[0]][suradnice[1]] = ' '
        print("hore")
    elif binary_suffix == "01":
        if suradnice[0] == playing_field_size-1:
            playing_field[0][suradnice[1]] = 'p'
            playing_field[suradnice[0]][suradnice[1]] = ' '
        else:
            playing_field[suradnice[0]+1][suradnice[1]] = 'p'
            playing_field[suradnice[0]][suradnice[1]] = ' '
        print("dole")
    elif binary_suffix == "10":
        if suradnice[1] == 0:
            playing_field[suradnice[0]][playing_field_size-1] = 'p'
            playing_field[suradnice[0]][suradnice[1]] = ' '
        else:
            playing_field[suradnice[0]][suradnice[1]-1] = 'p'
            playing_field[suradnice[0]][suradnice[1]] = ' '
        print("dolava")
    elif binary_suffix == "11":
        if suradnice[1] == playing_field_size-1:
            playing_field[suradnice[0]][0] = 'p'
            playing_field[suradnice[0]][suradnice[1]] = ' '
        else:
            playing_field[suradnice[0]][suradnice[1]+1] = 'p'
            playing_field[suradnice[0]][suradnice[1]] = ' '
        print("doprava")
    print_field()


def fitness(dna):
    index = 0
    counter = 0
    vypis = 0
    while index < len(dna) and counter < 500:
        binary_prefix = dna[index][:2]
        if binary_prefix in ("00", "01"):
            binary_address = dna[index][2:]
            decimal_address = int(binary_address, 2)
            binary_suffix = dna[index][6:]
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
            #pohyb(dna[index])
            vypis += 1
            index += 1
        counter += 1


def create_generation():
    generation = []
    for i in range(generation_size):
        generation.append(generate_dna(64))
    return generation


fitness(create_generation()[0])
