# Main AI file
# Controls all functions of chess play from high-level perspective

import time, random
from Misc import piece_color, tuple_pair_to_human_move, all_squares
from OpeningBook import OpeningBook

class Skywalker:
    # All configs are given as follows:
    # color: "white" / "black"
    # time_limit: number of seconds since starting
    # depth: maximum branch depth

    def __init__(self):
        self.opening_book = OpeningBook()
        print("Opening book loaded.")
    
    def get_piece_value(self, board, config = None, *, color = None):
        """
        Returns value of pieces remaining on board (difference of your pieces and opponent's pieces)

        Accepts Board object and config dictionary

        Uses standard piece values (and 8 for king)
        """
        # print("Getting piece value!")
        assert config or color
        board = board.board
        color = color if color else config['color']
        values = {'p': 1, 'n': 3, 'b': 3, 'q': 9, 'k': 8, 'r': 5}
        black_value = sum(sum(values[piece] for piece in row if piece and piece_color(piece) == "black") for row in board)
        white_value = sum(sum(values[piece.lower()] for piece in row if piece and piece_color(piece) == "white") for row in board)
        return white_value - black_value if color == 'white' else black_value - white_value

    def get_board_value(self, board, config):
        # TODO: Consider more factors in board value (e.g. position)
        return self.get_piece_value(board, config)

    def generate_naive_move(self, board, config):
        return self.generate_predictive_piece_value_move(board, config, depth=0)

    def generate_shortsighted_move(self, board, config):
        return self.generate_predictive_piece_value_move(board, config, depth=1)
        

    def generate_predictive_piece_value_after_move(self, board, config, move, depth = 1):
        """
        Generates the predicted piece value for the board after a move is played

        Searches `depth` half-moves after the proposed one
        """
        color = config['color']
        opp_color = 'white' if color == 'black' else 'black'
        opp_config = config.copy()
        opp_config['color'] = opp_color

        move_cache = board.move(*move)[1]

        tphm = tuple_pair_to_human_move # Shorthand
        # Immediate piece value
        if depth == 0:
            ret = (self.get_piece_value(board, config), "")
        elif depth == 1:
            # Predicted best piece value in one half-turn (naive opponent)
            opp_naive_move = self.generate_naive_move(board, opp_config)
            # debug_str = f"\t[Shortsightedness predicts that {tphm(opp_naive_move[0])} will follow...]\n"
            ret = (-1 * opp_naive_move[1], "") # Flip sign of piece value
        elif depth == 2:
            # Predicted best piece value in one full-turn (naive opponent, naive response)
            opponent_shortsighted_move = self.generate_shortsighted_move(board, opp_config)
            debug_str = f"Starting with move {tphm(move)},\n"
            debug_str += f"Predicts that enemy will shortsightedly move {tphm(opponent_shortsighted_move[0])}...\n"
            move_cache_2 = board.move(*opponent_shortsighted_move[0])[1]
            player_resp = self.generate_shortsighted_move(board, config)
            board.unmove(move_cache_2)
            debug_str += f"Predicts that player will shortsightedly respond {tphm(player_resp[0])}...\n"
            debug_str += f"Results in value of {player_resp[1]}...\n"
            ret = (player_resp[1], debug_str)

        board.unmove(move_cache)
        return ret

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
        if depth == 2: print(f"FINDING BEST MOVE FOR COLOR {color}")
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
                    value, debug_str = self.generate_predictive_piece_value_after_move(board, config, move, depth)
                    if value > best_move[1]:
                        best_move = (move, value)
                        if debug_str: print(debug_str)
        return best_move

    def alpha_beta_max(self, board, alpha, beta, depth_remaining, color, opp_color):
        if not depth_remaining:
            return self.get_piece_value(board, color=opp_color)
        for move in board.get_all_moves_smart(color):
            move_cache = board.move(*move)[1]
            score = self.alpha_beta_min(board, alpha, beta, depth_remaining - 1, color, opp_color)
            board.unmove(move_cache)
            if score >= beta:
                # print(f"beta cut {depth_remaining}", flush=True)
                return beta
            if score > alpha:
                alpha = score
        return alpha

    def alpha_beta_min(self, board, alpha, beta, depth_remaining, color, opp_color):
        if not depth_remaining:
            return self.get_piece_value(board, color=color)
        for move in board.get_all_moves_smart(opp_color):
            move_cache = board.move(*move)[1]
            score = self.alpha_beta_max(board, alpha, beta, depth_remaining - 1, color, opp_color)
            board.unmove(move_cache)
            if score <= alpha:
                # print(f"alpha cut {depth_remaining}", flush=True)
                return alpha
            if score < beta:
                beta = score
        return beta

    def generate_alphabeta_move(self, board, config, depth):
        color = config['color']
        opp_color = 'white' if color == 'black' else 'black'
        opp_config = config.copy()
        opp_config['color'] = opp_color

        best_move = (((0, 0), (0, 0)), -1000)
        for move in board.get_all_moves_smart(color):
            move_cache = board.move(*move)[1]
            score = self.alpha_beta_max(board, -10**6, 10**6, depth, color, opp_color)
            board.unmove(move_cache)
            if score > best_move[1]:
                best_move = (move, score)
            print(f"Testing {move}... score of {score}.")
        return best_move

    # Return a move in human format based on an opening book of good lines
    def generate_opening_book_move(self, move_history):
        return self.opening_book.get_move(move_history)

    def generate_move_by_level(self, board, config, level, turn_number, move_history):
        if turn_number <= 10: # Early opening
            book_move = self.generate_opening_book_move(move_history)
            if book_move:
                print("Book move match!")
                return book_move
        if level == 0:
            tuple_move = self.generate_naive_move(board, config)[0]
        else:
            # tuple_move = self.generate_predictive_piece_value_move(board, config, depth=level)[0]
            tuple_move = self.generate_alphabeta_move(board, config, depth=level)[0]
        return tuple_pair_to_human_move(tuple_move)

    def generate_move(self, board, config):
        # TODO: Consider previous board state for castling and en passant

        # Set timer and max depth according to config

        # Get some candidate moves

        # Branch a little off those

        # Prune candidates by average branch success

        # Go deeper on the most promising branches

        # Give move that results in best outcome

        return "e2e4"

