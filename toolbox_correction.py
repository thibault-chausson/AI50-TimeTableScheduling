import variables as var
import numpy as np


def occupied(plannings):
    """
    Returns the occupied rooms, teachers, ... at a given time stamp
    :param plannings: list of schedules for rooms, courses or professors...
    :return mat: a matrix of arrays of occupied rooms, or professors, or courses...
    """
    # Calculate the number of time slots based on the defined constants
    step = var.MINUTES_PER_CELL
    time_slots = int((var.END_TIME - var.START_TIME) / step)
    # Create a matrix with empty lists for each time slot and day
    mat = [[[] for _ in range(var.DAYS)] for _ in range(time_slots)]

    # Iterate over each planning in the list of plannings
    for planning in plannings:
        room = planning[1]  # Get the room or resource identifier
        # Find indices of non-zero elements in the planning matrix
        non_zero_indices = np.argwhere(planning[0] > 0)

        # For each pair of indices, add the room to the corresponding slot in mat
        for i, j in non_zero_indices:
            mat[i][j].append(room)

    return mat


def check_only_0_1(planning):
    """
    Returns True if the planning contains only 0 and 1
    :param planning: a planning
    :return: True or False
    """
    return planning[(planning != 0) & (planning != 1)].shape[0] == 0


def check_not_ubiquity(occupied_list):
    """
    Return array of true or false if a room, or professor, or group... is occupied by only one course
    :param occupied_list: list of occupied rooms, or professors, or courses...
    :return res, total: res is the array of true or false, total is True if all the rooms are occupied by only one course, or professor, or group..., else False
    """
    res = []
    total = True
    for occu in occupied_list:
        check = check_only_0_1(occu[0])
        res.append([check, occu[1]])  # occu[0] is the planning, occu[1] is the room, or professor, or course...
        if not check:
            total = False
    return res, total


def calculate_nb_students_by_uv(promo):
    """
    Returns a dictionary with the number of students by UV
    :param promo: a promo
    :return: a dictionary with the number of students by UV
    """
    res = {}
    for student in promo.students_list:  # Ici, on itère sur students_list
        for uv in student.uvs:
            if uv not in res:
                res[uv] = 1
            else:
                res[uv] += 1
    return res


def check_room_capacity(chr, room_capacity_dict, capacity_dict):
    """
    Returns True if the number of students in a room is less than the capacity of the room
    :param room_capacity_dict: a dictionary with the capacity of each room
    :param chr: a chromosome
    :param capacity_dict: a dictionary with the capacity of each room
    :return: list of timeslots where the number of students is greater than the capacity of the room, and UVs concerned
    """

    res = []
    for gene in chr:
        # Skip genes without a room or not in capacity_dict
        if gene.room is None or gene.code not in capacity_dict:
            continue

        # Check if the number of students exceeds the room capacity
        if capacity_dict[gene.code] > room_capacity_dict.get(gene.room, 0):
            res.append(
                {'start_time': gene.start_time, 'duration': gene.duration, 'start_day': gene.start_day,
                 'code': gene.code, 'room': gene.room})

    return res


def change_room_if_overcrowded_and_free(chr, room_too_small, room_list, room_occupied, capacity_dict):
    """
    Returns a chromosome with a new room for a given timeslot if the room is overcrowded and if there is a free room and the new planning of rooms
    :param chr: a chromosome
    :param room_too_small: list of timeslots where the number of students is greater than the capacity of the room, and UVs concerned
    :param room_list: a list of rooms
    :param room_occupied: a planning of rooms
    :param capacity_dict: a dictionary with the capacity of each room
    :return: a chromosome with a new room for a given timeslot if the room is overcrowded and if there is a free room and the new planning of rooms
    """
    # Set the time step based on a constant variable
    step = var.MINUTES_PER_CELL

    # Iterate over each gene in the chromosome
    for gene in chr:
        # Skip if there's no room assigned to the gene
        if gene.room is None:
            continue

        # Check if the current gene matches any of the overcrowded rooms
        for one_small_room in room_too_small:
            # Skip if the gene's details do not match the details of the overcrowded room
            if (gene.start_time, gene.start_day, gene.code, gene.room) != (
                    one_small_room['start_time'], one_small_room['start_day'], one_small_room['code'],
                    one_small_room['room']):
                continue

            # Calculate the start and end indices based on the gene's start time and duration
            index_start_time = gene.start_time // step - var.START_TIME // step
            index_end_time = index_start_time + gene.duration // step

            # Filter potential rooms that are free and have enough capacity
            potential_rooms = [room for room in room_list if room.capacity > capacity_dict[gene.code] and all(
                room.room not in room_occupied[i][gene.start_day] for i in range(index_start_time, index_end_time))]

            # Continue to the next gene if no potential room is found
            if not potential_rooms:
                continue

            # Assign the first potential room to the gene
            new_room = potential_rooms[0].room
            gene.room = new_room

            # Update the room_occupied matrix for the new room and remove the old room
            for j in range(index_start_time, index_end_time):
                room_occupied[j][gene.start_day].append(new_room)
                room_occupied[j][gene.start_day].remove(one_small_room['room'])
            break

    return chr, room_occupied


