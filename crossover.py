import toolbox as tb
import random as rd

CHROMOSOME_1 = tb.import_population("datas/chromosome_1.json")[0]
CHROMOSOME_2 = tb.import_population("datas/chromosome_2.json")[0]


# Midpoint crossover

def single_point_crossover(chr1, chr2):
    """
    Returns a new chromosome created by crossing over two chromosomes.
    """
    middle = rd.randint(0, len(chr1))
    return chr1[:middle] + chr2[middle:]


# Two points crossover

def two_points_crossover(chr1, chr2):
    """
    Returns a new chromosome created by crossing over two chromosomes.
    """
    middle1 = rd.randint(0, len(chr1))
    middle2 = rd.randint(0, len(chr1))
    return chr1[:middle1] + chr2[middle1:middle2] + chr1[middle2:]


# Uniform crossover

def uniform_crossover(chr1, chr2):
    """
    Returns a new chromosome created by crossing over two chromosomes.
    """
    child_chr = []
    for i in range(len(chr1)):
        if rd.randint(0, 1) == 0:  # 0 means we take the gene from chr1 like "Heads or tails?"
            child_chr.append(chr1[i])
        else:
            child_chr.append(chr2[i])
    return child_chr


# Ordered crossover

def ordered_crossover(chr1, chr2):
    chromosome_length = len(chr1)

    # Random selection of start and end points for the subsequence
    start, end = sorted(rd.sample(range(chromosome_length), 2))

    # Creation of the offspring with a subsequence from the first parent
    child_chr = [None] * chromosome_length
    child_chr[start:end + 1] = chr1[start:end + 1]

    # Filling the rest of the offspring with elements from the second parent
    chr2_elements = [gene for gene in chr2 if gene not in child_chr[start:end + 1]]
    child_chr = [chr2_elements.pop(0) if gene is None else gene for gene in child_chr]

    return child_chr


def crossover_choice(chr1, chr2, choice):
    """
    Returns a new chromosome created by crossing over two chromosomes, with the choice of the crossover function.
    :param chr1:
    :param chr2:
    :param choice:
    :return:
    """
    # dictionary of crossover functions
    crossover_functions = {
        'single_point': single_point_crossover,
        'tow_points': two_points_crossover,
        'uniform': uniform_crossover,
        'order': ordered_crossover
    }
    if choice in crossover_functions:
        return crossover_functions[choice](chr1, chr2)
    else:
        raise ValueError("Invalid choice of crossover function.")
