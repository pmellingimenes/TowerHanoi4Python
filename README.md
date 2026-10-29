# TowerHanoi4Python - MG's Tower of Hanoi For Python
Welcome to MG's Tower of Hanoi for Python (3.8+) made with pygame.
## Before play
Install pygame-ce (the community edition of pygame, which works on current Python versions):

    python3 -m pip install pygame-ce

Plain `pygame` also works on older Python versions (up to 3.13).
## Playing the game
Execute the following command in the source code directory:

    python3 main.py

Pick the number of discs, then drag the top disc of a peg onto another peg.
Move the whole stack to the rightmost peg without ever putting a bigger disc on a smaller one.
## Code layout
- `hanoi.py` - the game rules (no pygame, easy to test)
- `models.py` - what gets drawn: colors, buttons and the board
- `main.py` - the app: screens, mouse handling and the main loop
