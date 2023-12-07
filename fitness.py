def fitness(dataStrcuture, schedule, studentWeight = 1, classroomWeight = 1, teacherWeight = 1):
    fitnessScore = strongFitness(dataStrcuture, schedule, studentWeight, classroomWeight, teacherWeight)
    if(fitnessScore > 0): return fitnessScore + 1000 #Adding 1000 to all strong fitness so they get less prioritized than weakOnes
    return weakFitness(dataStrcuture, schedule)

def strongFitness(dataStrcuture, schedule, studentWeight = 1, classroomWeight = 1, teacherWeight = 1):
    fitnessScore = studentWeight * studentStrongFitness(dataStrcuture, schedule)
    fitnessScore += teacherWeight * teacherStrongFitness(dataStrcuture, schedule)
    fitnessScore += classroomWeight * classroomStrongFitness(dataStrcuture, schedule)
    return fitnessScore

def weakFitness(dataStrcuture, schedule, studentWeight = 1, classroomWeight = 1, teacherWeight = 1):
    fitnessScore = studentWeight * studentWeakFitness(dataStrcuture, schedule)
    fitnessScore += teacherWeight * teacherWeakFitness(dataStrcuture, schedule)
    fitnessScore += classroomWeight * classroomWeakFitness(dataStrcuture, schedule)
    return fitnessScore

def studentStrongFitness(dataStrcuture, schedule):
    return 0

def teacherStrongFitness(dataStrcuture, schedule):
     for i in range(len(schedule)):

        #Evaluate schedule conflicts with other timeslots
        
        fitnessImpact = 0
        for j in range(i,len(schedule)):
            if(schedule[i]['Teacher'] != schedule[j]['Teacher']): continue
            if(timeslotOverlap(schedule[i],schedule[j])):
                fitnessImpact +=1
                fitness += fitnessImpact

def classroomStrongFitness(dataStrcuture, schedule):
    fitness = 0
    for i in range(len(schedule)):

        #Evaluate student capacity
        if(studentCapacityOverload(schedule[i])): fitness+=1


        #Evaluate schedule conflicts with other timeslots
        
        fitnessImpact = 0
        for j in range(i,len(schedule)):
            if(schedule[i]['Classroom'] != schedule[j]['Classroom']): continue
            if(timeslotOverlap(schedule[i],schedule[j])):
                fitnessImpact +=1
                fitness += fitnessImpact

def studentCapacityOverload(dataStrcuture, timeslot):
    if timeslot['Classroom'].capacity < timeslot['Course'].UV.capacity:return False

def timeslotOverlap(dataStrcuture, timeslot1,timeslot2):
    return timeslot1.start < timeslot2.end and timeslot2.start < timeslot1.end
    
#Can be re-written by building a list of conflicting UVs
def studentWeakFitness(dataStrcuture, schedule):
    fitness = 0
    for student in dataStrcuture.students:
        heat = 1
        i = 1
        for UV in student.UVs:
            for j in range(i,len(student.UVs)):
                if UVScheduleConflict(dataStrcuture, schedule, UV, student.UVs[j]):
                    fitness += heat
                    heat += 1
    return fitness

def UVScheduleConflict(dataStrcuture, schedule, UV1, UV2):
    for cours1 in UV1.cours:
        for cours2 in UV2.cours:
            if cours1.start < cours2.end and cours2.start < cours1.end : return True
    return False

def teacherWeakFitness(dataStrcuture, schedule):
    pass

def classroomWeakFitness(dataStrcuture, schedule):
    pass