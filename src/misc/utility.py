import json
from src.misc.constants import RED, YELLOW, BLUE, BLACK, color


def load_json_from_file(file_name: str):
    with open(file_name) as f:
        data = json.load(f)
    return data


def from_str_to_color(color_name: str) -> color:
    color_mapping = {
        "Red": RED,
        "Yellow": YELLOW,
        "Blue": BLUE,
        "Black": BLACK
    }

    return color_mapping.get(color_name)


def from_color_to_str(colour: color) -> str:
    color_mapping = {
        RED: "Red",
        YELLOW: "Yellow",
        BLUE: "Blue",
        BLACK: "Black"
    }

    return color_mapping.get(colour)
