import random as rd
import numpy as np
import toolbox as tb
from fitness import fitness


def create_couples(liste, n):
    # Utilisation de zip pour créer des couples
    couples = list(zip(liste[0::2], liste[1::2]))

    # Récupération des n premiers couples
    premiers_couples = couples[:n]

    return premiers_couples


def sorting_fitness(list_fitness, initial_population):
    """
    Returns a sorted fitness and population list
    """

    # Sort population list according to its fitness
    classement = sorted(range(len(initial_population)), key=lambda i: list_fitness[i], reverse=True)
    # print(f"Classement : {classement} \n")

    # sorted_initial_population = [initial_population[i] for i in classement]
    sorted_list_fitness = sorted(list_fitness, reverse=True)

    return sorted_list_fitness, classement


def tournament_selection(sorted_list_fitness, sorted_index_population, t_size, nb_couple):  # t_size >= nb_couple * 2
    tournoi = rd.sample(range(len(sorted_list_fitness)),
                        t_size)  # On choisit t_size individus au hasard à savoir que l'indice 0 est la meilleure fitness
    tournoi.sort()  # On trie les indices du tournoi dans l'ordre croissant
    print(f"Tournoi : {tournoi} \n")
    list_index_parents = []
    for i in range(0, t_size):
        list_index_parents.append(sorted_index_population[tournoi[i]])

    return create_couples(list_index_parents, nb_couple)


def roulette_wheel_selection(index_population, list_fitness, nb_couple):
    """
    Spin the wheel by selecting a random point on the wheel and then moving through the individuals in the population, accumulating fitness until the selected point is reached or exceeded. 
    The corresponding individual is then chosen as parent.
    """
    total_fitness = sum(list_fitness)
    parents = []
    for _ in range(nb_couple * 2):
        roulette_spin = rd.uniform(0, total_fitness)

        cumul_fitness = 0
        for i, fitness_individu in enumerate(list_fitness):
            cumul_fitness += fitness_individu
            if cumul_fitness <= roulette_spin:
                # Pour eviter d'avoir les meme parents
                if index_population[i] not in parents:
                    parents.append(index_population[i])
                else:
                    parents.append(index_population[i - 1])
                break

    return create_couples(parents, nb_couple)


def selection_elitiste(index_population, nb_couple):
    """
    Returns the best individuals
    """
    indices_elite = index_population[:nb_couple * 2]

    return create_couples(indices_elite, nb_couple)


def selection_probabiliste(index_population, list_fitness, nb_couple):
    inverted_fitness = [1 / value for value in list_fitness]
    total_inverted_fitness = np.sum(inverted_fitness)

    # Proba de choisir un individu 
    probabilites = [inverted_fitness[i] / total_inverted_fitness for i in range(len(index_population))]
    # print(probabilités)
    # print(sum(probabilités))

    # Choisissez nb_couple de parents en fonction des probabilités
    index_parents = rd.choices(index_population, weights=probabilites, k=nb_couple * 2)

    return create_couples(index_parents, nb_couple)


if __name__ == "__main__":
    initial_population = tb.import_population("datas/population.json")
    list_fitness = [fitness(chromosome) for chromosome in initial_population]
    print(f"Fitness : {list_fitness} \n")

    sorted_list_fitness, sorted_index_population = sorting_fitness(list_fitness, initial_population)
    print(f"Sorted fitness : {sorted_list_fitness} \n")
    print(f"Sorted index population : {sorted_index_population} \n")

    print(f"Roulette wheel : {roulette_wheel_selection(sorted_index_population, sorted_list_fitness, 3)} \n")
    print(f"Elites : {selection_elitiste(sorted_index_population, 2)} \n")
    print(f"Selection proba : {selection_probabiliste(sorted_index_population, sorted_list_fitness, 2)} \n")

    # sorted_initial_population = [initial_population[i] for i in sorted_index_population]
    print(f"Tournoi : {tournament_selection(sorted_list_fitness, sorted_index_population, 5, 2)} \n")

    print("Done.")
