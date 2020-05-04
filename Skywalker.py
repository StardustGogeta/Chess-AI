# Main AI file
# Controls all functions of chess play from high-level perspective

import time, random
from Misc import piece_color, tuple_to_human_move, all_squares

class Skywalker:
    # All configs are given as follows:
    # color: "white" / "black"
    # time_limit: number of seconds since starting
    # depth: maximum branch depth

    
    def get_piece_value(self, board, config):
        """
        Returns value of pieces remaining on board (difference of your pieces and opponent's pieces)

        Accepts Board object and config dictionary

        Uses standard piece values (and 100 for king)
        """
        # print("Getting piece value!")
        board = board.board
        values = {'p': 1, 'n': 3, 'b': 3, 'q': 9, 'k': 100, 'r': 5}
        black_value = sum(sum(values[piece] for piece in row if piece and piece_color(piece) == "black") for row in board)
        white_value = sum(sum(values[piece.lower()] for piece in row if piece and piece_color(piece) == "white") for row in board)
        return white_value - black_value if config['color'] == 'white' else black_value - white_value

    def get_board_value(self, board, config):
        # TODO: Consider more factors in board value (e.g. position)
        return self.get_piece_value(board, config)

    def generate_naive_move(self, board, config):
        return self.generate_predictive_piece_value_move(board, config, depth=0)
        # """
        # Level 0: Generate a naive move based on the highest immediate piece value possible

        # "Immediate Gratification" / "Greedy" Approach

        # Key Properties:
        # - Looks one half-turn ahead
        # - Finds all possible moves
        # - Randomly sorts moves (optionally trimming off a fraction at random)
        # - Gets move that results in best piece value
        # - Sends chosen move and the resultant piece value
        # """
        # color = config['color']
        # best_move = ((0, 0), (0, 0), -1000)
        # squares = list(all_squares())
        # # Randomize selected squares / pieces
        # for (y, x) in random.sample(squares, int(len(squares) * 4/4)):
        #     moves = board.get_moves((y, x), color)
        #     if moves:
        #         # Randomize order of moves evaluated
        #         random.shuffle(moves)
        #         for move in moves:
        #             new_board = board.copy()
        #             new_board.move((y, x), move)
        #             value = self.get_piece_value(new_board, config)
        #             if value > best_move[1]:
        #                 best_move = ((y, x), move), value)
        # if best_move[2] == -1000:
        #     return "AI FAILED - Checkmate inevitable?"
        # return best_move

    def generate_predictive_piece_value_after_move(self, board, config, move, depth = 1):
        """
        Generates the predicted piece value for the board after a move is played

        Searches `depth` half-moves after the proposed one
        """
        color = config['color']
        opp_color = 'white' if color == 'black' else 'black'
        opp_config = config
        opp_config['color'] = opp_color

        new_board = board.copy().move(*move)

        # Immediate piece value
        if depth == 0:
            return self.get_piece_value(new_board, config)
        elif depth == 1:
            # Predicted best piece value in one half-turn (naive opponent)
            opp_naive_move = self.generate_naive_move(new_board, opp_config)
            return -1 * opp_naive_move[1] # Flip sign of piece value
        elif depth == 2:
            # Predicted best piece value in one full-turn (naive opponent, naive response)
            opponent_naive_move = self.generate_naive_move(new_board, opp_config)
            naive_resp = self.generate_naive_move(new_board.copy().move(*opponent_naive_move[0]), config)
            return naive_resp[1]

    def generate_predictive_piece_value_move(self, board, config, depth = 1):
        """
        Level ?: Generates a move based on the predicted highest piece value possible after `depth` half-moves
        Case of 1 half-move: We want to go with naive
        Case of 2 half-moves: We want to see what the opponent's response to our move would be (naive)
        Case of 3 half moves: We want to see what the opponent's response to our move would be (naive), and our response to that (naive)

        Key Properties:
        - Finds all possible moves
        - Randomly sorts moves (optionally trimming off a fraction at random)
        - Gets move that results in best predicted piece value after `depth` half-turns
        - Sends chosen move

        (When depth=0, devolves to naive case)
        """
        color = config['color']
        best_move = (((0, 0), (0, 0)), -1000)
        squares = list(all_squares())
        # Randomize selected squares / pieces
        for (y, x) in random.sample(squares, int(len(squares))):
            dests = board.get_moves((y, x), color)
            if dests:
                # Randomize order of moves evaluated
                random.shuffle(dests)
                for dest in dests:
                    move = ((y, x), dest)
                    value = self.generate_predictive_piece_value_after_move(board, config, move, depth)
                    if value > best_move[1]:
                        best_move = (move, value)
        if best_move[1] == -1000:
            return "AI FAILED - Checkmate inevitable?"
        return best_move

    def generate_move_by_level(self, board, config, level):
        if level == 0:
            tuple_move = self.generate_naive_move(board, config)[0]
        else:
            tuple_move = self.generate_predictive_piece_value_move(board, config, depth=level)[0]
        return tuple_to_human_move(tuple_move[0]) + '' + tuple_to_human_move(tuple_move[1])


    def generate_move(self, board, config):
        # TODO: Consider previous board state for castling and en passant

        # Set timer and max depth according to config

        # Get some candidate moves

        # Branch a little off those

        # Prune candidates by average branch success

        # Go deeper on the most promising branches

        # Give move that results in best outcome

        return "e2e4"

