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
        self.trump_suit = None  # This will be set during the round

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
            self.bid = self.calculate_bid(max_possible)

    def calculate_bid(self, max_possible):
        """Simple AI logic to calculate a bid based on hand strength."""
        score = 0
        trump_count = sum(1 for card in self.hand if card.suit == self.trump_suit)
        high_cards = [card for card in self.hand if card.rank in ['A', 'K', 'Q']]

        score += len(high_cards)
        score += trump_count * 0.5  # Trump cards are valuable

        # Bonus for longer suits (more than 2 of same suit)
        suit_counts = {}
        for card in self.hand:
            suit_counts[card.suit] = suit_counts.get(card.suit, 0) + 1
        long_suits = sum(1 for count in suit_counts.values() if count >= 3)
        score += long_suits * 0.5

        # Round to nearest whole number but not above max_possible
        bid = min(max_possible, round(score))
        return bid

# Play card logic block
    def play_card(self, lead_suit: str = None, validate_fn=None):
        """Play a card from hand, respecting the lead suit if possible."""
        
        if self.is_human:
            return self.play_card_human(lead_suit, validate_fn)
        else:
            return self.play_card_ai(lead_suit)
    # Human player logic
    def play_card_human(self, lead_suit=None, validate_fn=None):
        """Human player logic for playing a card."""
        while True:
            print(f"\n{self.name}'s hand:")
            for idx, card in enumerate(self.hand):
                print(f"{idx + 1}: {card}")

            try:
                choice = int(input("Choose a card to play (1 - {}): ".format(len(self.hand))))
                if 1 <= choice <= len(self.hand):
                    chosen_card = self.hand[choice - 1]

                    # Validate the card choice using game's rule
                    if validate_fn:
                        try:
                            validate_fn(self, chosen_card, lead_suit)
                        except ValueError as e:
                            print(f"Invalid card: {e}")
                            continue  # Ask again

                    self.hand.remove(chosen_card)
                    return chosen_card
                else:
                    print("Invalid number. Try again.")
            except ValueError:
                print("Please enter a valid number.")

    # AI player logic
    def play_card_ai(self, lead_suit=None):
        """AI logic for playing a card."""
        # Get valid cards (must follow suit if possible)
        valid_cards = self.get_valid_cards(lead_suit)

        # If bid is met or exceeded, avoid winning!
        if self.tricks_won >= self.bid:
            return self.play_safest_card(valid_cards)

        # If leading, play low
        if lead_suit is None:
            return self.play_low_card(valid_cards)

        # Otherwise, try to win (e.g., play strongest card)
        return self.play_best_card(valid_cards)

    def get_valid_cards(self, lead_suit):
        """Get valid cards to play based on the lead suit."""
        if not lead_suit:
            return self.hand.copy()
        return [card for card in self.hand if card.suit == lead_suit] or self.hand.copy()
    
    def play_low_card(self, cards):
        """Play the lowest card in hand."""
        non_trump = [c for c in cards if c.suit != self.trump_suit]
        if non_trump:
            return self.remove_card(min(non_trump, key=lambda c: c.value))
        return self.remove_card(min(cards, key=lambda c: c.value))

    def play_best_card(self, cards):
        """Play the highest card in hand."""
        trump_cards = [c for c in cards if c.suit == self.trump_suit]
        if trump_cards:
            return self.remove_card(max(trump_cards, key=lambda c: c.value))
        return self.remove_card(max(cards, key=lambda c: c.value))
    
    def play_safest_card(self, cards):
        """Play the safest card to avoid winning."""
        non_trump = [c for c in cards if c.suit != self.trump_suit]
        if non_trump:
            return self.remove_card(min(non_trump, key=lambda c: c.value))
        return self.remove_card(min(cards, key=lambda c: c.value))
    
    def remove_card(self, card):
        """Remove a card from the player's hand."""
        self.hand.remove(card)
        return card

# Resetting the round
    def reset_for_new_round(self):
        """Reset player state for a new round."""
        self.hand = []
        self.bid = None
        self.tricks_won = 0

    def __repr__(self):
        return f"Player({self.name})"
