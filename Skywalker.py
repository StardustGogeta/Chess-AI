# Main AI file
# Controls all functions of chess play from high-level perspective

import time
from Misc import piece_color, tuple_to_human_move

class Skywalker:
    # All configs are given as follows:
    # color: "white" / "black"
    # time_limit: number of seconds since starting
    # depth: maximum branch depth

    # Accepts Board object and config dictionary
    def get_board_value(self, board, config):
        board = board.board
        values = {'p': 1, 'n': 3, 'b': 3, 'q': 9, 'k': 100, 'r': 5}
        black_value = sum(sum(values[piece] for piece in row if piece and piece_color(piece) == "black") for row in board)
        white_value = sum(sum(values[piece.lower()] for piece in row if piece and piece_color(piece) == "white") for row in board)
        return white_value - black_value if config['color'] == 'white' else black_value - white_value

    # Generate a naive move based on the highest immediate board value possible
    def generate_naive_move(self, board, config):
        color = config['color']
        best_move = ((0, 0), (0, 0), -1000)
        for y in range(8):
            for x in range(8):
                moves = board.get_moves((y, x), color)
                if moves:
                    for move in moves:
                        new_board = board.copy()
                        new_board.move((y, x), move)
                        value = self.get_board_value(new_board, config)
                        if value > best_move[2]:
                            best_move = ((y, x), move, value)
        return tuple_to_human_move(best_move[0]) + '-' + tuple_to_human_move(best_move[1])


    def generate_move(self, board, config):
        # TODO: Consider previous board state for castling and en passant

        # Set timer and max depth according to config

        # Get some candidate moves

        # Branch a little off those

        # Prune candidates by average branch success

        # Go deeper on the most promising branches

        # Give move that results in best outcome

        return "e2e4"

