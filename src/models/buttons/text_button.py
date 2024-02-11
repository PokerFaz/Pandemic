import pygame
from src.models.buttons.button import Button
from src.misc.constants import GRAY, RED, color
from typing import Any


class TextButton(Button):
    def __init__(self, x: int, y: int, info: Any, width: int, height: int, text: str, text_size: int):
        """
        Initializes text button

        :param x: positional argument by x
        :param y: positional argument by y
        :param info: what information it holds
        :param width: width of the button
        :param height: height of the button
        :param text: what text will be displayed
        :param text_size: what will be the size of the displayed text
        """
        super().__init__(x, y, info)
        self.rect = pygame.Rect(x, y, width, height)
        self.text_size = text_size
        self.text = text

    def display_button(self, screen: pygame.Surface, rect_color: color = GRAY, text_color: color = RED, transparency: int = 0):
        """
        Displays a text button

        :param screen: on what screen it will be displayed
        :param rect_color: the color of the rectangle when displayed
        :param text_color: the color of the text
        :param transparency: the transparency of the rectangle
        :return: nothing
        """

        if transparency == 0:
            pygame.draw.rect(screen, rect_color, self.rect)

        font = pygame.font.Font(None, self.text_size)
        text = font.render(self.text, True, text_color)

        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def is_point_inside(self, x: int, y: int) -> bool:
        """
        Checks if the click was inside the rectangle of the text button

        :param x: positional argument by x from the mouse click
        :param y: positional argument by x from the mouse click
        :return: true if inside else false
        """

        return self.rect.collidepoint(x, y)
