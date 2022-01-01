from ..strings.keys import *
from ..strings.errors import *
from notraffic.app.models.zone import zone_name_max_length


def validate_zone(zone, is_edit=False):
    print(f'validate_zone: {zone}')

    if api_name not in zone and not is_edit:
        return validation_error_is_required.format(api_name)

    if api_name in zone and (not isinstance(zone[api_name], str) or len(zone[api_name]) == 0 or len(
            zone[api_name]) > zone_name_max_length):
        return validation_error_empty_string.format(api_name, zone_name_max_length)

    if api_min_x not in zone and not is_edit:
        return validation_error_is_required.format(api_min_x)

    if api_min_x in zone and (not isinstance(zone[api_min_x], int) or zone[api_min_x] < 0):
        return validation_error_wrong_int.format(api_min_x)

    if api_max_x not in zone and not is_edit:
        return validation_error_is_required.format(api_max_x)

    if api_max_x in zone and (not isinstance(zone[api_max_x], int) or zone[api_max_x] < 0):
        return validation_error_wrong_int.format(api_max_x)

    if api_min_x in zone and api_max_x in zone:
        if zone[api_min_x] >= zone[api_max_x]:
            return validation_error_need_to_be_larger.format(api_max_x, api_min_x)

    if api_min_y not in zone and not is_edit:
        return validation_error_is_required.format(api_min_y)

    if api_min_y in zone and (not isinstance(zone[api_min_y], int) or zone[api_min_y] < 0):
        return validation_error_wrong_int.format(api_min_y)

    if api_max_y not in zone and not is_edit:
        return validation_error_is_required.format(api_max_y)

    if api_max_y in zone and (not isinstance(zone[api_max_y], int) or zone[api_max_y] < 0):
        return validation_error_wrong_int.format(api_max_y)

    if api_min_y in zone and api_max_y in zone:
        if zone[api_min_y] >= zone[api_max_y]:
            return validation_error_need_to_be_larger.format(api_max_y, api_min_y)

    return None
