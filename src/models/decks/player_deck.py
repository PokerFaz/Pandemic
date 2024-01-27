from src.models.decks.deck import Deck
from src.models.city import City
from src.models.card import CityCard, EpidemicCard, EventCard
import random
from src.misc.utility import load_image


class PlayerDeck(Deck):
    def __init__(self, cities: dict[str: City]):
        super().__init__()
        self.deck: list[EventCard | CityCard | EpidemicCard] = [CityCard(city, load_image(city.image)) for city in cities.values()]

    # ADDS EPIDEMIC CARDS TO THE PLAYER DECK BASED ON THE DIFFICULTY
    def prepare_deck(self, difficulty: str):
        number_of_epidemic_cards = 4 if difficulty == "EASY" else (5 if difficulty == "NORMAL" else 6)
        cards_per_deck = int(len(self.deck) / number_of_epidemic_cards)
        epidemic_card = EpidemicCard()

        # SPLITS THE INTERVAL INTO SMALL INTERVALS BASED ON NUM OF EPIDEMIC CARDS AND RANDOMLY CHOOSES ONE NUMBER FROM EACH INTERVAL
        random_indices = [random.choice(range(start, end)) for start, end in
                          zip(range(0, len(self.deck), cards_per_deck),
                              range(cards_per_deck, len(self.deck) + 1, cards_per_deck))]

        result = []
        for i, card in enumerate(self.deck):
            if i in random_indices:
                result.append(epidemic_card)
            result.append(card)

        self.deck = result

    def get_cards(self, number: int) -> list[EventCard | CityCard | EpidemicCard]:
        result = [city for city in self.deck[:number]]
        self.remove_top_cards(number)
        return result
