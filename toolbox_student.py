# toolbox_student.py
import uuid as uuid
import random as rd
import toolbox as tb
import json


class Student:
    def __init__(self, student_id, name, uvs=None):
        self.student_id = student_id
        self.name = name
        self.uvs = uvs if uvs is not None else []

    def __repr__(self):
        return f"Student({self.student_id}, {self.name}, {self.uvs})"

    def add_uv(self, uv):
        if isinstance(uv, tb.UV):
            self.uvs.append(uv)
        else:
            print("L'objet n'est pas une instance de la classe UV")

    def export(self):
        return {
            "student_id": str(self.student_id),
            "name": self.name,
            "uvs": self.uvs
        }


class Promo:
    def __init__(self):
        self.students_list = []

    def add_student(self, student):
        if isinstance(student, Student):
            self.students_list.append(student)
        else:
            print("L'objet ajouté n'est pas une instance de la classe Student")

    def remove_student(self, student_id):
        self.students_list = [student for student in self.students_list if student.student_id != student_id]

    def get_student(self, student_id):
        for student in self.students_list:
            if student.student_id == student_id:
                return student
        return None

    def export(self):
        return {
            "students_list": self.students_list
        }

    def __repr__(self):
        return f"Promo({self.students_list})"


def get_all_uvs_chromosome(chromosome):
    uvs = []
    for gene in chromosome:
        if gene.code not in uvs:
            uvs.append(gene.code)
    return uvs


def create_student(list_uv, nb_uv=6):
    # ID is UUID, name is random, uvs is list of six UV form list_us
    ID = uuid.uuid4()
    name = "Student" + str(ID)
    # Pick six UV randomly from list_uv
    uvs = []
    index = rd.sample(range(len(list_uv) - 1), nb_uv)
    for i in range(len(index)):
        uvs.append(list_uv[index[i]])
    return Student(ID, name, uvs)


def create_promo(list_uv, promo_size):
    promo_fct = Promo()
    for _ in range(promo_size):
        promo_fct.add_student(create_student(list_uv))
    return promo_fct


def export_promo(promo_fct, filename="./datas/promo.json"):
    """
    Exports a promo into a json file.
    """
    with open(filename, "w") as f:
        json.dump([student.export() for student in promo_fct.students_list], f, indent=4)


def import_promo(filename="./datas/promo.json"):
    """
    Imports a promo from a json file.
    """
    with open(filename, "r") as f:
        students_list = json.load(f)
    promo_fct = Promo()
    for student in students_list:
        promo_fct.add_student(Student(student["student_id"], student["name"], student["uvs"]))
    return promo_fct


if __name__ == '__main__':
    chromosome_1 = tb.import_population("datas/population.json")[0]
    les_uvs = get_all_uvs_chromosome(chromosome_1)
    promo = create_promo(les_uvs, 300)
    print(promo)
    export_promo(promo, "datas/promo.json")
    promo_import = import_promo("datas/promo.json")
    print(promo_import)
    print("Done.")
