import numpy as np
import json
import random as rd
import variables as var


class Room:
    def __init__(self, room, capacity, type, description, site):
        self.room = room
        self.capacity = capacity
        self.type = type
        self.description = description
        self.site = site

    def codeToRoom(roomCode):
        with open('datas/salles.json') as f_in:
            rooms = json.load(f_in)
        if roomCode not in rooms:
            print("Non existing room " + roomCode)
            return None
        targetRoom = rooms[roomCode]
        newRoom = Room(
            roomCode,
            targetRoom["capacity"],
            targetRoom["type"],
            targetRoom["description"],
            targetRoom["site"]
        )
        return newRoom

    def __repr__(self):
        return f"Room({self.room}, {self.capacity}, {self.type}, {self.description}, {self.site})"


class UV:
    def __init__(self, code, name, credits, semester, rooms, teachers, cm=0, td=0, tp=0, capacity=0):
        self.code = code
        self.name = name
        self.credits = credits
        self.semester = semester
        self.rooms = rooms
        self.teachers = teachers
        # The time for each type of class in minutes
        self.cm = cm
        self.td = td
        self.tp = tp
        self.capacity = capacity

    def codeToUV(UVCode):
        with open('datas/uvs.json') as f_in:
            uvs = json.load(f_in)
        targetUV = next((item for item in uvs if item["code"] == UVCode), None)
        if targetUV == None: return None
        newUV = UV(
            UVCode,
            targetUV["name"],
            targetUV["credits"],
            targetUV["semester"],
            targetUV["rooms"],
            targetUV["teachers"],
            targetUV["cm"],
            targetUV["td"],
            targetUV["tp"],
            targetUV["capacity"]
        )
        return newUV

    def export(self):
        return {
            "code": self.code,
            "name": self.name,
            "credits": self.credits,
            "semester": self.semester,
            "rooms": self.rooms,
            "teachers": self.teachers,
            "cm": self.cm,
            "td": self.td,
            "tp": self.tp,
            "capacity": self.capacity
        }

    def __repr__(self):
        return f"UV({self.code}, {self.name}, {self.credits}, {self.semester}, {self.rooms}, {self.teachers}, total_min: {self.cm + self.td + self.tp}, {self.capacity})"


class Gene:
    def __init__(self, room, start_time, start_day, duration, teacher, code, course_type):
        self.room = room
        self.start_time = start_time
        self.start_day = start_day
        self.duration = duration
        self.teacher = teacher
        self.code = code
        self.type = course_type

    def export(self):
        return {
            "room": self.room,
            "start_time": self.start_time,
            "start_day": self.start_day,
            "duration": self.duration,
            "teacher": self.teacher,
            "code": self.code,
            "type": self.type
        }

    def __repr__(self):
        return f"Gene({self.room}, {self.start_time}, {self.start_day}, {self.duration}, {self.teacher}, {self.code}, {self.type})"


