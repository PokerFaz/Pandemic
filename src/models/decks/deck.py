import random
from src.models.card import Card


class Deck:
    def __init__(self):
        self.deck: list[Card] = []

    def __len__(self) -> int:
        return len(self.deck)

    def __str__(self) -> str:
        info = [card.name for card in self.deck]
        return str(info)

    def __iter__(self) -> Card:
        for card in self.deck:
            yield card

    def add_cards(self, cards: list[Card]):
        self.deck.extend(cards)

    def shuffle(self):
        random.shuffle(self.deck)

    def remove_top_cards(self, number_of_removed_cards: int):
        self.deck = self.deck[number_of_removed_cards:]

    def top_n_cards(self, number: int) -> list[Card]:
        result = [city for city in self.deck[:number]]
        self.remove_top_cards(number)
        return result
