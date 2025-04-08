""" Deck class for card games """

import random
from .card import Card

class Deck:
    """Deck class for a standard deck of playing cards."""
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in Card.SUITS for rank in Card.RANKS]

    def shuffle(self):
        """Shuffle the deck of cards."""
        random.shuffle(self.cards)

    def deal(self, num_players: int, cards_per_player: int) -> list:
        """Deal cards to players."""
        if num_players * cards_per_player > len(self.cards):
            raise ValueError("Not enough cards to deal")

        hands = [[] for _ in range(num_players)]
        for _ in range(cards_per_player):
            for player_hand in hands:
                player_hand.append(self.cards.pop())

        return hands

    def remaining(self) -> int:
        """Amount of cards remaining in the deck."""
        return len(self.cards)
