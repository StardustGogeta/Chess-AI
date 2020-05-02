from Board import Board
from Skywalker import Skywalker
from Misc import human_move_to_tuple

class Game:
    def __init__(self):
        self.board = Board()
        self.ai = Skywalker()
        self.ai_cfg = {"color": "white"}

    def run_game(self):
        # TODO: Check for game finish (stalemate, 50 turn rule, checkmate)
        while True:
            print("\n" + "-" * 60 + "\n" + str(self.board) + "\n" + "-" * 60 + "\n")
            print("AI recommends... " + self.ai.generate_naive_move(self.board, self.ai_cfg))
            move = input("Enter a move: ")
            self.make_move(move)
            
    
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
        if len(move) > 4:
            return self.__force_move_tuple__(((row0, col0), (row1, col1, move[4])))
        return self.__force_move_tuple__(((row0, col0), (row1, col1)))

    # Accepts move without performing any validation
    def __force_move_tuple__(self, move):
        if len(move[1]) == 2:
            (row0, col0), (row1, col1) = move
            self.board.move((row0, col0), (row1, col1))
        else:
            (row0, col0), (row1, col1, promotion) = move
            self.board.move((row0, col0), (row1, col1, promotion))
        return self

    def __repr__(self):
        return repr(self.board)


if __name__ == "__main__":
    print("Testing!")
    g = Game()

    g.run_game()

    # print(g)
    # print("\n")
    # g.make_move("e2e4")
    # print(g)
    # print("\n")

    # S = Skywalker()
    # cfg = {"color": "white"}

    # while True:
    #     g.make_move(input("Enter a move: "))
    #     print(g)
    #     print(S.get_board_value(g.board, cfg))
    #     print("\n")

    # print(g.board.get_moves(human_move_to_tuple("b1"), 'white'))

    # print(S.generate_naive_move(g.board, cfg))

