import toolbox as tb
from fitness import fitness
import selection as sl


def normalize(arg_list_fitness, arg_fitness_child):
    # Normalize the fitness list
    max_fitness = max(max(arg_list_fitness), arg_fitness_child)
    min_fitness = min(min(arg_list_fitness), arg_fitness_child)
    normalized_list_fitness = [(fitness_boucle - min_fitness) / (max_fitness - min_fitness) for fitness_boucle in
                               arg_list_fitness]
    # Calculate the fitness of the child
    normalized_fitness_child = (arg_fitness_child - min_fitness) / (max_fitness - min_fitness)
    normalized_list_fitness.pop()
    return normalized_list_fitness, normalized_fitness_child


def insertion_dichotomique(arr, x):
    debut, fin = 0, len(arr)
    while debut < fin:
        milieu = (debut + fin) // 2
        if arr[milieu] < x:
            fin = milieu
        else:
            debut = milieu + 1
    return debut


# http://serge.mehl.free.fr/anx/insertion_dichoto.html
def replace(arg_list_fitness, population, arg_fitness_child, arg_child):
    if arg_fitness_child > arg_list_fitness[-1]:
        # Vérifier si le chromosome n'est pas déjà dans la population
        if not (arg_fitness_child in arg_list_fitness):
            # Remove the worst chromosome
            arg_list_fitness.pop()
            # Remove the worst chromosome
            population.pop()
            # Normalize the fitness list
            # n_list_fitness, n_fitness_child = normalize(arg_list_fitness, arg_fitness_child)
            # Dichotomic search to insert the new chromosome
            index = insertion_dichotomique(arg_list_fitness, arg_fitness_child)
            # Insert the new chromosome
            arg_list_fitness.insert(index, arg_fitness_child)
            # Insert the new chromosome
            population.insert(index, arg_child)
    return arg_list_fitness, population


if __name__ == "__main__":
    initial_population = tb.import_population("datas/population.json")
    list_fitness = [fitness(chromosome) for chromosome in initial_population]
    print(f"Fitness : {list_fitness} \n")

    # import chromosome_1
    child = tb.import_population("datas/chromosome_1.json")[0]
    fitness_child = -300
    print(f"Fitness child : {fitness_child} \n")

    sorted_list_fitness, sorted_index_population = sl.sorting_fitness(list_fitness, initial_population)
    print(f"Sorted fitness : {sorted_list_fitness} \n")
    print(f"Sorted index population : {sorted_index_population} \n")
    sorted_initial_population = [initial_population[i] for i in sorted_index_population]

    list_fitness_replace, population_replace = replace(sorted_list_fitness, sorted_initial_population, fitness_child,
                                                       child)
    print(f"Replace : {list_fitness_replace} \n")
