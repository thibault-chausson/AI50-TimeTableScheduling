import toolbox as tb
import toolbox_correction as tb_c
import toolbox_student as tb_s


def correction_room(arg_chr, arg_room_capacity_dict, room_list, capacity_uv_promo_dict):
    fct_plannings = tb.planning_room(arg_chr)
    fct_ubiquity = tb_c.check_not_ubiquity(fct_plannings)
    # Check ubiquity
    if not fct_ubiquity[1]:
        for ubi in fct_ubiquity[0]:
            if not ubi[0]:
                room_name = ubi[1]
                for planning in fct_plannings:
                    if planning[1] == room_name:
                        planning_room = planning[0]
                        arg_chr, _ = tb_c.change_room_ubiquity(arg_chr, room_name, planning_room, fct_plannings)
                        break
    fct_plannings = tb.planning_room(arg_chr)
    fct_occupied = tb_c.occupied(fct_plannings)
    fct_room_too_small = tb_c.check_room_capacity(arg_chr, arg_room_capacity_dict, capacity_uv_promo_dict)
    correc, _ = tb_c.change_room_if_overcrowded_and_free(arg_chr, fct_room_too_small, room_list, fct_occupied,
                                                         capacity_uv_promo_dict)
    return correc


def correction_teacher(arg_chr):
    fct_plannings_teacher = tb.planning_teacher(arg_chr)
    fct_ubiquity = tb_c.check_not_ubiquity(fct_plannings_teacher)
    if not fct_ubiquity[1]:
        for ubi in fct_ubiquity[0]:
            if not ubi[0]:  # On bouge le cours du prof
                teacher_name = ubi[1]  # On récupère le nom du prof
                for planning in fct_plannings_teacher:
                    if planning[1] == teacher_name:
                        # On récupère le planning du prof
                        planning_teacher = planning[0]
                        arg_chr = tb_c.change_timeslot_teacher_occupied(arg_chr, teacher_name, planning_teacher)
                        break
    return arg_chr


if __name__ == '__main__':
    CHROMOSOME_1 = tb.import_population("datas/chromosome_1.json")[0]
    LIST_ROOM = tb.get_rooms()
    LIST_UVS = tb.import_uvs()
    PROMO = tb_s.import_promo()
    plannings = tb.planning_room(CHROMOSOME_1)
    occupee = tb_c.occupied(plannings)
    ubiquity = tb_c.check_not_ubiquity(plannings)
