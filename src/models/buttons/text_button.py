import pygame
from src.models.buttons.button import Button
from src.misc.constants import GRAY, RED, color
from typing import Any


class TextButton(Button):
    def __init__(self, x: int, y: int, info: Any, width: int, height: int, text: str, text_size: int):
        super().__init__(x, y, info)
        self.rect = pygame.Rect(x, y, width, height)
        self.text_size = text_size
        self.text = text

    def display_button(self, screen: pygame.Surface, rect_color: color = GRAY, text_color: color = RED, transparency: int = 0):
        if transparency == 0:
            pygame.draw.rect(screen, rect_color, self.rect)

        font = pygame.font.Font(None, self.text_size)
        text = font.render(self.text, True, text_color)

        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def is_point_inside(self, x: int, y: int) -> bool:
        return self.rect.collidepoint(x, y)
