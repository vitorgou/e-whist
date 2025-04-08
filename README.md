# E-whist
E-Whist game

## Project roadmap
### First iteration

Core Logic MVP (Minimum Viable Product) Start with a console-version of the game to test:

Deck + shuffling

Dealing cards to players

Bidding system

Trick-playing rules

Scoring system

This gets your game playable even if it's ugly.

Then get assets (once you know what you need)

Card images

Fonts for score display or menus

Sounds (optional for now)

UI ideas will flow more easily once you’ve played the game a bit.

Then build your Pygame UI layer You’ll wrap the tested core logic with visuals and interactions:

Card animations

Drag-and-drop or click-based play

Turn indicators, bidding UI, etc.

## Folder structure

e-whist/
│
├── assets/                     # Images, sounds, fonts, etc.
│   ├── cards/
│   ├── sounds/
│   └── fonts/
│
├── src/                        # All source code lives here
│   ├── core/                   # Core game logic (card classes, game loop, state management)
│   │   ├── card.py
│   │   ├── deck.py
│   │   ├── player.py
│   │   ├── round.py
│   │   └── game.py
│   │
│   ├── ui/                     # UI handling (menus, buttons, animations, drawing)
│   │   ├── screen_manager.py
│   │   ├── menu_screen.py
│   │   ├── game_screen.py
│   │   └── ui_elements.py
│   │
│   ├── ai/                     # AI logic for bot players (can be expanded later)
│   │   └── ai_player.py
│   │
│   ├── config/                 # Constants and settings
│   │   └── settings.py
│   │
│   └── main.py                 # Entry point to the game
│
├── tests/                      # Unit tests for all modules
│   ├── test_deck.py
│   ├── test_player.py
│   └── ...
│
├── requirements.txt            # Dependencies
├── README.md                   # Game overview, how to play, how to run
├── LICENSE
└── setup.py                    # For future packaging/deployment

