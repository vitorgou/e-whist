"""Round module for the card game."""

import random
from .card import Card
from .player import Player
from .deck import Deck

class Round:
    """Round class for managing the game round, including bidding and tricks."""
    def __init__(self, players: list[Player], round_number, starting_lead_player: Player):
        self.players = players
        self.round_number = round_number
        self.starting_player = starting_lead_player
        self.starting_lead_player_index = self.players.index(starting_lead_player)
        self.deck = Deck()
        self.trump_suit = self.choose_trump_suit()
        self.cards_played = []
        self.current_trick = []
        self.round_number = 1  # Track round number
        self.lead_index = 0
    
    def play_round(self):
        """Full round flow: bidding, tricks, and scoring."""
        print(f"\n=== Round {self.round_number} begins ===")
        print(f"Trump suit is: {self.trump_suit}\n")

        self.start_bidding()
        self.start_tricks()
        self.score_round()

    def choose_trump_suit(self) -> str:
        """Choose a random trump suit for this round."""
        return random.choice(Card.SUITS)

    def start_bidding(self):
        """Simulate a simple bidding phase. For now, all players bid 1."""
        print(f"Trump suit for round {self.round_number}: {self.trump_suit}")

        for player in self.players:
            player.trump_suit = self.trump_suit
            if player.is_human:
                print(f"\n{player.name}, your hand:")
                for i, card in enumerate(player.hand):
                    print(f"{i}: {card}")
            player.make_bid(max_possible=len(player.hand))  # Adjust this based on card count
            print(f"{player.name} bids {player.bid}")

    def start_tricks(self):
        """Start the trick phase of the round."""
        num_players = len(self.players)

        for trick_number in range(len(self.players[0].hand)):
            print(f"\nTrick {trick_number + 1} begins...")

            # Now we can correctly calculate
            lead_player_index = (self.starting_lead_player_index + trick_number) % num_players
            lead_player = self.players[lead_player_index]

            self.play_trick(lead_player)

    def play_trick(self, lead_player: Player):
        """Each player plays one card for the trick, starting from lead_player."""
        self.current_trick = []
        lead_suit = None
        num_players = len(self.players)
        trick_order = []

        # Find the index of the leading player
        lead_player_index = self.players.index(lead_player)

        # Build the trick order starting from the leading player
        for i in range(num_players):
            player_index = (lead_player_index + i) % num_players
            trick_order.append(self.players[player_index])

        # Now players play cards in correct order
        for i, player in enumerate(trick_order):
            played_card = None

            while played_card is None:
                played_card = player.play_card(
                    lead_suit=lead_suit,
                    validate_fn=self.validate_card_play
                )

                if i == 0:
                    lead_suit = played_card.suit

                self.current_trick.append(played_card)
                print(f"{player.name} plays {played_card}")

        self.determine_winner_of_trick(trick_order)


    def determine_winner_of_trick(self, trick_order: list):
        """Determine winner based on trick order and trump."""
        winning_card = self.current_trick[0]
        winning_player = trick_order[0]

        for i, card in enumerate(self.current_trick[1:], start=1):
            if self.is_card_winner(card, winning_card):
                winning_card = card
                winning_player = trick_order[i]

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
