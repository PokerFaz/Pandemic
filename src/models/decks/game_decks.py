from src.models.decks.player_deck import PlayerDeck
from src.models.decks.infection_deck import InfectionDeck
from src.models.decks.deck import Deck
from src.models.city import City


class GameDecks:
    """
    Represents all decks used in Pandemic
    """

    def __init__(self):
        """
        Initializes all the decks
        """

        self.player_deck = PlayerDeck({})
        self.players_discard_pile = PlayerDeck({})
        self.infection_deck = InfectionDeck({})
        self.infection_discard_pile = InfectionDeck({})

    def setup(self, cities: dict[str, City]):
        """
        Sets up all the decks

        :param cities: used for making the decks
        :return: nothing
        """

        self.player_deck = PlayerDeck(cities)
        self.players_discard_pile = Deck()
        self.player_deck.shuffle()

        self.infection_deck = InfectionDeck(cities)
        self.infection_discard_pile = Deck()
        self.infection_deck.shuffle()

    def prepare_player_deck(self, difficulty: str):
        """
        Adds the epidemic cards to the player deck

        :param difficulty: the board's difficulty
        :return: nothing
        """

        self.player_deck.prepare_deck(difficulty)
