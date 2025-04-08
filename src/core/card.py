"""Card class for a standard deck of playing cards."""

class Card:
    """Basic card class for a standard deck of playing cards."""
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    RANK_VALUES = {rank: index for index, rank in enumerate(RANKS, start=2)}

    def __init__(self, suit: str, rank: str):
        if suit not in Card.SUITS:
            raise ValueError(f"Invalid suit: {suit}")
        if rank not in Card.RANKS:
            raise ValueError(f"Invalid rank: {rank}")

        self.suit = suit
        self.rank = rank
        self.value = Card.RANK_VALUES[rank]  # Useful for comparing cards

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank
