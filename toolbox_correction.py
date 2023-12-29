import variables as var


def occupied(plannings):
    """
    Returns the occupied rooms at a given time stamp
    :param plannings: list of schedules for rooms, courses or professors...
    :return mat: a matrix of arrays of occupied rooms, or professors, or courses...
    """
    step = var.MINUTES_PER_CELL
    mat = [[[] for _ in range(var.DAYS)] for _ in range(int((var.END_TIME - var.START_TIME) / step))]
    for planning in plannings:
        room = planning[1]
        for i in range(len(planning[0])):
            for j in range(len(planning[0][i])):
                if planning[0][i][j] > 0:
                    mat[i][j].append(room)
    return mat


def check_only_0_1(planning):
    """
    Returns True if the planning contains only 0 and 1
    :param planning: a planning
    :return: True or False
    """
    for i in range(len(planning)):
        for j in range(len(planning[i])):
            if planning[i][j] != 0 and planning[i][j] != 1:
                return False
    return True


def check_not_ubiquity(occupied_list):
    """
    Return array of true or false if a room is occupied by only one course, or professor, or group...
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


def check_room_capacity(chr, room_list, capacity_dict):
    """
    Returns True if the number of students in a room is less than the capacity of the room
    :param chr: a chromosome
    :param room_list: a list of rooms
    :param capacity_dict: a dictionary with the capacity of each room
    :return: list of timeslots where the number of students is greater than the capacity of the room, and UVs concerned
    """
    res = []
    for gene in chr:
        if gene.room is not None:
            for room in room_list:
                if gene.room == room.room:
                    if gene.code in capacity_dict:
                        if capacity_dict[gene.code] > room.capacity:
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
    for gene in chr:
        if gene.room is not None:
            for one_small_room in room_too_small:
                if gene.start_time == one_small_room['start_time'] and gene.start_day == one_small_room[
                    'start_day'] and gene.code == one_small_room['code'] and gene.room == one_small_room['room']:
                    for room in room_list:
                        step = var.MINUTES_PER_CELL
                        index_start_time = gene.start_time // step - var.START_TIME // step
                        print(index_start_time)
                        print(gene.start_time)
                        print(gene.duration)
                        index_end_time = index_start_time + gene.duration // step
                        if room.capacity > capacity_dict[gene.code] and all(
                                [room.room not in room_occupied[i][gene.start_day] for i in
                                 range(index_start_time, index_end_time)]):
                            gene.room = room.room
                            for j in range(index_start_time, index_end_time):
                                # Add room to schedule of occupied rooms
                                room_occupied[j][gene.start_day].append(room.room)
                                # Removal of the old room from the schedule of occupied rooms
                                print(room_occupied[j][gene.start_day])
                                room_occupied[j][gene.start_day].remove(one_small_room['room'])
                            break
                    break
    return chr, room_occupied
