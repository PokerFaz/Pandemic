import json
import os
import pygame
from src.misc.constants import RED, YELLOW, BLUE, BLACK, color
from math import sqrt
from typing import Any, Iterable


def load_json_from_file(file_name: str) -> Any:
    """
    Loads json file

    :param file_name: name of the file
    :return: Any
    """
    with open(file_name) as f:
        data = json.load(f)
    return data


def find_file(file_name: str, starting_dir: str = ".") -> str | None:
    """
    Finds a file in a directory

    :param file_name: target file name
    :param starting_dir: starting directory
    :return: path to get to the file or nothing
    """

    for root, dirs, files in os.walk(starting_dir):
        for file in files:
            if file == file_name:
                return join_path(root, file)

    return None


def join_path(*path_parts: str) -> str:
    """
    Combines multiple strings into a single file path.

    :param path_parts: parts of the file
    :return: the full path
    """
    return os.path.join(*path_parts)


def load_image(file_path: str) -> pygame.Surface:
    """
    Loads an image from path

    :param file_path: the path
    :return: surface that has the displayed image
    """
    return pygame.image.load(file_path)


def resize(image: pygame.Surface, new_size: tuple[float, float]) -> pygame.Surface:
    """
    Resizes the image

    :param image: the image to be resized
    :param new_size: the new dimensions
    :return: newly resized image surface
    """
    return pygame.transform.scale(image, new_size)


def from_str_to_color(color_name: str) -> color:
    """
    Converts a string representation of a color to a color.

    :param color_name: The name of the color to be converted.
    :return: the color
    """

    color_mapping = {
        "Red": RED,
        "Yellow": YELLOW,
        "Blue": BLUE,
        "Black": BLACK
    }

    return color_mapping.get(color_name)


def from_color_to_str(colour: color) -> str:
    """
    Converts a color to its name.

    :param colour: colour object
    :return: name of the color
    """

    color_mapping = {
        RED: "Red",
        YELLOW: "Yellow",
        BLUE: "Blue",
        BLACK: "Black"
    }

    return color_mapping.get(colour)


def distance_between_two_points(p1_x: float, p1_y: float, p2_x: float, p2_y: float) -> float:
    """
    Calculates the distance between two points

    :param p1_x: The x-coordinate of the first point.
    :param p1_y: The y-coordinate of the first point.
    :param p2_x: The x-coordinate of the second point.
    :param p2_y: The y-coordinate of the second point.
    :return: the distance between the two points
    """

    return sqrt(abs((p2_x - p1_x) ** 2 + (p2_y - p1_y) ** 2))


def my_enumerate(iterable: Iterable, reset: int) -> tuple[int, int, Any]:
    """
    Enumerates over an object with the option to reset the index.

    :param iterable: The iterable object to be enumerated.
    :param reset: The index at which to reset the enumeration.
    :return: [number of resets, current index, the elem itself]
    """

    index = 0
    breaks = 0
    for elem in iterable:
        if index == reset:
            index = 0
            breaks += 1
        yield breaks, index, elem
        index += 1
