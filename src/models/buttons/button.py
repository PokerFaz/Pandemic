import pygame
from typing import Any


class Button:
    def __init__(self, x: int, y: int, info: Any):
        """
        Initializes button object

        :param x: positional argument by x
        :param y: positional argument by y
        :param info: what information it will hold

        Attributes:
        clickable: flag that shows whether it can be clicked
        """

        self.info = info
        self.clickable = True
        self.x = x
        self.y = y

    def display_button(self, screen: pygame.Surface, *args):
        """
        Function that will be overwritten by the class children

        :param screen: the screen where it will be displayed
        :param args: arguments necessary for displaying the button
        :return: nothing
        """
        pass

    def is_clicked(self, mouse_x: int, mouse_y: int) -> bool:
        """
        Checks if the button is pressed

        :param mouse_x: positional argument by x
        :param mouse_y: positional argument by y
        :return: true if clicked else false
        """

        if not self.clickable:
            return False

        if self.is_point_inside(mouse_x, mouse_y):
            return True

        return False

    def is_point_inside(self, x: int, y: int) -> bool:
        """
         Function that will be overwritten by the class children

        :param x: positional argument by x
        :param y: positional argument by y
        :return: true if it is inside else false
        """
        pass
