from toolbox import UV,Room
import toolbox_student

def fitness(schedule, studentWeight = 1, classroomWeight = 1, teacherWeight = 1):
    fitnessScore = strongFitness(schedule, studentWeight, classroomWeight, teacherWeight)
    if(fitnessScore > 0): return 0 - fitnessScore
    return weakFitness(schedule)

def strongFitness(schedule, studentWeight = 1, classroomWeight = 1, teacherWeight = 1):
    fitnessScore = studentWeight * studentStrongFitness(schedule)
    fitnessScore += teacherWeight * teacherStrongFitness(schedule)
    fitnessScore += classroomWeight * classroomStrongFitness(schedule)
    return fitnessScore

def weakFitness(schedule, studentWeight = 1, classroomWeight = 1, teacherWeight = 1):
    fitnessScore = studentWeight * studentWeakFitness(schedule)
    fitnessScore += teacherWeight * teacherWeakFitness(schedule)
    fitnessScore += classroomWeight * classroomWeakFitness(schedule)
    return fitnessScore

def studentStrongFitness(schedule):
    return 0

def teacherStrongFitness(schedule):
     fitness = 0
     for i in range(len(schedule)):

        #Evaluate schedule conflicts with other timeslots
        fitnessImpact = 0
        for j in range(i,len(schedule)):
            if(schedule[i]['teacher'] != schedule[j]['teacher']): continue
            if(timeslotOverlap(schedule[i],schedule[j])):
                fitnessImpact +=1
                fitness += fitnessImpact

def classroomStrongFitness(schedule):
    fitness = 0
    for i in range(len(schedule)):

        #Evaluate student capacity
        if(studentCapacityOverload(schedule[i])): fitness+=1

        #Evaluate schedule conflicts with other timeslots
        fitnessImpact = 0
        for j in range(i,len(schedule)):
            if(schedule[i]['room'] != schedule[j]['room']): continue
            if(timeslotOverlap(schedule[i],schedule[j])):
                fitnessImpact +=1
                fitness += fitnessImpact

def studentCapacityOverload(timeslot):
    if timeslot['room'].capacity < UV.codeToUV(timeslot['code']).capacity:return False

def timeslotOverlap(timeslot1,timeslot2):
    if timeslot1.start_day != timeslot2.start_day : return False
    return timeslot1.start_time < timeslot2.start_time + timeslot2.duration and timeslot2.start_time < timeslot1.start_time + timeslot1.duration

#Can be re-written by building a list of conflicting UVs
def studentWeakFitness(schedule):
    fitness = 0
    for student in students:
        heat = 1
        i = 1
        for UV in student.UVs:
            for j in range(i,len(student.UVs)):
                if UVScheduleConflict(schedule, UV, student.UVs[j]):
                    fitness += heat
                    heat += 1
    return fitness

def UVScheduleConflict(schedule, UV1, UV2):
    for cours1 in UV1.cours:
        for cours2 in UV2.cours:
            if cours1.start < cours2.end and cours2.start < cours1.end : return True
    return False

def teacherWeakFitness(schedule):
    pass

def classroomWeakFitness(schedule):
    pass