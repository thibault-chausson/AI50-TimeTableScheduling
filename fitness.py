from toolbox import UV,Room
import toolbox_student

def fitness(chromosome, studentWeight = 1, classroomWeight = 1, teacherWeight = 1):
    fitnessScore = strongFitness(chromosome, studentWeight, classroomWeight, teacherWeight)
    if(fitnessScore > 0): return 0 - fitnessScore
    return 0 # No weak fitness for now
    # return weakFitness(chromosome)  

def strongFitness(chromosome, studentWeight = 1, classroomWeight = 1, teacherWeight = 1):
    fitnessScore = studentWeight * studentStrongFitness(chromosome)
    fitnessScore += teacherWeight * teacherStrongFitness(chromosome)
    fitnessScore += classroomWeight * classroomStrongFitness(chromosome)
    return fitnessScore 

def weakFitness(chromosome, studentWeight = 1, classroomWeight = 1, teacherWeight = 1):
    fitnessScore = studentWeight * studentWeakFitness(chromosome)
    fitnessScore += teacherWeight * teacherWeakFitness(chromosome)
    fitnessScore += classroomWeight * classroomWeakFitness(chromosome)
    return fitnessScore

def studentStrongFitness(chromosome):
    return 0

def teacherStrongFitness(chromosome):
    fitness = 0
    index = 0
    for gene1 in chromosome:
        index+=1
        #Evaluate schedule conflicts with other timeslots
        fitnessImpact = 0
        for gene2 in chromosome[index:]:
            if(gene1.teacher != gene2.teacher): continue
            if(timeslotOverlap(gene1,gene2)):
                fitnessImpact +=1
                fitness += fitnessImpact
    return fitness

def classroomStrongFitness(chromosome):
    fitness = 0
    index = 0
    for gene1 in chromosome:
        index += 1
        #Evaluate student capacity
        if(studentCapacityOverload(gene1)): fitness+=1

        #Evaluate schedule conflicts with other timeslots
        fitnessImpact = 0
        for gene2 in chromosome[index:]:
            if(gene1.room != gene2.room): continue
            if(timeslotOverlap(gene1,gene2)):
                fitnessImpact +=1
                fitness += fitnessImpact
    return fitness

def studentCapacityOverload(gene):
    if Room.codeToRoom(gene.room).capacity < UV.codeToUV(gene.code).capacity:return True
    return False

def timeslotOverlap(gene1,gene2):
    if gene1.start_day != gene2.start_day : return False
    return gene1.start_time < gene2.start_time + gene2.duration and gene2.start_time < gene1.start_time + gene1.duration

#Can be re-written by building a list of conflicting UVs
def studentWeakFitness(chromosome):
    fitness = 0
    students = toolbox_student.promo_import().students_list
    for student in students:
        heat = 1
        i = 1
        for uv in student.uvs:
            for j in range(i+1,len(student.uvs)):
                if UVScheduleConflict(chromosome, uv, student.uvs[j]):
                    fitness += heat
                    heat += 1
    return fitness

def UVScheduleConflict(chromosome, UV1, UV2):
    for cours1 in UV1.cours:
        for cours2 in UV2.cours:
            if cours1.start < cours2.end and cours2.start < cours1.end : return True
    return False

def teacherWeakFitness(chromosome):
    return 0

def classroomWeakFitness(chromosome):
    return 0