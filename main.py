import genetique as gen
import toolbox as tb
import toolbox_student as tbs
import time as t
import benchmark as bm

if __name__ == "__main__":
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

    start_data = t.time()
    uvs = tb.import_uvs("datas/uvs.json")
    promo = tbs.import_promo("datas/promo.json")
    population = tb.import_population("datas/population.json")
    sorted_fitness, sorted_population = gen.sort_dataset(population)
    room_list = tb.get_rooms()
    end_data = t.time()
    print("Data loading time: ", end_data - start_data)

    bm.benchmark(promo, room_list, population, sorted_fitness, 10,
                 0.2, 1, 'roulette',
                 'single_point', 5, True, sorted_fitness, sorted_population,
                 "Evolution of the fitness with \n correction and wheel selection,\n single point crossover",
                 "schedule1")
