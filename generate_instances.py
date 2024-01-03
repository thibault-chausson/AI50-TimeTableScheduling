from toolbox_student import *
from toolbox import *
from initial_population import *

def get_instance(sites, formations, pop_size, promo_size, export=False):
    """
    Generates the population and the promo from the given sites and formations
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

    population = generate_population(pop_size, uvs, rooms)
    promo = create_promo(uvs, promo_size)

    if export:
        export_population(population, "./datas/population.json")
        export_promo(promo, "./datas/promo.json")
    else:
        return population, promo


if __name__ == '__main__':
    pop, promo = get_instance(["Belfort", "Sevenans"], ["FISE-INFO", "FISA-INFO"], 10, 20, export=False)