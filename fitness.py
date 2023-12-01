def fitness(schedule, studentWeight = 1, classroomWeight = 1, teacherWeight = 1):
    fitnessScore = strongFitness(schedule, studentWeight, classroomWeight, teacherWeight)
    if(fitnessScore > 0): return fitnessScore + 1000 #Adding 1000 to all strong fitness so they get less prioritized than weakOnes
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
     for i in range(len(schedule)):

        #Evaluate schedule conflicts with other timeslots
        
        fitnessImpact = 0
        for j in range(i,len(schedule)):
            if(schedule[i]['Teacher'] != schedule[j]['Teacher']): continue
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
            if(schedule[i]['Classroom'] != schedule[j]['Classroom']): continue
            if(timeslotOverlap(schedule[i],schedule[j])):
                fitnessImpact +=1
                fitness += fitnessImpact

def studentCapacityOverload(timeslot):
    if timeslot['Classroom'].capacity < timeslot['Course'].UV.capacity:return False

def timeslotOverlap(timeslot1,timeslot2):
    return timeslot1.start < timeslot2.end and timeslot2.start < timeslot1.end
    

def studentWeakFitness(schedule):
    pass

def teacherWeakFitness(schedule):
    pass

def classroomWeakFitness(schedule):
    pass