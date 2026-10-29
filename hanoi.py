"""
MG's Tower of Hanoi for Python - Game Rules Module
Pure game logic, no pygame here, so it can be tested on its own.
"""
class Hanoi():
    def __init__(self, n_discs):
        self.n_discs = n_discs
        # Each peg is a list of disc sizes, bottom to top (n_discs is the biggest)
        self.pegs = [list(range(n_discs, 0, -1)), [], []]
        self.moves = 0
    @property
    def min_moves(self):
        return 2 ** self.n_discs - 1
    def top(self, peg):
        return self.pegs[peg][-1] if self.pegs[peg] else None
    def can_move(self, src, dst):
        if src == dst or not self.pegs[src]:
            return False
        return not self.pegs[dst] or self.top(src) < self.top(dst)
    # Move the top disc from src to dst, returns False if the move is illegal
    def move(self, src, dst):
        if not self.can_move(src, dst):
            return False
        self.pegs[dst].append(self.pegs[src].pop())
        self.moves += 1
        return True
    def is_solved(self):
        return len(self.pegs[2]) == self.n_discs
