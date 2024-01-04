import random
from toolbox import *  # The global variables in tooblox.py will also be imported.
import variables as var


def get_individual(uv_info, rooms, search_cap=100, room_usage=0.4):
    """
    Returns a chromosome that has no overlaps between rooms, teachers and uvs.
    """
    chromosome = []
    room_index = 0
    counter = 0

    uvs = uv_info.copy()
    random.shuffle(uvs)
    rooms = rooms.copy()
    random.shuffle(rooms)

    for idx, uv in enumerate(uvs):
        for course_type, time in zip(("cm", "td", "tp"), (uv.cm, uv.td, uv.tp)):
            if time == 0:
                continue

            done = False
            while not done:
                steps = int(np.ceil(time / var.WEEKS / var.MINUTES_PER_CELL))
                teacher = random.choice(uv.teachers)
                print(f"uv: {idx}/{len(uvs)},\t salle: {room_index}/{len(rooms)}", end="\r")
                room = rooms[room_index]
                planning_r = planning_room(chromosome, room.room)
                planning_t = planning_teacher(chromosome, teacher)
                planning_u = planning_uv(chromosome, uv.code)
                if (planning_r.sum() >= planning_r.shape[0] * planning_r.shape[1] * room_usage) or (
                        counter >= search_cap - 1):
                    room_index += 1
                    room = rooms[room_index]
                    planning_r = planning_room(chromosome, room.room)
                    if room_index >= len(rooms):
                        raise Exception("No more rooms available. Maybe increase room usage ?")

                start_time = random.randint(0, planning_r.shape[0] - steps)
                start_day = random.randint(0, planning_r.shape[1] - 1)
                counter = 0
                # Making sure that there are no overlaps between rooms, teachers and uvs.
                while (planning_r[start_time:start_time + steps, start_day] + planning_t[start_time:start_time + steps,
                                                                              start_day] + planning_u[
                                                                                           start_time:start_time + steps,
                                                                                           start_day]).sum() != 0:
                    counter += 1
                    if counter == search_cap:
                        break
                    start_time = random.randint(0, planning_r.shape[0] - steps)
                    start_day = random.randint(0, planning_r.shape[1] - 1)

                if counter < search_cap:
                    done = True

            gene = Gene(room.room, var.START_TIME + start_time * var.MINUTES_PER_CELL, start_day,
                        steps * var.MINUTES_PER_CELL,
                        teacher, uv.code, course_type)
            chromosome.append(gene)

    print()
    return chromosome


def generate_population(nb_individu, uvs_fct, rooms_fct):
    population_fct = []
    for _ in range(nb_individu):
        population_fct.append(get_individual(uvs_fct, rooms_fct))
    return population_fct


if __name__ == '__main__':
    rooms = get_rooms("Belfort")
    uvs = get_uvs("FISE-INFO")
    uvs = [i for i in uvs if
           i.teachers != [None]]  # Pas de profs pour une UV crée un bug dans la fonction planning_teacher

    # chromosome = get_individual(uvs, rooms)

    # export_population([chromosome], "chromosome.json")

    population = generate_population(10, uvs, rooms)
    export_population(population, "datas/population_new.json")
