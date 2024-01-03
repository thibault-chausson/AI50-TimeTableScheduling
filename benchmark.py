import matplotlib.pyplot as plt
import os
import time as t
import genetique as gen
import toolbox as tb
import toolbox_student as tb_s
import schedule as sc


def benchmark(arg_promo, arg_room_list, arg_population, arg_fitness, generation,
              mutation_rate, nb_couple_elite, selection_choice, crossover_choice,
              arg_tournament_size, correction, sorted_fitness, sorted_population, title="Evolution of the fitness",
              filename="schedule"):
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

    print("Best fitness after: ", fitness)
    print("Best chromosome after: ", chromosome)

    # Create results folder if it doesn't exist
    if not os.path.exists('results/' + filename):
        os.makedirs('results/' + filename)

    # Save the best chromosome
    tb.export_chr(chromosome, f"results/{filename}/{filename}.json")

    # Save plot
    plt.savefig(f"results/{filename}/{filename}.png", dpi=300)

    plt.show()

    # Create schedule
    if not os.path.exists('results/' + filename + '/schedule_all_uv'):
        os.makedirs('results/' + filename + '/schedule_all_uv')

    create_schedule_all(chromosome, 'uv', filename)


def create_schedule_all(chr, promo, type_schedule, filename):
    """
    Create a schedule for all UVs in the chromosome.
    """
    if type_schedule == 'uv':
        data_chr = tb_s.get_all_uvs_chromosome(chr)
        kind = "uv"
    elif type_schedule == 'teacher':
        data_chr = tb_s.get_all_teacher_chromosome(chr)
        kind = "teacher"
    elif type_schedule == 'room':
        data_chr = tb_s.get_all_room_chromosome(chr)
        kind = "room"
    elif type_schedule == 'student':
        data_chr = tb_s.get_all_student_promo(promo)
        kind = "student"
    else:
        print("Error: type_schedule must be 'uv' or 'teacher'")
        return

    for data in data_chr:
        key = data
        chr = sc.get_genes_from(chr, kind, key)
        mat = sc.get_classes_mat(chr)
        sc.make_schedule(mat, chr, kind, key, 'results/' + filename + '/schedule_all_uv/' + key + '.png')