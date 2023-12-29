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

    print(occupee)

    print(PROMO)

    capacity_dict = tb_c.calculate_nb_students_by_uv(PROMO)

    print(capacity_dict)
    print(LIST_UVS)
    print(LIST_ROOM)

    room_too_small = tb_c.check_room_capacity(CHROMOSOME_1, LIST_ROOM, capacity_dict)

    print(room_too_small)

    correc, _ = tb_c.change_room_if_overcrowded_and_free(CHROMOSOME_1, room_too_small, LIST_ROOM, occupee,
                                                         capacity_dict)

    print(correc)

    check_new_chr = tb_c.check_room_capacity(correc, LIST_ROOM, capacity_dict)

    print(check_new_chr)

    # print(CHROMOSOME_1)

    # print(tb_c.check_room_capacity(CHROMOSOME_1, LIST_ROOM, LIST_UVS))

    # print(tb.planning_room(CHROMOSOME_1, 'B412'))
    # plannings = tb.planning_room(CHROMOSOME_1)
    # print(plannings)
    # occupee = tb_c.occupied(plannings)
    # print(occupee)

    # ubi = tb_c.check_not_ubiquity(plannings)
    # print(ubi)

    # print(tb.planning_teacher(CHROMOSOME_1, 'Nicolas SIMONCINI'))
