from pygame.sprite import Sprite
from pygame import Surface
from src.misc.images import back_image
from src.models.card import EventCard, CityCard


class Player(Sprite):
    def __init__(self, name: str = "", player_image: Surface = back_image, x: int = 0, y: int = 0, offset_by_x: int = 0):
        Sprite.__init__(self)
        self.name = name
        self.location = "Atlanta"
        self.cards: list[EventCard, CityCard] = []
        self.image = player_image
        self.rect = self.image.get_rect()
        self.moves = 4
        self.offset_by_x = offset_by_x
        self.rect.center = (x, y)

    def __str__(self):
        return f"{self.name} is currently in {self.location}. They have {len(self.cards)} cards: {self.cards}"

    def move(self, x: int, y: int, city: str):
        self.rect.center = (x + 5 + self.offset_by_x, y - 25)
        self.location = city
        self.moves -= 1

    def draw(self, cards: list[EventCard | CityCard]):
        self.cards.extend(cards)

    def remove_cards(self, cards: list[EventCard | CityCard]):
        for card in cards:
            self.cards.remove(card)

    def replenish_moves(self):
        self.moves = 4

    def has(self, city_name: str) -> bool:
        for card in self.cards:
            if card.name == city_name:
                return True

        return False
