""" Main entry point for the e-whist game. """
# src/main.py

from core.deck import Deck
from core.round import Round
from core.player import Player

NUM_PLAYERS = 4
CARDS_PER_PLAYER = 3

def main():
    """Main function to run the e-whist game."""
    print("Welcome to e-whist!")

    # Initialize players
    players = [Player(f"Player {i+1}") for i in range(NUM_PLAYERS)]

    # Create and shuffle the deck
    deck = Deck()
    deck.shuffle()

    # Deal cards to players
    hands = deck.deal(NUM_PLAYERS, CARDS_PER_PLAYER)
    for player, hand in zip(players, hands):
        player.receive_hand(hand)

    # Start the round
    round_1 = Round(players)
    round_1.start_bidding()
    round_1.start_tricks()
    round_1.score_round()

if __name__ == "__main__":
    main()
