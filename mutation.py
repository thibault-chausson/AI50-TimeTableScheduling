import toolbox as tb
import random as rd
import variables as var

CHROMOSOME_1 = tb.import_population("./datas/chromosome_1.json")[0]


# Swap 2 random timeslot

def swap_timeslot(chr):
    """
    Returns a chromosome with two mutated genes
    """
    # Select two random rows
    indices = rd.sample(range(len(chr) - 1), 2)

    # Verifier que les deux start_time + duration ne depasse pas la fin de la journée (end_time)

    if chr[indices[0]].start_time + chr[indices[1]].duration > var.END_TIME and chr[indices[1]].start_time + chr[
        indices[0]].duration > var.END_TIME:
        # Swap values between the selected rows for "Start_Time" and "Start_day "
        temp_start_time = chr[indices[0]].start_time
        chr[indices[0]].start_time = chr[indices[1]].start_time
        chr[indices[1]].start_time = temp_start_time

        temp_start_day = chr[indices[0]].start_day
        chr[indices[0]].start_day = chr[indices[1]].start_day
        chr[indices[1]].start_day = temp_start_day
    else:  # on fait un changement de timeslot
        chr = change_timeslot(chr)

    return chr


# Change 1 random timeslot

import random


def random_step(debut, fin, pas):
    steps = int((fin - debut) / pas)
    res = random.randint(0, steps)
    return debut + res * pas


def change_timeslot(chr):
    """
    Returns a chromosome with one mutated gene
    """
    indice = rd.randint(0, len(chr) - 1)

    # Change the value of "Start_Time" and "Start_day " of a random gene
    chr[indice].start_time = random_step(var.START_TIME, var.END_TIME - chr[indice].duration, var.MINUTES_PER_CELL)
    chr[indice].start_day = rd.randint(0, var.DAYS - 1)

    return chr


# Swap 2 random timeslot 

def swap_room(chr):
    """
    Returns a chromosome with two mutated genes
    """
    # Select two random rows
    indices = rd.sample(range(len(chr) - 1), 2)

    # Swap values between the selected rows for "room"
    temp_start_room = chr[indices[0]].room
    chr[indices[0]].room = chr[indices[1]].room
    chr[indices[1]].room = temp_start_room

    return chr


# Change 1 random room

def change_room(chr):
    """
    Returns a chromosome with one mutated gene
    """
    indice = rd.randint(0, len(chr) - 1)
    indice_room = rd.randint(0, len(tb.get_rooms()) - 1)

    # Change the value of "Start_Time" and "Start_day " of a random gene
    chr[indice].room = tb.get_rooms()[indice_room].room

    return chr


# Random mutation function

def random_mutation(chr):
    """
    Choose a random mutation 
    """
    # List of all mutation
    mutations = [change_timeslot, swap_timeslot]  # [swap_timeslot, change_timeslot, swap_room, change_room]

    # Choose one randomly
    mutation_aleatoire = rd.choice(mutations)
    return mutation_aleatoire(chr)


if __name__ == '__main__':
    print("Mutation...")
    print(CHROMOSOME_1)

    print("Swap_room:")
    print(swap_room(CHROMOSOME_1))
    print("Change_room")
    print(change_room(CHROMOSOME_1))
    print("Swap_timeslot")
    print(swap_room(CHROMOSOME_1))
    print("Change_timeslot")
    print(change_timeslot(CHROMOSOME_1))

    print("Random_mutation")
    print(random_mutation(CHROMOSOME_1))
