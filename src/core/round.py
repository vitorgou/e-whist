"""Round module for the card game."""

import random
from .card import Card
from .player import Player
from .deck import Deck

class Round:
    """Round class for managing the game round, including bidding and tricks."""
    def __init__(self, players: list):
        self.players = players
        self.deck = Deck()
        self.trump_suit = self.choose_trump_suit()
        self.cards_played = []
        self.current_trick = []
        self.round_number = 1  # Track round number

    def choose_trump_suit(self) -> str:
        """Choose a random trump suit for this round."""
        return random.choice(Card.SUITS)

    def start_bidding(self):
        """Simulate a simple bidding phase. For now, all players bid 1."""
        print(f"Trump suit for round {self.round_number}: {self.trump_suit}")
        for player in self.players:
            player.make_bid(max_possible=5)  # Adjust this based on card count
            print(f"{player.name} bids {player.bid}")

    def start_tricks(self):
        """Start the trick phase of the round."""
        for trick_number in range(len(self.players[0].hand)):
            print(f"\nTrick {trick_number + 1} begins...")
            self.play_trick()

    def play_trick(self):
        """Each player plays one card for the trick."""
        self.current_trick = []
        lead_suit = None  # Keep track of the lead suit

        for i, player in enumerate(self.players):
            played_card = None

            while played_card is None:
                # Ask the player to play a card
                played_card = player.play_card(lead_suit)

                # If it's not the first card, validate the card
                if lead_suit is not None:
                    try:
                        self.validate_card_play(player, played_card, lead_suit)
                    except ValueError as e:
                        print(e)  # Display the error message if a player violates the rules
                        played_card = None  # Reset played card to allow retry
                        continue  # Let the player retry playing a valid card

                # Set the lead suit if it's the first player
                elif i == 0:
                    lead_suit = played_card.suit  # First card determines the lead suit
                # If valid, append the card to the trick
                self.current_trick.append(played_card)
                print(f"{player.name} plays {played_card}")


        self.determine_winner_of_trick()





    def determine_winner_of_trick(self):
        """Determine the winner of the trick based on trump and the lead suit."""
        winning_card = self.current_trick[0]
        winning_player = self.players[0]

        # Simple logic: highest card wins (trump suit > others, same suit wins by rank)
        for i, card in enumerate(self.current_trick[1:], start=1):
            if self.is_card_winner(card, winning_card):
                winning_card = card
                winning_player = self.players[i]

        print(f"{winning_player.name} wins the trick with {winning_card} \n")
        winning_player.tricks_won += 1

    def is_card_winner(self, card, current_winner_card):
        """Check if the card is a winner based on the trump suit and ranks."""
        if card.suit == self.trump_suit and current_winner_card.suit != self.trump_suit:
            return True
        if card.suit == current_winner_card.suit and card.value > current_winner_card.value:
            return True
        return False

    def score_round(self):
        """Score the round based on the players' bids and tricks won."""
        for player in self.players:
            if player.bid == player.tricks_won:
                score = 5 * player.tricks_won + 10  # Correct bid, earn extra points
            else:
                score = (-5 * player.tricks_won) -10  # Incorrect bid, lose points

            print(f"{player.name} scored {score} points")
            player.tricks_won = 0  # Reset for next round (or a scoring phase)

    def validate_card_play(self, player: Player, card: Card, lead_suit: str):
        """Ensure that players follow the rules regarding suit and trump cards."""
        if lead_suit and card.suit != lead_suit and self.suit_in_hand(player, lead_suit):
            raise ValueError(f"{player.name} must follow the lead suit!")

        if card.suit == self.trump_suit and not self.has_non_trump_cards(player):
            # If leading with a trump, check that it's their only suit
            if self.suit_in_hand(player, self.trump_suit) != len(player.hand):
                raise ValueError(f"{player.name} cannot lead with a trump suit unless it's their only suit!")

    def suit_in_hand(self, player: Player, suit: str) -> int:
        """Check how many cards the player has of a specific suit."""
        return sum(1 for card in player.hand if card.suit == suit)

    def has_non_trump_cards(self, player: Player) -> bool:
        """Check if the player has any non-trump cards left in hand."""
        return any(card.suit != self.trump_suit for card in player.hand)
