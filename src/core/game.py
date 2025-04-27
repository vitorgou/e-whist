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
        self.starting_lead_player_index = 0  # First round: Player 0 leads

    def play(self):
        """Play the game for a fixed number of rounds."""
        for round_number in range(1, 12):  # 11 rounds
            # Rotate who leads
            leading_player = self.players[self.starting_lead_player_index % len(self.players)]

            round_instance = Round(self.players, round_number, leading_player)
            round_instance.play_round()

            # After each round, next player leads
            self.starting_lead_player_index += 1

    def start(self):
        """Start the game and manage the rounds."""
        for round_number, hand_size in enumerate(self.hand_sizes, start=1):
            print(f"\n=== Round {round_number} | Hand size: {hand_size} ===")
            self.prepare_round(hand_size)

            starting_lead_player = self.players[self.starting_lead_player_index % len(self.players)]
            round_instance = Round(self.players, round_number, starting_lead_player)
            round_instance.hand_size = hand_size  # Optional if Round needs it

            # Instead of three method calls, just one
            round_instance.play_round()

            self.update_scores()
            self.rounds.append(round_instance)
            self.starting_lead_player_index += 1

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
