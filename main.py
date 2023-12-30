import genetique as gen
import toolbox as tb
import toolbox_student as tbs
import time as t

if __name__ == "__main__":
    start_data = t.time()
    uvs = tb.import_uvs("datas/uvs.json")
    promo = tbs.import_promo("datas/promo.json")
    population = tb.import_population("datas/population.json")
    sorted_fitness, sorted_population = gen.set_dataset(population)
    room_list = tb.get_rooms()
    print("Best fitness before: ", sorted_fitness)
    end_data = t.time()
    print("Data loading time: ", end_data - start_data)
    start_algo = t.time()
    chromosome, fitness = gen.genetic_algorithm_single_point_elite(promo, room_list, population, sorted_fitness, 100,
                                                                   0.2, 1)
    end_algo = t.time()
    print("Algorithm execution time: ", end_algo - start_algo)

    print(chromosome, fitness)
