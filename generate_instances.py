from toolbox_student import *
from initial_population import *
import toolbox as tb
import os
import genetique as gen
import json


def get_instance(sites, formations, pop_size, promo_size, export_path='./datas/instances/coucou', export=False):
    """
    Generates the population and the promo from the given sites and formations
    :param export_path:
    :param sites: list of sites
    :param formations: list of formations
    :param pop_size: size of the population
    :param promo_size: size of the promo
    :param export: if True, exports the population and the promo in json files, to ./datas/population.json and ./datas/promo.json
    :return: (population, promo)
    """
    rooms = []
    for site in sites:
        rooms.extend(get_rooms(site))
    uvs = []
    for formation in formations:
        uvs.extend(get_uvs(formation))
    uvs = [i for i in uvs if i.teachers != [None]]

    list_uv = []
    for uv in uvs:
        list_uv.append(uv.code)

    population = generate_population(pop_size, uvs, rooms)
    # Sort the population and the fitness
    fitness_sorted, population = gen.sort_dataset(population)

    promo = create_promo(list_uv, promo_size)

    # Correct the population
    room_list = tb.get_rooms()
    population, room_capacity_dict, capacity_uv_promo_dict = gen.correction_all(promo, room_list, population)

    if export:
        if not os.path.exists(export_path):
            os.makedirs(export_path)
        export_population(population, export_path + "/population.json")
        export_promo(promo, export_path + "/promo.json")
        # Save the capacity of the rooms
        with open(export_path + '/capacity_of_the_rooms.json', 'w') as file:
            json.dump(room_capacity_dict, file)

        # Save the capacity of the uvs
        with open(export_path + '/capacity_of_the_uvs.json', 'w') as file:
            json.dump(capacity_uv_promo_dict, file)

    return population, promo, room_capacity_dict, capacity_uv_promo_dict


if __name__ == '__main__':
    pop, promo, room_capa, uv_capa = get_instance(["Belfort", "Sevenans"], ["FISE-INFO", "FISA-INFO"], 10, 20,
                                                  export_path='./datas/instances/coucou',
                                                  export=True)
