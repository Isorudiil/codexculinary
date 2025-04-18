from fractions import Fraction
import re

def parse_ingredient_details(ingredient_details_str):
    """
    Turns string of ingredient details into nested dictionary
    """

    # data missing entirely
    ingredient_dict = {}
    if not ingredient_details_str:
        return None
        
    str_split = re.split(r'\s+', ingredient_details_str.strip())

    # too few arguments
    if len(str_split) < 3:
        return None

    name = " ".join(str_split[0:-2]).strip(":").strip(" ")
    
    quantity = str_split[-2:-1]
    if len(quantity) == 1:
        float_qty = float(Fraction(quantity[0]))
    # too many arguments for quantity
    else:
        return None

    unit = str_split[-1:]
    if len(unit) == 1:
        str_unit = str(unit[0])
    # too many arguments for units
    else:
        return None

    ingredient_dict[name.capitalize()] = {"quantity": float_qty, "unit": str_unit}
    return ingredient_dict

def separate_by_comma(comma_separated):
    new_list = []
    item_list = comma_separated.split(", ")
    for item in item_list:
        new_list.append(item)
    return new_list
