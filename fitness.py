def fitness(schedule):
    fitnessScore = strongFitness(schedule)
    if(fitnessScore > 0):
        return fitnessScore
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
    pass

def teacherStrongFitness(schedule):
    pass

def classroomStrongFitness(schedule):
    pass

def studentWeakFitness(schedule):
    pass

def teacherWeakFitness(schedule):
    pass

def classroomWeakFitness(schedule):
    pass