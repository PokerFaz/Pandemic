from src.models.decks.deck import Deck
from src.models.city import City
from src.models.card import InfectionCard


class InfectionDeck(Deck):
    def __init__(self, cities: dict[str: City]):
        super().__init__()
        self.deck: list[InfectionCard] = [InfectionCard(city) for city in cities.values()]

    def __iter__(self):
        super().__iter__()

    def __str__(self) -> str:
        return str([card.name for card in self.deck])
