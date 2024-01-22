from src.models.buttons.button import Button
import pygame


class ImageButton(Button):
    def __init__(self, x: int, y: int, name: str, image: pygame.image):
        super().__init__(x, y, name)
        self.image = image
        self.info = name
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def display_button(self, screen: pygame.Surface, *args):
        screen.blit(self.image, self.rect.topleft)

    def is_point_inside(self, x: int, y: int) -> bool:
        return self.rect.collidepoint(x, y)
