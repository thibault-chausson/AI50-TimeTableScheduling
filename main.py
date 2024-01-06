import toolbox as tb
import benchmark as bm
import toolbox_student as tbs
import json


def import_json(path):
    """
    Import a json file
    :param path: path of the file
    :return: data
    """
    with open(path, 'r') as file:
        data = json.load(file)
    return data


def read_fitness(path):
    """
    Read the fitness from a file
    :param path: path of the file
    :return: list of fitness
    """
    fitness = []
    with open(path, 'r') as file:
        for line in file:
            fitness.append(float(line))
    return fitness


if __name__ == "__main__":
    """
    Parameters
    """
    NAME_TEST = "visuels_rapport"
    PATH_DATA = "./datas/instances/" + NAME_TEST

    GENERATION_NUMBER = 1000
    MUTATION_PROBABILITY = 0.08
    NUMBER_OF_COUPLES = 2
    CORRECTION = True

    """
    List of selection functions:
    - tournament_selection : 'tournoi'
    - roulette_wheel_selection : 'roulette'
    - selection_probabiliste : 'proba'
    - selection_elitiste : 'elitiste'

    List of crossover functions:
    - single_point_crossover : 'single_point'
    - two_points_crossover : 'two_points'
    - uniform_crossover : 'uniform'
    - ordered_crossover : 'order'
    """
    SELECT = 'roulette'
    CROSS = 'single_point'
    TOURNOI_SIZE = 3

    """
    Results
    """
    FILE_NAME_RESULTS = NAME_TEST
    TITLE_GRAPH = "Evolution of the fitness with \n correction and wheel selection,\n single point crossover"
    CREATE_SCHEDULE = True

    """
    Create a population and school year
    SITE = ["Belfort", "Sevenans", ...]
    FORMATION = ["FISE-INFO", "FISA-INFO", ...]
    """
    SITE = ["Belfort"]
    FORMATION = ["FISE-INFO"]
    POPULATION_SIZE = 100
    PROMO_SIZE = 100
    NUMBERS_UV = 20
    EXPORT_PATH_INSTANCES = PATH_DATA
    EXPORT_INSTANCES = False

    room_list = []
    for ville in SITE:
        room_list = room_list + tb.get_rooms(ville)  # UTBM data
    uvs_list = []
    for formation in FORMATION:
        uvs_list = uvs_list + tb.get_uvs(formation)  # UTBM data

    """
    To limit the number of uvs
    """
    uvs_list = uvs_list[:NUMBERS_UV]

    """
    pop, fit, promo, room_capa, uv_promo_capa = gi.get_instance(SITE, FORMATION, POPULATION_SIZE,
                                                                PROMO_SIZE, room_list, uvs_list, EXPORT_PATH_INSTANCES,
                                                                EXPORT_INSTANCES)
    """
    """
    Import data
    """

    """
    Run the benchmark
    """
    history_fitness = []
    history_time = []

    for i in range(1):
        print("Test n°", i + 1)
        promo = tbs.import_promo(PATH_DATA + "/promo.json")  # Own data
        pop = tb.import_population(PATH_DATA + "/population.json")  # Own data
        fit = read_fitness(PATH_DATA + "/fitness_of_the_population.txt")  # Own data
        room_capa = import_json(PATH_DATA + "/capacity_of_the_rooms.json")  # UTBM data reworked
        uv_promo_capa = import_json(PATH_DATA + "/capacity_of_the_uvs_promo.json")  # Own data estimated

        best_fitness, time = bm.benchmark(promo, room_list, pop, fit, room_capa, uv_promo_capa, uvs_list,
                                          GENERATION_NUMBER, MUTATION_PROBABILITY, NUMBER_OF_COUPLES, SELECT,
                                          CROSS, TOURNOI_SIZE, CORRECTION, TITLE_GRAPH, FILE_NAME_RESULTS,
                                          CREATE_SCHEDULE)
        history_fitness.append(best_fitness)
        history_time.append(time)

    # Print the average fitness
    print("Average fitness: ", round(sum(history_fitness) / len(history_fitness), 2))
    print("Average time: ", round(sum(history_time) / len(history_time), 2))
