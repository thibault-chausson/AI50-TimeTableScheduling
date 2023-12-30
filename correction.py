import toolbox as tb
import toolbox_correction as tb_c
import toolbox_student as tb_s


def correction_room(chr, room_list):
    # TODO: implement this function, it should return a corrected chromosome, and select the best arguments for
    #  the function
    pass


if __name__ == '__main__':
    CHROMOSOME_1 = tb.import_population("datas/chromosome_1.json")[0]
    LIST_ROOM = tb.get_rooms()
    LIST_UVS = tb.import_uvs()
    PROMO = tb_s.import_promo()
    plannings = tb.planning_room(CHROMOSOME_1)
    occupee = tb_c.occupied(plannings)
    capacity_dict = tb_c.calculate_nb_students_by_uv(PROMO)

    print("chr", CHROMOSOME_1)
    print("list_room", LIST_ROOM)
    print("capacity_dict", capacity_dict)

    # Convert room_list to a dictionary for faster access
    room_capacity_dict = {room.room: room.capacity for room in LIST_ROOM}

    room_too_small = tb_c.check_room_capacity(CHROMOSOME_1, room_capacity_dict, capacity_dict)

    print("room_too_small", room_too_small)



    # print("room_too_small", room_too_small)
    #
    # correc, _ = tb_c.change_room_if_overcrowded_and_free(CHROMOSOME_1, room_too_small, LIST_ROOM, occupee,
    #                                                      capacity_dict)
    #
    # print("correc", correc)
    #
    # check_new_chr = tb_c.check_room_capacity(correc, LIST_ROOM, capacity_dict)
    #
    # print("check_new_chr", check_new_chr)
