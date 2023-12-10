import random as rd
import numpy as np
import toolbox as tb
from fitness import fitness


def sorting_fitness(list_fitness, initial_population):
    """
    Returns a sorted fitness and population list
    """

    #Sort population list according to its fitness
    classement = sorted(range(len(initial_population)), key=lambda i: list_fitness[i], reverse=True)
    print(f"Classement : {classement} \n")

    #sorted_initial_population = [initial_population[i] for i in classement]
    sorted_list_fitness = sorted(list_fitness, reverse=True)

    return sorted_list_fitness, classement;


def tournament_selection(population, t_size, nb_couple):
    
    tournoi = rd.sample(population, t_size)
    fitness_tournoi =  np.array([fitness(schedule) for schedule in tournoi])
    indices = np.flip(np.argsort(fitness_tournoi))
    #indice des individus selectionnés 
    parents = [ind for ind, chrom in enumerate(population) for i in indices if tournoi[i] == chrom]

    return parents[:nb_couple*2]


def roulette_wheel_selection(index_population, list_fitness, nb_couple):
    """
    Spin the wheel by selecting a random point on the wheel and then moving through the individuals in the population, accumulating fitness until the selected point is reached or exceeded. 
    The corresponding individual is then chosen as parent.
    """
    total_fitness = sum(list_fitness)
    parents = []
    for _ in range(nb_couple*2):
        roulette_spin = rd.uniform(0, total_fitness)

        cumul_fitness = 0
        for i, fitness_individu in enumerate(list_fitness):
            cumul_fitness += fitness_individu
            if cumul_fitness <= roulette_spin:
                #Pour eviter d'avoir les meme parents
                if(index_population[i] not in parents):
                    parents.append(index_population[i])
                else:
                    parents.append(index_population[i-1])
                break
        
    return parents

def selection_elitiste(index_population, nb_couple):
    """
    Returns the best individuals
    """
    indices_elite = index_population[:nb_couple*2]

    return indices_elite


def selection_probabiliste(index_population, list_fitness, nb_couple):
    inverted_fitness = [1/value for value in list_fitness]
    total_inverted_fitness = np.sum(inverted_fitness)
    
    # Proba de choisir un individu 
    probabilités = [inverted_fitness[i] / total_inverted_fitness for i in range(len(index_population))]
    #print(probabilités)
    #print(sum(probabilités))

    # Choisissez nb_couple de parents en fonction des probabilités
    index_parents = rd.choices(index_population, weights=probabilités, k=nb_couple*2)
    
    return index_parents



if __name__ == "__main__":

    initial_population = tb.import_population("datas/population.json")    
    list_fitness = [fitness(chromosome) for chromosome in initial_population]
    print(f"Fitness : {list_fitness} \n")

    sorted_list_fitness, sorted_index_population = sorting_fitness(list_fitness, initial_population)

    print(f"Roulette wheel : {roulette_wheel_selection(sorted_index_population, sorted_list_fitness, 2)} \n")
    print(f"Elites : {selection_elitiste(sorted_index_population, 2)} \n")
    print(f"Selection proba : {selection_probabiliste(sorted_index_population, sorted_list_fitness, 2)} \n")

    sorted_initial_population = [initial_population[i] for i in sorted_index_population]
    print(f"Tournoi : {tournament_selection(sorted_initial_population, 8, 2)} \n")

    

    print("Done.")


