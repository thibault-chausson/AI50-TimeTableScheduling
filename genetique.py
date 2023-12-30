import random as rd
import selection as sl
import crossover as cr
import mutation as mt
import replace as rp
import correction as co
import toolbox_correction as tb_c


def set_dataset(arg_population):
    # Trier la population par score du meilleur au pire
    list_fitness = [sl.fitness(chromosome) for chromosome in arg_population]
    sorted_list_fitness, sorted_index_population = sl.sorting_fitness(list_fitness, arg_population)
    sorted_population = [arg_population[i] for i in sorted_index_population]
    return sorted_list_fitness, sorted_population


def genetic_algorithm_single_point_elite(arg_promo, arg_room_list, arg_population, arg_fitness, generation=100,
                                         mutation_rate=0.01, nb_couple_elite=1):
    # Convert room_list to a dictionary for faster access
    room_capacity_dict = {room.room: room.capacity for room in arg_room_list}
    capacity_uv_promo_dict = tb_c.calculate_nb_students_by_uv(arg_promo)
    # Corriger la population initiale
    for i in range(len(arg_population)):
        arg_population[i] = co.correction_room(arg_population[i], room_capacity_dict, arg_room_list, capacity_uv_promo_dict)

    for _ in range(generation):
        # Selection
        index_parents = sl.selection_elitiste(nb_couple_elite)

        # Reproduction
        tableau_enfants = []
        for k in range(len(index_parents)):
            enfant_aux = cr.single_point_crossover(arg_population[index_parents[k][0]],
                                                   arg_population[index_parents[k][1]])
            # Correction
            enfant_aux = co.correction_room(enfant_aux, room_capacity_dict, arg_room_list, capacity_uv_promo_dict)
            tableau_enfants.append(enfant_aux)

        # Mutation
        for i in range(len(tableau_enfants)):
            if rd.random() < mutation_rate:
                aux_mutation = mt.random_mutation(tableau_enfants[i])
                # Correction
                aux_mutation = co.correction_room(aux_mutation, room_capacity_dict, arg_room_list,
                                                  capacity_uv_promo_dict)
                tableau_enfants[i] = aux_mutation

        # Remplacement des pires chromosomes par les meilleurs enfants
        for i in range(len(tableau_enfants)):
            arg_fitness, arg_population = rp.replace(arg_fitness, arg_population,
                                                     sl.fitness(tableau_enfants[i]), tableau_enfants[i])

    # Selection du meilleur chromosome
    best_chromosome = arg_population[0]
    best_fitness = arg_fitness[0]

    print(arg_fitness)

    return best_chromosome, best_fitness
