from src.models.decks.deck import Deck
from src.models.city import City
from src.models.card import InfectionCard


class InfectionDeck(Deck):
    def __init__(self, cities: dict[str: City]):
        super().__init__()
        for city_info in cities.values():
            city_card = InfectionCard(city_info.name)
            self.deck.append(city_card)
