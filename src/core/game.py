"""Game class for managing the game state and flow."""
from .round import Round
from .deck import Deck

class Game:
    """Game class for managing the game state and flow."""
    def __init__(self, players):
        self.players = players
        self.hand_sizes = [3, 5, 7, 9, 11, 13, 11, 9, 7, 5, 3]
        self.scores = {player.name: 0 for player in players}
        self.rounds = []

    def start(self):
        """Start the game and manage the rounds."""
        for round_number, hand_size in enumerate(self.hand_sizes, start=1):
            print(f"\n=== Round {round_number} | Hand size: {hand_size} ===")
            self.prepare_round(hand_size)
            round_instance = Round(self.players)
            round_instance.round_number = round_number
            round_instance.start_bidding()
            round_instance.start_tricks()
            round_instance.score_round()
            self.update_scores()
            self.rounds.append(round_instance)

        print("\n🎉 Game Over! Final Scores:")
        self.display_final_scores()

    def prepare_round(self, hand_size):
        """Prepare the round by shuffling and dealing cards to players."""
        deck = Deck()
        deck.shuffle()
        hands = deck.deal(num_players=len(self.players), cards_per_player=hand_size)

        for player, hand in zip(self.players, hands):
            player.hand = hand
            player.bid = 0
            player.tricks_won = 0

    def update_scores(self):
        """Update scores based on the results of the round."""
        for player in self.players:
            if player.bid == player.tricks_won:
                score = 5 * player.tricks_won + 10
            else:
                score = (-5 * player.tricks_won) -10
            self.scores[player.name] += score

    def display_final_scores(self):
        """Display the final scores of all players."""
        for player, score in self.scores.items():
            print(f"{player}: {score}")
