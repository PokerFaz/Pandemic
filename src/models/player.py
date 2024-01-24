from pygame.sprite import Sprite
from pygame import Surface


class Player(Sprite):
    def __init__(self, name: str, player_image: Surface, x: int, y: int, offset_by_x: int):
        Sprite.__init__(self)
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
        self.rect.center = (x + 5 + self.offset_by_x, y - 25)
        self.city = city
        self.moves -= 1
        print(f"Player successfully moved to {city}")

    def draw(self, cards: list[str]):
        self.cards.extend(cards)

    def remove_cards(self, cards: list[str]):
        for card in cards:
            self.cards.remove(card)

    def replenish_moves(self):
        self.moves = 4

    def has(self, city_name: str) -> bool:
        for card in self.cards:
            if card == city_name:
                return True

        return False
