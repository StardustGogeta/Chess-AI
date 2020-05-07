import time
from Board import Board
from Skywalker import Skywalker
from Misc import human_move_to_tuple

DEBUGGING = True
START_AS_WHITE = False

class Game:
    def __init__(self):
        self.board = Board()
        self.ai = Skywalker()
        self.ai_cfg = {"color": "white" if START_AS_WHITE else "black"}
        self.history = []
        self.no_compute = not START_AS_WHITE
        self.force_calc = False

    def run_game(self):
        # TODO: Check for game finish (stalemate, 50 turn rule, checkmate)
        turn_number = 0
        move_history = []
        while True:
            self.history.append(self.board.copy())
            while True:
                try:
                    print("\n" + "-" * 60 + "\n" + str(self.board) + "\n" + "-" * 60 + "\n")

                    if self.force_calc or not self.no_compute:
                        start = time.perf_counter()
                        print("AI recommends... " + self.ai.generate_move_by_level(self.board, self.ai_cfg, 3, turn_number, move_history))
                        print(f"Time elapsed: {time.perf_counter()-start}")

                    move = input("Enter a move: ")
                    if move in ("REWIND", "UNDO"):
                        # Undo the previous move
                        if len(self.history) > 1:
                            self.board = self.history[-2]
                            self.history.pop()
                            move_history.pop()
                            print("Reset board to previous state.")
                            turn_number -= 10.5
                            self.no_compute = not self.no_compute
                            self.force_calc = False
                        else:
                            print("No board history available.")
                    elif move in ("RECALC", "REROLL"):
                        # Recalculate the AI move suggestion
                        continue
                    elif move in ("FORCECALC"):
                        # Force the AI to calculate a move when it is not on the proper turn
                        self.force_calc = True
                    else:
                        self.make_move(move)
                        move_history.append(move)
                        turn_number += 1
                        self.no_compute = not self.no_compute
                        self.force_calc = False
                        break
                except KeyboardInterrupt:
                    raise KeyboardInterrupt("Program ended by user.")
                except (ValueError, IndexError):
                    print("Invalid input.")
                except Exception as err:
                    if DEBUGGING:
                        raise err 
                    print("Invalid input.")
            
    
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
    g = Game()

    # g.board.load([
    #     [0, 0, 0, 0, 0, 0, 'r', 0],
    #     ['r', 0, 0, 0, 'k', 'n', 0, 0],
    #     [0, 0, 'p', 0, 0, 'p', 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 'p'],
    #     [0, 'R', 0, 'p', 0, 0, 0, 0],
    #     [0, 0, 0, 'N', 'q', 'p', 0, 0],
    #     [0, 0, 'K', 'R', 0, 'N', 0, 0],
    #     [0, 0, 0, 'Q', 0, 0, 0, 0]
    # ])

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

