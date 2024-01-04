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
    PATH_DATA = "./datas/instances/coucou"

    GENERATION_NUMBER = 10
    MUTATION_PROBABILITY = 0.2
    NUMBER_OF_COUPLES = 1
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
    TOURNOI_SIZE = 5

    """
    Results
    """
    FILE_NAME_RESULTS = "schedule1"
    TITLE_GRAPH = "Evolution of the fitness with \n correction and wheel selection,\n single point crossover"
    CREATE_SCHEDULE = False

    """
    Create a population and school year
    """
    """
    pop, fit, promo, room_capa, uv_promo_capa = gi.get_instance(["Belfort", "Sevenans"], ["FISE-INFO", "FISA-INFO"], 10,
                                                                20,
                                                                export_path='./datas/instances/coucou',
                                                                export=True)
    """

    """
    Import data
    """
    room_list = tb.get_rooms()  # UTBM data
    promo = tbs.import_promo(PATH_DATA + "/promo.json")  # Own data
    pop = tb.import_population(PATH_DATA + "/population.json")  # Own data
    fit = read_fitness(PATH_DATA + "/fitness_of_the_population.txt")  # Own data
    room_capa = import_json(PATH_DATA + "/capacity_of_the_rooms.json")  # UTBM data reworked
    uv_promo_capa = import_json(PATH_DATA + "/capacity_of_the_uvs_promo.json")  # Own data estimated

    """
    Run the benchmark
    """
    bm.benchmark(promo, room_list, pop, fit, room_capa, uv_promo_capa, GENERATION_NUMBER, MUTATION_PROBABILITY,
                 NUMBER_OF_COUPLES, SELECT, CROSS, TOURNOI_SIZE, CORRECTION, TITLE_GRAPH, FILE_NAME_RESULTS,
                 CREATE_SCHEDULE)
