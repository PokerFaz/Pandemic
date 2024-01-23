import random
from src.models.card import Card


class Deck:
    def __init__(self):
        self.deck = []

    def __len__(self) -> int:
        return len(self.deck)

    def __str__(self) -> str:
        info = [card.name for card in self.deck]
        return str(info)

    def add_cards(self, cards: list[Card]):
        self.deck.extend(cards)

    def shuffle(self):
        random.shuffle(self.deck)

    def remove_top_cards(self, number_of_removed_cards: int):
        self.deck = self.deck[number_of_removed_cards:]

    def get_cards(self, number: int) -> list[str]:
        return [city.name for city in self.deck[:number]]