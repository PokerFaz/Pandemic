import json
import os
import pygame
from src.misc.constants import RED, YELLOW, BLUE, BLACK, color
from math import sqrt
from typing import Any, Iterable


def load_json_from_file(file_name: str) -> Any:
    with open(file_name) as f:
        data = json.load(f)
    return data


def find_file(file_name: str, starting_dir: str = ".") -> str | None:
    for root, dirs, files in os.walk(starting_dir):
        for file in files:
            if file == file_name:
                return os.path.join(root, file)

    return None


def join_path(*path_parts: str) -> str:
    return os.path.join(*path_parts)


def load_image(file_name: str) -> pygame.Surface:
    return pygame.image.load(file_name)


def resize(image: pygame.Surface, new_x: float, new_y: float) -> pygame.Surface:
    return pygame.transform.scale(image, (new_x, new_y))


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


def distance_between_two_points(p1_x: float, p1_y: float, p2_x: float, p2_y: float) -> float:
    return sqrt(abs((p2_x - p1_x) ** 2 + (p2_y - p1_y) ** 2))


def my_enumerate(iterable: Iterable, reset: int) -> tuple[int, int, Any]:
    index = 0
    breaks = 0
    for elem in iterable:
        if index == reset:
            index = 0
            breaks += 1
        yield breaks, index, elem
        index += 1
