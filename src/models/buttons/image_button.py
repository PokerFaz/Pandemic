import pygame
from src.models.buttons.button import Button
from typing import Any


class ImageButton(Button):
    def __init__(self, x: int, y: int, info: Any, image: pygame.image):
        """
        Initializes image button objects

        :param x: positional argument by x
        :param y: positional argument by y
        :param info: what information the button holds
        :param image: the image of the button
        """

        super().__init__(x, y, info)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def display_button(self, screen: pygame.Surface, *args):
        """
        Displays an image button

        :param screen: on what screen it will be displayed
        :param args: none used here
        :return: nothing
        """

        screen.blit(self.image, self.rect.topleft)

    def is_point_inside(self, x: int, y: int) -> bool:
        """
        Checks if the click is inside the button

        :param x: positional argument by x
        :param y: positional argument by y
        :return: true if inside else false
        """

        return self.rect.collidepoint(x, y)
