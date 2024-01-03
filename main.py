import genetique as gen
import toolbox as tb
import toolbox_student as tbs
import time as t
import matplotlib.pyplot as plt


def benchmark(arg_promo, arg_room_list, arg_population, arg_fitness, generation,
              mutation_rate, nb_couple_elite, selection_choice, crossover_choice,
              arg_tournament_size, correction, title="Evolution of the fitness"):
    print("Best fitness before: ", sorted_fitness)
    print("Best chromosome before: ", sorted_population[0])
    start_algo = t.time()
    chromosome, fitness, history = gen.genetic_algorithm(arg_promo, arg_room_list, arg_population, arg_fitness,
                                                         generation, mutation_rate, nb_couple_elite, selection_choice,
                                                         crossover_choice, arg_tournament_size, correction)
    end_algo = t.time()

    # Graphic representation
    plt.plot(history)
    plt.xlabel("Generations")
    plt.ylabel("Fitness")
    plt.title(title)
    plt.text(x=0.1, y=0.1,
             s=f"Best fitness: {str(fitness)}, Algorithm execution time: {round(end_algo - start_algo, 5)}s",
             fontsize=10, transform=plt.gca().transAxes)
    plt.show()

    print("Best fitness after: ", fitness)
    print("Best chromosome after: ", chromosome)


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
    sorted_fitness, sorted_population = gen.set_dataset(population)
    room_list = tb.get_rooms()
    end_data = t.time()
    print("Data loading time: ", end_data - start_data)

    benchmark(promo, room_list, population, sorted_fitness, 10,
              0.2, 1, 'roulette',
              'single_point', 5, True,
              "Evolution of the fitness with correction and wheel selection, single point crossover")
