"""Player class for the game."""
import random

class Player:
    """Represents a player in the game."""
    def __init__(self, name, is_human=False):
        self.name = name
        self.is_human = is_human
        self.hand = []
        self.bid = 0
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
        """Bidding logic for the player."""
        if self.is_human:
            while True:
                try:
                    bid = int(input(f"{self.name}, enter your bid (0 to {max_possible}): "))
                    if 0 <= bid <= max_possible:
                        self.bid = bid
                        break
                    else:
                        print("Invalid bid.")
                except ValueError:
                    print("Please enter a number.")
        else:
            self.bid = random.randint(0, max_possible)


    def play_card(self, lead_suit: str = None, validate_fn=None):
        """Play a card from hand, respecting the lead suit if possible."""
        played_card = None
        if self.is_human:
            while True:
                print(f"\n{self.name}, it's your turn to play.")
                print("Your hand:")
                for i, card in enumerate(self.hand):
                    print(f"{i}: {card}")
                try:
                    choice = int(input("Choose the index of the card to play: "))
                    if 0 <= choice < len(self.hand):
                        chosen_card = self.hand[choice]

                        # Validate if a validator was passed (Round should pass one)
                        if validate_fn:
                            try:
                                validate_fn(self, chosen_card, lead_suit)
                                return self.hand.pop(choice)
                            except ValueError as e:
                                print(f"Invalid move: {e}")
                        else:
                            return self.hand.pop(choice)
                    else:
                        print("Invalid index.")
                except ValueError:
                    print("Please enter a number.")
        else:
            
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
