import toolbox as tb
import toolbox_correction as tb_c
import toolbox_student as tb_s


def correction_room(arg_chr, arg_room_capacity_dict, room_list, capacity_uv_promo_dict):
    fct_plannings = tb.planning_room(arg_chr)
    fct_occupee = tb_c.occupied(fct_plannings)
    fct_room_too_small = tb_c.check_room_capacity(arg_chr, arg_room_capacity_dict, capacity_uv_promo_dict)
    correc, _ = tb_c.change_room_if_overcrowded_and_free(arg_chr, fct_room_too_small, room_list, fct_occupee,
                                                         capacity_uv_promo_dict)
    return correc


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

    corrige = correction_room(CHROMOSOME_1, room_capacity_dict, LIST_ROOM, capacity_dict)

    print("corrige", corrige)

    print("check", tb_c.check_room_capacity(corrige, room_capacity_dict, capacity_dict))