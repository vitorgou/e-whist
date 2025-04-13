"""Main entry point for the e-whist game."""
from core.player import Player
from core.game import Game

NUM_PLAYERS = 4

def main():
    """Main function to start the e-whist game."""
    print("🎴 Welcome to e-whist!")

    # Ask how many human players
    while True:
        try:
            num_humans = int(input(f"How many human players? (0–{NUM_PLAYERS}): "))
            if 0 <= num_humans <= NUM_PLAYERS:
                break
            else:
                print("Invalid number.")
        except ValueError:
            print("Please enter a number.")

    # Create players based on input
    players = []
    for i in range(NUM_PLAYERS):
        is_human = i < num_humans
        name = input(f"Enter name for {'Human' if is_human else 'Computer'} Player {i+1}: ")
        players.append(Player(name=name, is_human=is_human))

    # Start the game
    game = Game(players)
    game.start()

if __name__ == "__main__":
    main()
