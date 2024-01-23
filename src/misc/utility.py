import json
import os
import pygame
from src.misc.constants import RED, YELLOW, BLUE, BLACK, color
from math import sqrt


def load_json_from_file(file_name: str):
    with open(file_name) as f:
        data = json.load(f)
    return data


def find_file(file_name: str, starting_dir: str = "."):
    for root, dirs, files in os.walk(starting_dir):
        for file in files:
            if file == file_name:
                return os.path.join(root, file)

    return None


def join_path(*path_parts):
    return os.path.join(*path_parts)


def load_image(file_name: str):
    return pygame.image.load(file_name)


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


def distance_between_two_points(p1_x: int, p1_y: int, p2_x: int, p2_y: int):
    return sqrt(abs((p2_x - p1_x) ** 2 + (p2_y - p1_y) ** 2))
