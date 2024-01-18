import pygame.sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, name, player_image, x, y, offset_by_x):
        super().__init__()
        self.name = name
        self.city = "Atlanta"
        self.cards = []
        self.image = player_image
        self.rect = self.image.get_rect()
        self.moves = 4
        self.offset_by_x = offset_by_x
        self.rect.center = (x, y)

    def __str__(self):
        return f"{self.name} is currently in {self.city}. They have {len(self.cards)} cards: {self.cards}"

    def move(self, x: int, y: int, city: str):
        self.rect.center = (x+5+self.offset_by_x, y-25)
        self.city = city
        self.moves -= 1
        print(f"Player successfully moved to {city}")

    def draw(self, cards):
        self.cards.extend(cards)

    def replenish_moves(self):
        self.moves = 4


