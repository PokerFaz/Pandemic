from src.models.buttons.button import Button
import pygame
from src.misc.constants import GRAY, RED, color


class TextButton(Button):
    def __init__(self, x: int, y: int, name: str, width: int, height: int, text: str, text_size: int):
        super().__init__(x, y, name)
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
