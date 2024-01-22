import pygame


class Button:
    def __init__(self, x: int, y: int, name: str):
        self.info = name
        self.clickable = True
        self.x = x
        self.y = y

    def display_button(self, screen: pygame.Surface, *args):
        pass

    def is_clicked(self, mouse_x: int, mouse_y: int):
        if not self.clickable:
            return False

        if self.is_point_inside(mouse_x, mouse_y):
            return True

        return False

    def is_point_inside(self, x: int, y: int):
        pass
