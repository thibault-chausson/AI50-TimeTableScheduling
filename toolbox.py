import numpy as np
import json


WEEKS = 15 # Number of weeks in a semester
DAYS = 5 # Number of days there is class in a week
MINUTES_PER_CELL = 30 # one cell of the matrix equals 30 minutes
START_TIME = 8 * 60 # Start of the day at 8am
END_TIME = 20 * 60 # End of the day at 8pm

class Room:
    def __init__(self, room, capacity, type, description, site):
        self.room = room
        self.capacity = capacity
        self.type = type
        self.description = description
        self.site = site
    
    def __repr__(self):
        return f"Room({self.room}, {self.capacity}, {self.type}, {self.description}, {self.site})"


class UV:
    def __init__(self, code, name, credits, semester, rooms, teachers, cm=0, td=0, tp=0):
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
    
    def __repr__(self):
        return f"UV({self.code}, {self.name}, {self.credits}, {self.semester}, {self.rooms}, {self.teachers}, total_min: {self.cm + self.td + self.tp})"


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
        return f"Gene({self.room}, {self.start_time}, {self.duration}, {self.teacher}, {self.code}, {self.type})"


def planning_teacher(chr, teacher=None):
    """
    Returns a planning for a given teacher in form of a binary matrix.
    If None is given, returns the planning for all teachers.
    """
    step = MINUTES_PER_CELL
    mat = np.zeros((int((END_TIME - START_TIME) / step), DAYS))
    if teacher is not None:
        for gene in chr:
            if teacher == gene.teacher:
                start = gene.start_time // step - START_TIME // step # 480 means the start of the matrix is at 8AM
                mat[start:start + gene.duration // step, gene.start_day] += 1
        return mat
    else:
        mats = []
        for teacher in set([i.teacher for i in chr]):
            mats.append(planning_teacher([i for i in chr if i.teacher == teacher], teacher))
        return mats


def planning_room(chr, room=None):
    """
    Returns a planning for a given room in form of a binary matrix.
    If None is given, returns the planning for all rooms.
    """
    step = MINUTES_PER_CELL
    mat = np.zeros((int((END_TIME - START_TIME) / step), DAYS))
    if room is not None:
        for gene in chr:
            if room == gene.room:
                start = gene.start_time // step - START_TIME // step # 480 means the start of the matrix is at 8AM
                mat[start:start + gene.duration // step, gene.start_day] += 1
        return mat
    else:
        mats = []
        for room in set([i.room for i in chr]):
            mats.append(planning_room([i for i in chr if i.room == room], room))
        return mats


def planning_uv(chr, uv=None):
    """
    Returns a planning for a given UV in form of a binary matrix.
    If None is given, returns the planning for all UVs.
    """
    step = MINUTES_PER_CELL
    mat = np.zeros((int((END_TIME - START_TIME) / step), DAYS))
    if uv is not None:
        for gene in chr:
            if uv == gene.code:
                start = gene.start_time // step - START_TIME // step # 480 means the start of the matrix is at 8AM
                mat[start:start + gene.duration // step, gene.start_day] += 1
        return mat
    else:
        mats = []
        for uv in set([i.code for i in chr]):
            mats.append(planning_uv([i for i in chr if i.code == uv], uv))
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
        return total * WEEKS
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
    with open("salles.json", "r") as f:
        rooms = json.load(f)

    for salle, desc in rooms.items():
        if desc["site"] == site or site is None:
            salles.append(Room(salle, desc["capacity"], desc["type"], desc["description"], desc["site"]))
    
    return salles


def get_uvs(category=None):
    """
    Returns a list of UV objects, from a certain category ('FISE-INFO', 'FISA-INFO', ...).
    """

    with open("desc_uv.json", "r") as f:
        desc_uv = json.load(f)

    uv_info = []
    for uv in desc_uv:
        if category in str(uv) or category is None:
            o = ""
            teachers = []
            if uv["automne"] is not None:
                o += "A"
                teachers.append(uv["automne"]["responsable"])
            if uv["printemps"] is not None:
                o += "P"
                teachers.append(uv["printemps"]["responsable"])
            cm, td, tp = 0, 0, 0

            for acti in uv["activites"]:
                if acti["code"] == "CM":
                    cm = acti["nbh"]
                elif acti["code"] == "TD":
                    td = acti["nbh"]
                elif acti["code"] == "TP":
                    tp = acti["nbh"]
            uv_info.append(UV(uv["code"], uv["libelle"], float(uv["creditsEcts"]), o, [], list(set(teachers)), cm, td, tp))
    
    return uv_info


def export_population(population, filename="./chromosome.json"):
    """
    Exports a population into a json file.
    """
    with open(filename, "w") as f:
        json.dump([[gene.export() for gene in chr] for chr in population], f, indent=4)


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
            chr.append(Gene(gene["room"], gene["start_time"], gene["start_day"], gene["duration"], gene["teacher"], gene["code"], gene["type"]))
        population.append(chr)
    
    return population