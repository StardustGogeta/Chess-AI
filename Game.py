from Board import Board
from Skywalker import Skywalker
from Misc import human_move_to_tuple

class Game:
    def __init__(self):
        self.board = Board()
    
    # Accepts moves as "e4e5" (or "d7d8Q" in case of promotion)
    def make_move(self, move):
        # TODO: Fix for input validation, both syntax and game logic
        return self.__force_move__(move)

    # Accepts moves as ((row, col), (row2, col2)) (or ((row, col), (row2, col2), "Q") in case of promotion)
    def make_move_tuple(self, move):
        # TODO: Fix for input validation, both syntax and game logic
        return self.__force_move_tuple__(move)

    # Accepts move without performing any validation
    def __force_move__(self, move):
        # Convert to zero-based indices
        row0, col0 = human_move_to_tuple(move[0:2])
        row1, col1 = human_move_to_tuple(move[2:4])
        return self.__force_move_tuple__(((row0, col0), (row1, col1)))

    # Accepts move without performing any validation
    def __force_move_tuple__(self, move):
        if len(move) == 2:
            (row0, col0), (row1, col1) = move
        else:
            raise Exception("Promotion not implemented!")

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

    # while True:
    #     g.make_move(input("Enter a move: "))
    #     print(g)
    #     print(S.get_board_value(g.board, cfg))
    #     print("\n")

    print(g.board.get_moves(human_move_to_tuple("b1")))

    print(S.generate_naive_move(g.board, cfg))

