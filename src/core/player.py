"""Player class for the game."""

class Player:
    """Represents a player in the game."""
    def __init__(self, name: str):
        self.name = name
        self.hand = []
        self.bid = None
        self.tricks_won = 0

    def receive_hand(self, cards: list):
        """Give the player their hand at the start of the round."""
        self.hand = cards
        self.sort_hand()

    def sort_hand(self):
        """Sort the hand by suit and rank (optional, but nice for consistency)."""
        self.hand.sort(key=lambda card: (card.suit, card.value))
        print(f"{self.name}'s hand sorted: {self.hand}")

    def make_bid(self, max_possible: int):
        """Placeholder for bidding logic. Can be overridden for AI or UI."""
        # For now, just always bid 1 for testing
        self.bid = 1

    def play_card(self, lead_suit: str = None):
        """Play a card from hand, respecting the lead suit if possible."""
        played_card = None
        
        # If there's a lead suit to follow
        if lead_suit is not None:
            # Check if the player has any card of the lead suit
            lead_cards = [card for card in self.hand if card.suit == lead_suit]
            
            if lead_cards:
                # If they have a card of the lead suit, play one of them
                played_card = self.hand.pop(self.hand.index(lead_cards[0]))  # Play the first lead suit card
            else:
                # If no cards of the lead suit, play any card
                if self.hand:  # Ensure the hand isn't empty
                    played_card = self.hand.pop(0)  # Play the first card
        else:
            # If there's no lead suit (first card), just play any card
            if self.hand:
                played_card = self.hand.pop(0)  # Play the first card

        return played_card


    def reset_for_new_round(self):
        """Reset player state for a new round."""
        self.hand = []
        self.bid = None
        self.tricks_won = 0

    def __repr__(self):
        return f"Player({self.name})"
