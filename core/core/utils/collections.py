from typing import Collection


def deep_update(base_dict, update_with):
    # Iterate over each item in the new dict
    for key, value in update_with.items():
        # if the value is a dict
        if isinstance(value, dict):
            base_dict_value = base_dict.get(key)
            # if  the original value is also a dict then run it through this same function
            if isinstance(base_dict_value, dict):
                deep_update(base_dict_value, value)
                # if the original value is NOT a dict then just set the new value
            else:
                base_dict[key] = value
                # if the new value is not a dict
        else:
            base_dict[key] = value

    return base_dict


def remove_keys(dict_: dict, keys: Collection):
    for key in keys:
        del dict_[key]
    return dict_
