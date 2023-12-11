import random as rd
import selection as sl
import crossover as cr
import mutation as mt
import replace as rp


def set_dataset(arg_population):
    # Trier la population par score du meilleur au pire
    list_fitness = [sl.fitness(chromosome) for chromosome in arg_population]
    sorted_list_fitness, sorted_index_population = sl.sorting_fitness(list_fitness, arg_population)
    sorted_population = [arg_population[i] for i in sorted_index_population]
    return sorted_list_fitness, sorted_population


def genetic_algorithm_single_point_elite(uvs_fct, promo_fct, arg_population, arg_fitness, generation=100,
                                         mutation_rate=0.01, nb_couple_elite=1):
    for _ in range(generation):
        # Selection
        index_parents = sl.selection_elitiste(nb_couple_elite)

        # Reproduction
        tableau_enfants = []
        for k in range(len(index_parents)):
            tableau_enfants.append(cr.single_point_crossover(arg_population[index_parents[k][0]],
                                                             arg_population[index_parents[k][1]]))

        # Correction

        # Mutation
        for i in range(len(tableau_enfants)):
            if rd.random() < mutation_rate:
                tableau_enfants[i] = mt.mutation_test(tableau_enfants[i])

        # Correction

        # Remplacement des pires chromosomes par les meilleurs enfants
        for i in range(len(tableau_enfants)):
            arg_fitness, arg_population = rp.replace(arg_fitness, arg_population,
                                                     sl.fitness(tableau_enfants[i]), tableau_enfants[i])

    # Selection du meilleur chromosome
    best_chromosome = arg_population[0]
    best_fitness = arg_fitness[0]

    print(arg_fitness)

    return best_chromosome, best_fitness
