import toolbox as tb
import random as rd

CHROMOSOME_1 = tb.import_population("datas\chromosome_1.json")[0]

# Swap 2 random timeslot 

def swap_timeslot(chr):
    """
    Returns a chromosome with two mutated genes
    """
    # Select two random rows
    indices = rd.sample(range(len(chr)), 2)
    
    # Swap values between the selected rows for "Start_Time" and "Start_day "
    temp_start_time = chr[indices[0]].start_time
    chr[indices[0]].start_time = chr[indices[1]].start_time 
    chr[indices[1]].start_time = temp_start_time

    temp_start_day = chr[indices[0]].start_day
    chr[indices[0]].start_day = chr[indices[1]].start_day
    chr[indices[1]].start_day = temp_start_day
    
    return chr


# Change 1 random timeslot 

def change_timeslot(chr):
    """
    Returns a chromosome with one mutated gene
    """
    indice = rd.randint(0, len(chr))

    # Change the value of "Start_Time" and "Start_day " of a random gene
    chr[indice].start_time = rd.randrange((tb.END_TIME - tb.START_TIME + 1) // 30 + 1) * tb.MINUTES_PER_CELL + tb.START_TIME
    chr[indice].start_day = rd.randint(0,tb.DAYS)

    return chr


# Swap 2 random timeslot 

def swap_room(chr):
    """
    Returns a chromosome with two mutated genes
    """
    # Select two random rows
    indices = rd.sample(range(len(chr)), 2)

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
    indice = rd.randint(0, len(chr))
    indice_room = rd.randint(0, len(tb.get_rooms()))

    # Change the value of "Start_Time" and "Start_day " of a random gene
    chr[indice].room = tb.get_rooms()[indice_room].room

    return chr


# Random mutation function

def random_mutation(chr):
    """
    Choose a random mutation 
    """
    # List of all mutation
    mutations = [swap_timeslot, change_timeslot, swap_room, change_room]

    # Choose one randomly
    mutation_aleatoire = rd.choice(mutations)
    return mutation_aleatoire(chr)

    

if __name__ == '__main__':
    print("Mutation...")
    print(CHROMOSOME_1)
    """
    print("Swap_room:")
    print(swap_room(CHROMOSOME_1))
    print("Change_room")
    print(change_room(CHROMOSOME_1))
    print("Swap_timeslot")
    print(swap_room(CHROMOSOME_1))
    print("Change_timeslot")
    print(change_timeslot(CHROMOSOME_1))
    """
    print("Random_mutation")
    print(random_mutation(CHROMOSOME_1))
    