def find_all_course_between_time_slot_for_teacher(chr, start_time, end_time, start_day, teacher_name):
    """
    Returns a list of all the courses of a teacher between two time slots
    :param chr: a chromosome
    :param start_time: the start time of the time slot
    :param end_time: the end time of the time slot
    :param teacher_name: the name of the teacher
    :param start_day: the start day of the time slot
    :return: a list of all the courses of a teacher between two time slots with the index of the gene in the chromosome
    """
    res = []
    for i, gene in enumerate(chr):
        if (gene.teacher == teacher_name and gene.start_time >= start_time
                and gene.start_time + gene.duration <= end_time and gene.start_day == start_day):
            res.append([gene, i])
    return res


# Fonction pour regrouper les créneaux par jour
def regrouper_creneaux(indices, timeslots):
    step = var.MINUTES_PER_CELL
    grouped_timeslots = {}
    current_day = None
    current_start_time = None
    current_end_time = None

    for indice, timeslot in zip(indices, timeslots):
        day = indice[1]
        start_time = timeslot[0]

        if day != current_day:
            if current_day is not None:
                grouped_timeslots[current_day].append([current_start_time, current_end_time])
            current_day = day
            current_start_time = start_time
            current_end_time = start_time + step
            grouped_timeslots.setdefault(current_day, [])
        else:
            if start_time == current_end_time:
                # Créneau consécutif
                current_end_time += step
            else:
                # Nouvel intervalle
                grouped_timeslots[current_day].append([current_start_time, current_end_time])
                current_start_time = start_time
                current_end_time = start_time + step

    # Ajout du dernier intervalle
    if current_day is not None:
        grouped_timeslots[current_day].append([current_start_time, current_end_time])

    return grouped_timeslots


def change_timeslot_teacher_occupied(chr, teacher_name, planning_teacher):
    """
    Returns a chromosome with a new timeslot for a given teacher if the teacher is occupied and if there is a free timeslot.
    :param chr: Chromosome representing the current schedule.
    :param teacher_name: Name of the teacher.
    :param planning_teacher: Current planning of the teacher.
    :return: Updated chromosome with changed timeslot.
    """

    # Define the time step (duration of each cell in the timetable)
    step = var.MINUTES_PER_CELL

    # Find the indices of timeslots where the teacher is occupied (values > 1 in planning_teacher indicate occupation)
    indices = np.argwhere(planning_teacher > 1)


    # Convert these indices to actual timeslots considering the start time of the day and the step
    timeslots = []
    for indice in indices:
        timeslots.append([indice[0] * step + var.START_TIME, indice[1]])

    # Group the timeslots by day
    creneau = regrouper_creneaux(indices, timeslots)

    # Retrieve the teacher's courses within these occupied timeslots
    courses = []
    for day in creneau:
        for cre in creneau[day]:
            courses.append(find_all_course_between_time_slot_for_teacher(chr, cre[0], cre[1], day, teacher_name))

    # Look for free timeslots that can accommodate the teacher's courses and update the start_time and start_day
    for course in courses:
        for cour in course:
            # Find free timeslots for the teacher's courses
            old_start_time = cour[0].start_time
            old_start_day = cour[0].start_day
            old_end_time = old_start_time + cour[0].duration
            free_timeslots_start = []

            # Check each potential timeslot for availability
            for i in range(0, int((var.END_TIME - var.START_TIME - cour[0].duration) // step)):
                for j in range(var.DAYS):
                    conditions = [planning_teacher[i + k][j] == 0 for k in range(0, cour[0].duration // step)]
                    if all(conditions):
                        free_timeslots_start.append([i, j])

            # If there are free timeslots available
            if len(free_timeslots_start) > 0:
                # Find the closest free timeslot
                closest_timeslot = min(free_timeslots_start, key=lambda x: abs(x[0] - cour[0].start_time // step))

                # Update the start_time and start_day and modify the teacher's planning accordingly
                cour[0].start_time = closest_timeslot[0] * step + var.START_TIME
                cour[0].start_day = closest_timeslot[1]

                # Place the course in the chromosome
                chr[cour[1]] = cour[0]

                # Update the teacher's planning: remove the old timeslot and add the new one
                new_start_day = cour[0].start_day
                new_start_time = cour[0].start_time
                new_end_time = new_start_time + cour[0].duration
                for i in range((new_start_time - var.START_TIME) // step, (new_end_time - var.START_TIME) // step):
                    planning_teacher[i][new_start_day] += 1

                for i in range((old_start_time - var.START_TIME) // step, (old_end_time - var.START_TIME) // step):
                    planning_teacher[i][old_start_day] -= 1

    return chr
