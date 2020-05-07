import random
from Misc import human_move_to_tuple
from Board import Board

# Provides a dictionary that maps board position strings to sets of appropriate moves to follow with
class OpeningBook:
    def __init__(self):
        self.book = dict()

        sicilian = ['e2e4', 'c7c5', 'g1f3', 'd7d6', 'd2d4']
        center = ['e2e4', 'e7e5', 'd2d4', 'e5d4']
        king_pawn = ['e2e4', 'e7e5']
        kpkn = king_pawn + ['g1f3', 'b8c6']
        ruy_lopez = kpkn + ['f1b5', 'a7a6', 'b5a4']

        king_pawn2 = king_pawn + ['d2d3', 'g8f6', 'g1f3', 'b8c6']
        king_pawn2a = king_pawn2 + ['f1e2']
        king_pawn2b = king_pawn2 + ['c2c3']
        king_pawn2c = king_pawn2 + ['g2g3']

        french_defense =      ['e2e4', 'e7e6', 'd2d4', 'd7d5']
        french_defense_alt1 = ['e2e4', 'd7d5', 'd2d4', 'e7e6']
        french_defense_alt2 = ['d2d4', 'e7e6', 'e2e4', 'd7d5']
        french_defense_alt3 = ['d2d4', 'd7d5', 'e2e4', 'e7e6']
        french_classical = french_defense + ['b1c3', 'g8f6']

        reti_base = ['g1f3']
        reti = reti_base + ['d7d5']
        reti1 = reti + ['c2c4', 'd5d4']
        reti2 = reti + ['d2d4', 'c7c6']
        reti_alt = reti_base + ['g8f6', 'd2d4']

        # Some lines are strictly subsets of others, so we need not include them
        lines = [
            sicilian,
            center,
            ruy_lopez,
            king_pawn2a,
            king_pawn2b,
            king_pawn2c,
            french_defense_alt1,
            french_defense_alt2,
            french_defense_alt3,
            french_classical,
            reti1,
            reti2,
            reti_alt
        ]

        for line in lines:
            self.add(line)
        # print(f"openings:")
        # for opening in self.book:
        #     for y in range(8):
        #         print(opening[y*8:y*8+8])
        #     print(self.book[opening], "\n")

    def add(self, line):
        board = Board()
        for (i, move) in enumerate(line[:-1]):
            pos = human_move_to_tuple(move[0:2])
            dest = human_move_to_tuple(move[2:4])
            board.move(pos, dest)
            key = board.hash()
            if key not in self.book:
                self.book[key] = set()
            self.book[key].add(line[i + 1])
            
    def get_move(self, move_history):
        board = Board()
        for move in move_history:
            pos = human_move_to_tuple(move[0:2])
            dest = human_move_to_tuple(move[2:4])
            board.move(pos, dest)
        key = board.hash()
        if key in self.book:
            return random.choice(list(self.book[key]))
        return None
