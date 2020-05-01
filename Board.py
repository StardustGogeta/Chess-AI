class Board:
    def __init__(self, board = None):
        if board:
            self.board = board
        else:
            self.reset()

    def reset(self):
        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]

        return self

    def clear(self):
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        return self

    def load(self, board):
        self.board = board
        return self
    
    def move(self, start, end):
        piece = self.board[start[0]][start[1]]
        self.board[start[0]][start[1]] = 0
        self.board[end[0]][end[1]] = piece
        return self

    def __repr__(self):
        return '\n'.join('\t'.join((f'[{piece}]' if piece else '*') for piece in row) for row in self.board)
