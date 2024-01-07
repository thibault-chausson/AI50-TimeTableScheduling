import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import ListedColormap
import matplotlib.ticker as mticker

from toolbox import *
from variables import *


def get_genes_from(chr, kind, key):
    """
    Returns all the genes from a given chromosome that match the given key, based on the given kind.
    Example: get_genes_from(chromosome, "teacher", "M. Dupont") will return all the genes from the chromosome that have "M. Dupont" as a teacher.
    chr: list of Gene objects
    kind: str, either "teacher", "room", "uv" or "student".
    key: str or Student object, the teacher, room, uv or student to look for
    """
    if kind == "teacher":
        return [i for i in chr if i.teacher == key]
    elif kind == "room":
        return [i for i in chr if i.room == key]
    elif kind == "uv":
        return [i for i in chr if i.code == key]
    elif kind == "student":
        classes = []
        for uv in key.uvs:
            for gene in chr:
                if gene.code == uv:
                    classes.append(gene)
        return classes


def get_classes_mat(chr):
    """
    Transforms a chromosome coming from get_genes_from into a matrix with classes as values, when a class is present at a given time and day.
    chr: list of Gene objects
    """
    mat = [[None for _ in range(DAYS)] for _ in range(int((END_TIME - START_TIME) / MINUTES_PER_CELL))]
    mat = np.array(mat)
    for gene in chr:
        start = gene.start_time // MINUTES_PER_CELL - START_TIME // MINUTES_PER_CELL
        mat[start:start + gene.duration // MINUTES_PER_CELL, gene.start_day] = ", ".join(
            (gene.code, gene.room, gene.type))
    mat[mat == None] = ""

    return mat


def make_schedule(mat, chr, kind, key, save_path="./images/schedule.png"):
    """
    Makes a schedule based on a matrix coming from get_classes_mat.
    mat: np.array, matrix of classes coming from get_classes_mat
    chr: list of Gene objects coming from get_genes_from
    kind: str, either "teacher", "room" or "uv"
    key: str, the teacher, room or uv code to look for
    save_path: str, path where to save the schedule. If None is given, the schedule will be displayed instead of saved.
    """
    plt.figure(figsize=(8, 8), dpi=100)
    index = [f'{minute // 60}:{minute % 60:02d}' for minute in range(START_TIME, END_TIME, MINUTES_PER_CELL)]
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    df_schedule = pd.DataFrame(mat, index=index, columns=days_of_week)

    uvs = [gene.code for gene in chr]
    uvs.insert(0, "")
    value_map = {elem: i for i, elem in enumerate(set(mat.flatten()))}
    value_map[""] = 0
    for i, uv in enumerate(list(set(uvs))):
        for k in value_map.keys():
            if uv in k:
                value_map[k] = i

    df_schedule_numeric = df_schedule.replace(value_map)
    seen = []
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            if mat[i, j] not in seen:
                seen.append(mat[i, j])
            else:
                mat[i, j] = ""
    df_schedule = pd.DataFrame(mat, index=index, columns=days_of_week)

    colors = ['lightgray'] + sns.color_palette('tab20', len(set(mat.flatten())) - 1).as_hex()
    colormap = ListedColormap(colors)

    ax = sns.heatmap(df_schedule_numeric, cmap=colormap, cbar=False, annot=df_schedule, fmt='s')
    ticks_loc = ax.get_yticks().tolist()
    ax.yaxis.set_major_locator(mticker.FixedLocator([t - 0.5 for t in ticks_loc]))
    ax.set_yticklabels(index)  # replace with your labels
    plt.tick_params(axis='x', bottom=False, top=True, labelbottom=False, labeltop=True)

    plt.title("Schedule for {} {}".format(kind, key))

    if save_path != None:
        plt.savefig(save_path, bbox_inches='tight')
    else:
        plt.show()
