import pygame
from src.models.buttons.button import Button
from typing import Any


class ImageButton(Button):
    def __init__(self, x: int, y: int, info: Any, image: pygame.image):
        super().__init__(x, y, info)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def display_button(self, screen: pygame.Surface, *args):
        screen.blit(self.image, self.rect.topleft)

    def is_point_inside(self, x: int, y: int) -> bool:
        return self.rect.collidepoint(x, y)
