import random as rd
import selection as sl
import crossover as cr
import mutation as mt
import replace as rp
import correction as co
import toolbox_correction as tb_c


def sort_dataset(arg_population, arg_capacity_uv_promo_dict):
    # Sort the population by fitness
    list_fitness = [sl.fitness(chromosome, arg_capacity_uv_promo_dict) for chromosome in arg_population]
    sorted_list_fitness, sorted_index_population = sl.sorting_fitness(list_fitness, arg_population)
    sorted_population = [arg_population[i] for i in sorted_index_population]
    return sorted_list_fitness, sorted_population


def correction_all(arg_promo, arg_room_list, arg_population):
    # Convert room_list to a dictionary for faster access
    room_capacity_dict = {room.room: room.capacity for room in arg_room_list}
    capacity_uv_promo_dict = tb_c.calculate_nb_students_by_uv(arg_promo)
    # Correction of the initial population
    # Correction of the teacher
    for i in range(len(arg_population)):
        arg_population[i] = co.correction_teacher(arg_population[i])
    # Correction of the room
    for i in range(len(arg_population)):
        arg_population[i] = co.correction_room(arg_population[i], room_capacity_dict, arg_room_list,
                                               capacity_uv_promo_dict)
    return arg_population, room_capacity_dict, capacity_uv_promo_dict


def genetic_algorithm(arg_room_list, arg_population, arg_fitness, room_capacity_dict, capacity_uv_promo_dict,
                      generation=100,
                      mutation_rate=0.01, nb_couple_elite=1, selection_choice='elitiste',
                      crossover_choice='single_point',
                      arg_tournament_size=5, correction=True):
    """
    Returns the best chromosome and its fitness after a genetic algorithm.
    :param capacity_uv_promo_dict:
    :param room_capacity_dict:
    :param correction:
    :param arg_room_list:
    :param arg_population:
    :param arg_fitness:
    :param generation:
    :param mutation_rate:
    :param nb_couple_elite:
    :param selection_choice:
    :param crossover_choice:
    :param arg_tournament_size:
    :return:
    """

    # History
    history = []

    for _ in range(generation):
        # Selection
        index_parents = sl.selection_choice(arg_fitness, selection_choice, nb_couple_elite, arg_tournament_size)

        # Reproduction
        tableau_enfants = []
        for k in range(len(index_parents)):
            enfant_aux = cr.crossover_choice(arg_population[index_parents[k][0]],
                                             arg_population[index_parents[k][1]], crossover_choice)
            # Correction
            if correction:
                enfant_aux = co.correction_teacher(enfant_aux)
                enfant_aux = co.correction_room(enfant_aux, room_capacity_dict, arg_room_list, capacity_uv_promo_dict)
            tableau_enfants.append(enfant_aux)

        # Mutation
        for i in range(len(tableau_enfants)):
            if rd.random() < mutation_rate:
                aux_mutation = mt.random_mutation(tableau_enfants[i])
                # Correction
                if correction:
                    aux_mutation = co.correction_teacher(aux_mutation)
                    aux_mutation = co.correction_room(aux_mutation, room_capacity_dict, arg_room_list,
                                                      capacity_uv_promo_dict)
                tableau_enfants[i] = aux_mutation

        # Remplacement des pires chromosomes par les meilleurs enfants
        for i in range(len(tableau_enfants)):
            arg_fitness, arg_population = rp.replace(arg_fitness, arg_population,
                                                     sl.fitness(tableau_enfants[i], capacity_uv_promo_dict),
                                                     tableau_enfants[i])

        # History
        history.append(arg_fitness[0])

    # Selection du meilleur chromosome
    best_chromosome = arg_population[0]
    best_fitness = arg_fitness[0]

    print(arg_fitness)

    return best_chromosome, best_fitness, history