def planning_teacher(chr, teacher=None):
    """
    Returns a planning for a given teacher in form of a sparse matrix, if all numbers are 0 or 1  it's good, else a
    teacher has two simultaneous courses.
    If None is given, returns the planning for all teachers.
    """
    step = var.MINUTES_PER_CELL
    mat = np.zeros((int((var.END_TIME - var.START_TIME) / step), var.DAYS))
    if teacher is not None:
        for gene in chr:
            if teacher == gene.teacher:
                start = gene.start_time // step - var.START_TIME // step  # 480 means the start of the matrix is at 8AM
                mat[start:start + gene.duration // step, gene.start_day] += 1
        return mat
    else:
        mats = []
        for teacher in set([i.teacher for i in chr]):
            mats.append([planning_teacher([i for i in chr if i.teacher == teacher], teacher), teacher])
        return mats


def find_conflicts(planning):
    """
    Returns a list of conflicts in a given planning.
    indices = np.argwhere((matrice != 0) & (matrice != 1))
    """
    conflicts = []
    for i in range(len(planning)):
        for j in range(len(planning[i])):
            if planning[i][j] > 1:
                conflicts.append((i, j))
    return conflicts


def planning_room(chr, room=None):
    """
    Returns a planning for a given room in form of a sparse matrix, if all numbers are 0 or 1  it's good, else a room
    has two simultaneous courses.
    If None is given, returns the planning for all rooms.
    """
    step = var.MINUTES_PER_CELL
    mat = np.zeros((int((var.END_TIME - var.START_TIME) / step), var.DAYS))
    if room is not None:
        for gene in chr:
            if room == gene.room:
                start = gene.start_time // step - var.START_TIME // step  # 480 means the start of the matrix is at 8AM
                mat[start:start + gene.duration // step, gene.start_day] += 1
        return mat
    else:  # If no room is given, we return a list of matrices for each room => [[matrice, room], ...]
        mats = []
        for room in set([i.room for i in chr]):
            mats.append([planning_room([i for i in chr if i.room == room], room), room])
        return mats


def planning_uv(chr, uv=None):
    """
    Returns a planning for a given UV in form of a sparse matrix, if all numbers are 0 or 1  it's good, else a UV
    has two simultaneous sessions.
    If None is given, returns the planning for all UVs.
    """
    step = var.MINUTES_PER_CELL
    mat = np.zeros((int((var.END_TIME - var.START_TIME) / step), var.DAYS))
    if uv is not None:
        for gene in chr:
            if uv == gene.code:
                start = gene.start_time // step - var.START_TIME // step  # 480 means the start of the matrix is at 8AM
                mat[start:start + gene.duration // step, gene.start_day] += 1
        return mat
    else:
        mats = []
        for uv in set([i.code for i in chr]):
            mats.append([planning_uv([i for i in chr if i.code == uv], uv), uv])
        return mats


def calc_uv_time(chr, uv=None):
    """
    Returns the total time of a given UV in a given chromosome.
    """
    total = 0
    if uv is not None:
        for gene in chr:
            if uv == gene.code:
                total += gene.duration
        return total * var.WEEKS
    else:
        totals = {}
        for uv in set([i.code for i in chr]):
            totals[uv] = calc_uv_time([i for i in chr if i.code == uv], uv)
        return totals


def get_rooms(site=None):
    """
    Returns a list of Room objects.
    """
    salles = []
    with open("datas/salles.json", "r") as f:
        rooms = json.load(f)

    for salle, desc in rooms.items():
        if desc["site"] == site or site is None:
            salles.append(Room(salle, desc["capacity"], desc["type"], desc["description"], desc["site"]))

    return salles


def get_uvs(category=None):
    """
    Returns a list of UV objects, from a certain category ('FISE-INFO', 'FISA-INFO', ...).
    """

    with open("datas/desc_uv.json", "r") as f:
        desc_uv = json.load(f)

    uv_info = []
    for uv in desc_uv:
        if category is None or category in str(uv):
            o = ""
            teachers = []
            if uv["automne"] is not None:
                o += "A"
                teachers.append(uv["automne"]["responsable"])
            if uv["printemps"] is not None:
                o += "P"
                teachers.append(uv["printemps"]["responsable"])
            cm, td, tp = 0, 0, 0
            capacity = rd.randint(20, 75)

            for acti in uv["activites"]:
                if acti["code"] == "CM":
                    cm = acti["nbh"]
                elif acti["code"] == "TD":
                    td = acti["nbh"]
                elif acti["code"] == "TP":
                    tp = acti["nbh"]
            uv_info.append(
                UV(uv["code"], uv["libelle"], float(uv["creditsEcts"]), o, [], list(set(teachers)), cm, td, tp,
                   capacity))

    return uv_info


def export_uvs(uvs_fct, filename="./datas/uvs.json"):
    """
    Exports a list of UVs into a json file.
    :param uvs_fct:
    :param filename:
    :return:
    """
    with open(filename, "w") as f:
        json.dump([uv.export() for uv in uvs_fct], f, indent=4)


def import_uvs(filename="./datas/uvs.json"):
    """
    Imports a list of UVs from a json file.
    :param filename:
    :return:
    """
    with open(filename, "r") as f:
        uvs_load = json.load(f)
    uvs_fct = []
    for uv in uvs_load:
        uvs_fct.append(
            UV(uv["code"], uv["name"], uv["credits"], uv["semester"], uv["rooms"], uv["teachers"], uv["cm"], uv["td"],
               uv["tp"], uv["capacity"]))
    return uvs_fct


def generate_uv_capacities(mean, spread, input_file="./datas/uvs.json", output_file="./datas/uvs.json"):
    uv_list = import_uvs(filename=input_file)
    for uv in uv_list:
        uv.capacity = round(np.random.normal(mean, spread))
    export_uvs(uv_list, filename=output_file)


def export_population(population, filename="./datas/chromosome.json"):
    """
    Exports a population into a json file.
    """
    with open(filename, "w") as f:
        json.dump([[gene.export() for gene in chr] for chr in population], f, indent=4)


def export_chr(chr, filename="./datas/chromosome_only.json"):
    """
    Exports a chromosome into a json file.
    :param chr:
    :param filename:
    :return:
    """
    with open(filename, "w") as f:
        json.dump([gene.export() for gene in chr], f, indent=4)


def import_population(filename):
    """
    Returns a population of chromosomes from a solution file.
    """
    population = []
    with open(filename, "r") as f:
        data = json.load(f)
    for chromosome in data:
        chr = []
        for gene in chromosome:
            chr.append(Gene(gene["room"], gene["start_time"], gene["start_day"], gene["duration"], gene["teacher"],
                            gene["code"], gene["type"]))
        population.append(chr)

    return population
