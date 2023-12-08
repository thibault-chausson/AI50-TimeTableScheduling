import genetique as gen
import toolbox as tb
import toolbox_student as tbs

if __name__ == "main":
    uvs = tb.import_uvs("uvs.json")
    promo = tbs.import_promo("promo.json")
    population = tb.import_population("population.json")
    res = gen.genetic_algorithm_single_point_elite(uvs, promo, population, 100, 10, 0.01)

    print(res)
