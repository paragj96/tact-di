height_map = {}
scaling_factor = 0.9


def get_height_map():
    return height_map


def set_height_map(mapping):
    global height_map
    height_map = mapping


def get_scaling_factor():
    return scaling_factor


def set_scaling_factor(num):
    global scaling_factor
    scaling_factor = num