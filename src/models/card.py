from pygame import Surface
from src.misc.images import epidemic_image
from src.models.city import City


class Card:
    def __init__(self, card_type: str, name: str):
        self.card_type = card_type
        self.name = name

    def __str__(self):
        return f"Type: {self.card_type}, Name: {self.name}"


class CityCard(Card):
    def __init__(self, city: City, image: Surface):
        super().__init__("City Card", city.name)
        self.image = image
        self.rect = self.image.get_rect()


class EpidemicCard(Card):
    def __init__(self):
        super().__init__("Epidemic Card", "Epidemic card")
        self.image = epidemic_image


class EventCard(Card):
    def __init__(self, name: str, image: Surface):
        super().__init__("Event Card", name)
        self.image = image


class InfectionCard(Card):
    def __init__(self, city: City):
        super().__init__("Infection Card", city.name)
