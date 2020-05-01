# Main AI file
# Controls all functions of chess play from high-level perspective

import time

class Skywalker:
    # All configs are given as follows:
    # color: "white" / "black"
    # time_limit: number of seconds since starting
    # depth: maximum branch depth

    # Accepts Board object and config dictionary
    def get_board_value(self, board, config):
        board = board.board
        values = {'p': 1, 'n': 3, 'b': 3, 'q': 9, 'k': 100, 'r': 5}
        ends = [ord('a'), ord('z'), ord('A'), ord('Z')]
        black_value = sum(sum(values[piece] for piece in row if piece and ends[0] <= ord(piece) <= ends[1]) for row in board)
        white_value = sum(sum(values[piece.lower()] for piece in row if piece and ends[2] <= ord(piece) <= ends[3]) for row in board)
        return white_value - black_value if config['color'] == 'white' else black_value - white_value

    def generate_move(self, board, config):
        # TODO: Consider previous board state for castling and en passant

        # Set timer and max depth according to config

        # Get some candidate moves

        # Branch a little off those

        # Prune candidates by average branch success

        # Go deeper on the most promising branches

        # Give move that results in best outcome

        return "e2e4"

