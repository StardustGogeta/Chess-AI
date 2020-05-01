from Board import Board

class Game:
    def __init__(self):
        self.board = Board()
    
    # Accepts moves as "e4e5" (or "d7d8Q" in case of promotion)
    def make_move(self, move):
        # Convert to zero-based indices
        col0 = ord(move[0]) - ord('a')
        row0 = 8 - int(move[1])
        col1 = ord(move[2]) - ord('a')
        row1 = 8 - int(move[3])

        self.board.move((row0, col0), (row1, col1))
        return self

    def __repr__(self):
        return repr(self.board)


if __name__ == "__main__":
    print("Testing!")
    g = Game()
    print(g)
    print("\n\n")
    g.make_move("e2e5")
    print(g)
