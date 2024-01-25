from src.models.decks.deck import Deck
from src.models.city import City
from src.models.card import InfectionCard


class InfectionDeck(Deck):
    def __init__(self, cities: dict[str: City]):
        super().__init__()
        self.deck = [InfectionCard(city_info.name) for city_info in cities.values()]

    def __iter__(self):
        for card in self.deck:
            yield card
