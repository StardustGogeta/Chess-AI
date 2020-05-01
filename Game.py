from Board import Board
from Skywalker import Skywalker

class Game:
    def __init__(self):
        self.board = Board()
    
    # Accepts moves as "e4e5" (or "d7d8Q" in case of promotion)
    def make_move(self, move):
        # TODO: Fix for input validation, both syntax and game logic
        self.__force_move__(move)

    # Accept move without performing any validation
    def __force_move__(self, move):
        # Convert to zero-based indices
        col0 = ord(move[0]) - ord('a')
        row0 = 8 - int(move[1])
        col1 = ord(move[2]) - ord('a')
        row1 = 8 - int(move[3])

        # TODO: Add pawn promotion
        self.board.move((row0, col0), (row1, col1))
        return self

    def __repr__(self):
        return repr(self.board)


if __name__ == "__main__":
    print("Testing!")
    g = Game()
    print(g)
    print("\n")
    g.make_move("e2e4")
    print(g)
    print("\n")

    S = Skywalker()
    cfg = {"color": "white"}

    while True:
        g.make_move(input("Enter a move: "))
        print(g)
        print(S.get_board_value(g.board, cfg))
        print("\n")

