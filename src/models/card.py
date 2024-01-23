from pygame import Surface


class Card:
    def __init__(self, card_type: str, name: str):
        self.card_type = card_type
        self.name = name

    def __str__(self):
        return f"Type: {self.card_type}"


class CityCard(Card):
    def __init__(self, city: str, image: Surface):
        super().__init__("City Card", city)
        self.image = image
        self.rect = self.image.get_rect()


class EpidemicCard(Card):
    def __init__(self):
        super().__init__("Epidemic Card", "epidemic_card")


class EventCard(Card):
    def __init__(self, name: str):
        super().__init__("Event Card", name)


class InfectionCard(Card):
    def __init__(self, city: str):
        super().__init__("Infection Card", city)
