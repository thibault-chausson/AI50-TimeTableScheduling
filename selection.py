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


def sorting_fitness(arg_list_fitness, arg_initial_population):
    """
    Returns a sorted fitness and population list
    """

    # Sort population list according to its fitness
    classement = sorted(range(len(arg_initial_population)), key=lambda i: arg_list_fitness[i], reverse=True)
    # print(f"Classement : {classement} \n")

    # sorted_initial_population = [initial_population[i] for i in classement]
    fct_sorted_list_fitness = sorted(arg_list_fitness, reverse=True)

    return fct_sorted_list_fitness, classement


def tournament_selection(arg_sorted_list_fitness, t_size, nb_couple):  # t_size >= nb_couple * 2
    tournoi = rd.sample(range(len(arg_sorted_list_fitness)),
                        t_size)  # On choisit t_size individus au hasard à savoir que l'indice 0 est la meilleure fitness
    tournoi.sort()  # On trie les indices du tournoi dans l'ordre croissant
    list_index_parents = tournoi[:nb_couple * 2]  # On prend les nb_couple * 2 premiers indices du tournoi
    # Shuffle the list
    rd.shuffle(list_index_parents)

    return create_couples(list_index_parents, nb_couple)


def roulette_wheel_selection(arg_list_fitness, nb_couple):
    """
    Spin the wheel by selecting a random point on the wheel and then moving through the individuals in the population, accumulating fitness until the selected point is reached or exceeded. 
    The corresponding individual is then chosen as parent.
    """
    total_fitness = sum(arg_list_fitness)

    proba_list = [fitness_chr / total_fitness for fitness_chr in arg_list_fitness]
    parents = []

    # Spin the wheel
    for _ in range(nb_couple * 2):
        spin = rd.random()
        fitness_sum = 0
        for i in range(len(proba_list)):
            fitness_sum += proba_list[i]
            if fitness_sum >= spin:
                parents.append(i)
                break

    return create_couples(parents, nb_couple)


def selection_elitiste(nb_couple):
    """
    Returns the best individuals
    """
    indices_elite = [i for i in range(nb_couple * 2)]

    return create_couples(indices_elite, nb_couple)


def selection_probabiliste(arg_list_fitness, nb_couple):
    inverted_fitness = [1 / value for value in arg_list_fitness]
    total_inverted_fitness = np.sum(inverted_fitness)

    # Proba de choisir un individu 
    probabilites = [inverted_fitness[i] / total_inverted_fitness for i in range(len(arg_list_fitness))]
    # print(probabilités)
    # print(sum(probabilités))

    index_population = [i for i in range(len(arg_list_fitness))]
    # Choisissez nb_couple de parents en fonction des probabilités
    index_parents = rd.choices(index_population, weights=probabilites, k=nb_couple * 2)

    return create_couples(index_parents, nb_couple)


def selection_choice(arg_sorted_list_fitness, arg_selection_choice, arg_nb_couple=1, arg_tournament_size=5):
    """
    Choose the selection method
    :param arg_sorted_list_fitness:
    :param arg_selection_choice:
    :param arg_nb_couple:
    :param arg_tournament_size:
    :return:
    """
    if arg_selection_choice == "elitiste":
        return selection_elitiste(arg_nb_couple)
    elif arg_selection_choice == "tournoi" and arg_tournament_size >= arg_nb_couple * 2:
        return tournament_selection(arg_sorted_list_fitness, arg_tournament_size, arg_nb_couple)
    elif arg_selection_choice == "roulette":
        return roulette_wheel_selection(arg_sorted_list_fitness, arg_nb_couple)
    elif arg_selection_choice == "proba":
        return selection_probabiliste(arg_sorted_list_fitness, arg_nb_couple)
    else:
        print("Error: selection_choice()")
