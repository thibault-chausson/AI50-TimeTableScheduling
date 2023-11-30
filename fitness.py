def fitness(schedule):
    fitnessScore = strongFitness(schedule)
    if(fitnessScore > 0): return fitnessScore
    return weakFitness(schedule)

def strongFitness(schedule):
    fitnessScore = studentStrongFitness(schedule)
    fitnessScore += teacherStrongFitness(schedule)
    fitnessScore += classroomStrongFitness(schedule)
    return fitnessScore

def weakFitness(schedule):
    fitnessScore = studentWeakFitness(schedule)
    fitnessScore += teacherWeakFitness(schedule)
    fitnessScore += classroomWeakFitness(schedule)
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
    return False

def timeslotOverlap(timeslot1,timeslot2):
    return timeslot1.start < timeslot2.end and timeslot2.start < timeslot1.end
    

def studentWeakFitness(schedule):
    pass

def teacherWeakFitness(schedule):
    pass

def classroomWeakFitness(schedule):
    pass