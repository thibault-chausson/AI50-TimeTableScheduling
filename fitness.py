from toolbox import UV, Room
import toolbox_student
import toolbox
import json
import time

def fitness(chromosome, arg_capacity_uv_promo_dict, studentWeight=1, classroomWeight=1, teacherWeight=1):
    fitnessScore = strongFitness(chromosome, arg_capacity_uv_promo_dict, studentWeight, classroomWeight, teacherWeight)
    if (fitnessScore > 0): return 0 - fitnessScore
    return weakFitness(chromosome)


def strongFitness(chromosome, arg_capacity_uv_promo_dict, studentWeight=1, classroomWeight=1, teacherWeight=1):
    fitnessScore = studentWeight * studentStrongFitness(chromosome)
    fitnessScore += teacherWeight * teacherStrongFitness(chromosome)
    fitnessScore += classroomWeight * classroomStrongFitness(chromosome, arg_capacity_uv_promo_dict)
    return fitnessScore


def weakFitness(chromosome, studentWeight=1, classroomWeight=1, teacherWeight=1):
    conflictDict = generateUVConflictDictionnary(chromosome)
    fitnessScore = studentWeight * studentWeakFitness(conflictDict)
    fitnessScore += teacherWeight * teacherWeakFitness(chromosome)
    fitnessScore += classroomWeight * classroomWeakFitness(chromosome)
    return fitnessScore


def studentStrongFitness(chromosome):
    return 0


def teacherStrongFitness(chromosome):
    fitness = 0
    index = 0
    for gene1 in chromosome:
        index += 1
        # Evaluate schedule conflicts with other timeslots
        fitnessImpact = 0
        for gene2 in chromosome[index:]:
            if (gene1.teacher != gene2.teacher): continue
            if (timeslotOverlap(gene1, gene2)):
                fitnessImpact += 1
                fitness += fitnessImpact
    return fitness


def classroomStrongFitness(chromosome, arg_capacity_uv_promo_dict):

    
    fitness = 0
    index = 0
    rooms = toolbox.get_rooms()
    for gene1 in chromosome:
        index += 1
        # Evaluate student capacity
        if (studentCapacityOverload(gene1,arg_capacity_uv_promo_dict,rooms)): fitness += 1

        # Evaluate schedule conflicts with other timeslots
        fitnessImpact = 0
        for gene2 in chromosome[index:]:
            if (gene1.room != gene2.room): continue
            if (timeslotOverlap(gene1, gene2)):
                fitnessImpact += 1
                fitness += fitnessImpact
    return fitness


def studentCapacityOverload(gene,uv_capacity,rooms):
    gene_room = next((room for room in rooms if room.room == gene.room), None)
    #PLACEHOLDER
    if gene.code not in uv_capacity: return False
    if gene_room.capacity < uv_capacity[gene.code]: return True
    return False


def timeslotOverlap(gene1, gene2):
    if gene1.start_day != gene2.start_day: return False
    return gene1.start_time < gene2.start_time + gene2.duration and gene2.start_time < gene1.start_time + gene1.duration

def generateUVConflictDictionnary(chromosome):
    conflictDict = {}
    uvs = toolbox.get_uvs()
    i = 0
    for uv in uvs:
        conflictDict[uv.code] = []
        for j in range(i):
            if UVScheduleConflict(chromosome,uv,uvs[j]):
                conflictDict[uv.code].append(uvs[j].code)
                conflictDict[uvs[j].code].append(uv.code)
    return conflictDict


def studentWeakFitness(conflictDict):
    fitness = 0
    students = toolbox_student.import_promo().students_list
    for student in students:
        score = 120  # A student with all 6 UVs in conflict would lose 120 fitness points, bringing its score to 0
        heat = 1
        i = 1
        for uv in student.uvs:
            for j in range(i + 1, len(student.uvs)):
                if uv in conflictDict[student.uvs[j]]:
                    score -= heat
                    heat += 1
        fitness += score
    return fitness


def UVScheduleConflict(chromosome, UV1, UV2):
    for cours1 in UV1.cours:
        for cours2 in UV2.cours:
            if cours1.start < cours2.end and cours2.start < cours1.end: return True
    return False


def teacherWeakFitness(chromosome):
    return 0


def classroomWeakFitness(chromosome):
    return 0
