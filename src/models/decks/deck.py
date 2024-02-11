import random
from src.models.card import Card


class Deck:
    """
    Class representing a deck of cards
    """

    def __init__(self):
        """
        Initializes a deck
        """

        self.deck: list[Card] = []

    def __len__(self) -> int:
        return len(self.deck)

    def __str__(self) -> str:
        info = [card.name for card in self.deck]
        return str(info)

    def __iter__(self) -> Card:
        for card in self.deck:
            yield card

    def add_cards(self, cards: list[Card] | Card):
        """
        Adds cards to the back of the deck

        :param cards: cards to be added
        :return: nothing
        """

        if not isinstance(cards, list):
            cards = [cards]

        self.deck.extend(cards)

    def shuffle(self):
        """
        Shuffles the deck

        :return: nothing
        """

        random.shuffle(self.deck)

    def remove_top_cards(self, number_of_removed_cards: int):
        """
        Removes the top cards from a deck

        :param number_of_removed_cards: number of cards to be removed
        :return: nothing
        """

        self.deck = self.deck[number_of_removed_cards:]

    def top_n_cards(self, number: int) -> list[Card]:
        """
        Gets the top n cards

        :param number: number of cards taken
        :return: list of cards
        """

        result = [card for card in self.deck[:number]]
        self.remove_top_cards(number)
        return result

    def get_bottom_card(self) -> Card:
        """
        Gets and removes the last card from a deck

        :return: card
        """
        return self.deck.pop()

    def add_to_front(self, cards: list[Card]):
        """
        Adds cards to the front of the deck

        :param cards: cards to be added
        :return: nothing
        """

        cards.extend(self.deck)
        self.deck = cards
