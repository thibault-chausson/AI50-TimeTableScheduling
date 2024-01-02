from toolbox import *
import itertools
import variables as var

def no_overlaps(chr):
    """
    Hard Constraint.
    Check whether or not they are overlapping types of UVs between rooms, teachers and uvs.
    """
    for schedule, _ in planning_teacher(chr):
        if len(schedule[schedule > 1]) > 0:
            return False
    for schedule, _ in planning_room(chr):
        if len(schedule[schedule > 1]) > 0:
            return False
    for schedule, _ in planning_uv(chr):
        if len(schedule[schedule > 1]) > 0:
            return False
    return True


def lunch_break(chr, minimum_time=45):
    """
    Soft Constraint.
    Returns the number of teachers and Students (coming soon™) who won't have a lunch break, and the total number of teachers and students checked.
    Details: If someone has at least ONE day without a lunch break, he is counted as not having a lunch break.
    returns: (number of people who won't have lunch time, total number of people checked)
    """
    no_lunch_for_you, total_checked = 0, 0
    
    teachers = planning_teacher(chr)
    for teacher, _ in teachers:
        total_checked += 1
        res = np.zeros(var.DAYS)
        for i, col in enumerate(teacher[(12 * 60 - var.START_TIME)//var.MINUTES_PER_CELL:(14 * 60 - var.START_TIME)//var.MINUTES_PER_CELL,].T):
            temp = []
            for number, elem in itertools.groupby(col):
                if number == 1:
                    temp.append(len(list(elem)))
            res[i] = max(temp)
        
        if res[res >= minimum_time / var.MINUTES_PER_CELL].size != var.DAYS:
            no_lunch_for_you += 1
        
    return no_lunch_for_you, total_checked


def statistics(chr):
    """
    Soft Constaint.
    Returns statistics about a given chromosome.
    returns: (mean of the range of the teachers (see 2.4.2.1), mean of the gaps of the teachers (see 2.4.2.2))
    For our problem, both would need to be as small as possible.
    """

    teachers = planning_teacher(chr)
    ranges = []
    gaps = []
    for teacher, _ in teachers:
        means = teacher.sum(axis=0)/teacher.shape[0]
        ranges.append(means.max() - means.min())

        res = []
        for col in teacher.T:
            res.append(len([0 for _ in itertools.groupby(col)]))
        gaps.append(np.mean(res))

    return np.mean(ranges), np.mean(gaps)


def rooms_capacity():
    """
    Hard Constraint.
    Checks whether or not the room's capacity if respected, given students schedules.
    Will be done later as I do not know yet how to give a student a schedule based on his choices.
    """
    pass
    
