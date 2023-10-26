import pygame.sprite
from Board import City


class Player(pygame.sprite.Sprite):
    def __init__(self, name,  player_image, x=278, y=257):
        super().__init__()
        self.name = name
        self.city = "Atlanta"
        self.cards = []
        self.image = player_image
        self.rect = self.image.get_rect()
        self.moves = 4
        self.rect.center = (x, y)

    def __str__(self):
        player_cards_names = []
        for card in self.cards:
            player_cards_names.append(card.city_name)
        return f"{self.name} is currently in {self.city}. They have {len(self.cards)} cards: {player_cards_names[0:]}"

    def move(self, x, y):
        self.rect.center = (x+5, y-25)
        print(f"Player successfully moved to {self.city} ")

