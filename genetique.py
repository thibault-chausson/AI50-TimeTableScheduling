import random as rd


def genetic_algorithm_single_point_elite(uvs_fct, promo_fct, population_fct, generation=100, elite_size=10,
                                         mutation_rate=0.01):
    # Trier la population par score du meilleur au pire

    for _ in range(generation):
        # Selection
        tableau_parents = []

        # Reproduction
        tableau_enfants = []
        for k in range(len(tableau_parents)):
            tableau_enfants.append([])

        # Correction

        # Mutation
        for i in range(len(tableau_enfants)):
            if rd.random() < mutation_rate:
                tableau_enfants[i] = "moi"

        # Correction

        # Remplacement des pires chromosomes par les meilleurs enfants

    # Selection du meilleur chromosome
    best_chromosome = "moi"

    return best_chromosome
