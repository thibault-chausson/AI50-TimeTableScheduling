import matplotlib.pyplot as plt
import os
import time as t
import genetique as gen
import toolbox as tb
import toolbox_student as tb_s
import schedule as sc


def create_directory(path):
    """Crée un répertoire s'il n'existe pas."""
    if not os.path.exists(path):
        os.makedirs(path)


def benchmark(arg_promo, arg_room_list, arg_population, arg_fitness, arg_room_capacity_dict, arg_capacity_uv_promo_dict,
              generation,
              mutation_rate, nb_couple_elite, selection_choice, crossover_choice,
              arg_tournament_size, correction,
              title="Evolution of the fitness", filename="schedule", schedule=False):
    print("Best fitness before: ", arg_fitness)
    print("Best chromosome before: ", arg_population[0])
    start_algo = t.time()

    chromosome, fitness, history = gen.genetic_algorithm(arg_room_list, arg_population, arg_fitness,
                                                         arg_room_capacity_dict, arg_capacity_uv_promo_dict,
                                                         generation, mutation_rate, nb_couple_elite, selection_choice,
                                                         crossover_choice, arg_tournament_size, correction)
    end_algo = t.time()

    # Représentation graphique
    plt.plot(history)
    plt.xlabel("Generations")
    plt.ylabel("Fitness")
    plt.title(title)
    plt.text(x=0.1, y=0.1,
             s=f"Best fitness: {str(fitness)}, Algorithm execution time: {round(end_algo - start_algo, 5)}s",
             fontsize=10, transform=plt.gca().transAxes)

    print("Best fitness after: ", fitness)
    print("Best chromosome after: ", chromosome)

    # Création du dossier de résultats
    results_path = f'results/{filename}'
    create_directory(results_path)

    # Sauvegarde du meilleur chromosome et du graphique
    tb.export_chr(chromosome, f"{results_path}/{filename}.json")
    plt.savefig(f"{results_path}/{filename}.png", dpi=300)
    plt.show()

    if schedule:
        print("Creating schedules...")
        # Création des emplois du temps
        for schedule_type in ['uv', 'teacher', 'room', 'student']:
            schedule_folder = f'{results_path}/schedule_all_{schedule_type}'
            create_directory(schedule_folder)
            create_schedule_all(chromosome, arg_promo, schedule_type, filename)
        print("Schedules created.")


def create_schedule_all(chr, promo, type_schedule, filename):
    """
    Create a schedule for all UVs in the chromosome.
    """
    if type_schedule == 'uv':
        data_chr = tb_s.get_all_uvs_chromosome(chr)
        kind = "uv"
        folder = "schedule_all_uv"
    elif type_schedule == 'teacher':
        data_chr = tb_s.get_all_teacher_chromosome(chr)
        kind = "teacher"
        folder = "schedule_all_teacher"
    elif type_schedule == 'room':
        data_chr = tb_s.get_all_room_chromosome(chr)
        kind = "room"
        folder = "schedule_all_room"
    elif type_schedule == 'student':
        data_chr = tb_s.get_all_student_promo(promo)
        kind = "student"
        folder = "schedule_all_student"
    else:
        print("Error: type_schedule must be 'uv' or 'teacher'")
        return

    for data in data_chr:
        key = data
        chr = sc.get_genes_from(chr, kind, key)
        mat = sc.get_classes_mat(chr)
        if type_schedule == 'student':
            key = key.name
        sc.make_schedule(mat, chr, kind, key, 'results/' + filename + '/' + folder + '/' + key + '.png')
