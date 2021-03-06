import copy, random
from Misc import piece_color, valid_pos, all_squares

class Board:
    def __init__(self, board = None):
        if board:
            self.board = board
        else:
            self.reset()

    # Resets board to initial piece layout
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

    # Removes all pieces from board
    def clear(self):
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        return self

    # Loads board from 2D array (note that row 1 in chess is row 7 in the array, row 2 is row 6, etc.)
    def load(self, board):
        self.board = board
        return self
    
    # Performs a move of a piece from start to end positions
    def move(self, start, end):
        move_cache = (start, end, self.board[start[0]][start[1]], self.board[end[0]][end[1]])
        piece = self.board[start[0]][start[1]]
        self.board[start[0]][start[1]] = 0
        self.board[end[0]][end[1]] = piece if len(end) == 2 else end[2] # Promotion
        return self, move_cache

    # Undoes a move using a cache of the old start and end positions and pieces
    # TODO: Add en passant and castle support
    def unmove(self, move_cache):
        start, end, start_piece, end_piece = move_cache
        self.board[start[0]][start[1]] = start_piece
        self.board[end[0]][end[1]] = end_piece
        return self

    # Creates a deep copy of the current board
    def copy(self):
        return copy.deepcopy(self)

    def hash(self):
        return ''.join(str(e) for row in self.board for e in row)

    # Adds all valid rook moves for the given color to the moves list
    def __get_rook_moves__(self, pos, color, moves):
        y, x = pos

        # Increase y
        y2 = y + 1
        while y2 < 8:
            piece2 = self.board[y2][x]
            # Piece collision
            if piece2:
                color2 = piece_color(piece2)
                # Capture
                if color != color2:
                    moves.append((y2, x))
                break
            else:
                moves.append((y2, x))
            y2 += 1
        
        # Decrease y
        y2 = y - 1
        while y2 >= 0:
            piece2 = self.board[y2][x]
            # Piece collision
            if piece2:
                color2 = piece_color(piece2)
                # Capture
                if color != color2:
                    moves.append((y2, x))
                break
            else:
                moves.append((y2, x))
            y2 -= 1

        # Increase x
        x2 = x + 1
        while x2 < 8:
            piece2 = self.board[y][x2]
            # Piece collision
            if piece2:
                color2 = piece_color(piece2)
                # Capture
                if color != color2:
                    moves.append((y, x2))
                break
            else:
                moves.append((y, x2))
            x2 += 1
        
        # Decrease x
        x2 = x - 1
        while x2 >= 0:
            piece2 = self.board[y][x2]
            # Piece collision
            if piece2:
                color2 = piece_color(piece2)
                # Capture
                if color != color2:
                    moves.append((y, x2))
                break
            else:
                moves.append((y, x2))
            x2 -= 1

    # Adds all valid bishop moves for the given color to the moves list
    def __get_bishop_moves__(self, pos, color, moves):
        y, x = pos

        # Increase y and x
        y2, x2 = y + 1, x + 1
        while y2 < 8 and x2 < 8:
            piece2 = self.board[y2][x2]
            # Piece collision
            if piece2:
                color2 = piece_color(piece2)
                # Capture
                if color != color2:
                    moves.append((y2, x2))
                break
            else:
                moves.append((y2, x2))
            y2 += 1
            x2 += 1
        
        # Decrease y and x
        y2, x2 = y - 1, x - 1
        while y2 >= 0 and x2 >= 0:
            piece2 = self.board[y2][x2]
            # Piece collision
            if piece2:
                color2 = piece_color(piece2)
                # Capture
                if color != color2:
                    moves.append((y2, x2))
                break
            else:
                moves.append((y2, x2))
            y2 -= 1
            x2 -= 1

        # Increase y, decrease x
        y2, x2 = y + 1, x - 1
        while y2 < 8 and x2 >= 0:
            piece2 = self.board[y2][x2]
            # Piece collision
            if piece2:
                color2 = piece_color(piece2)
                # Capture
                if color != color2:
                    moves.append((y2, x2))
                break
            else:
                moves.append((y2, x2))
            y2 += 1
            x2 -= 1
        
        # Decrease y, increase x
        y2, x2 = y - 1, x + 1
        while y2 >= 0 and x2 < 8:
            piece2 = self.board[y2][x2]
            # Piece collision
            if piece2:
                color2 = piece_color(piece2)
                # Capture
                if color != color2:
                    moves.append((y2, x2))
                break
            else:
                moves.append((y2, x2))
            y2 -= 1
            x2 += 1

    # Adds all valid knight moves for the given color to the moves list
    def __get_knight_moves__(self, pos, color, moves):
        def check_pos(new_pos):
            if valid_pos(new_pos):
                y2, x2 = new_pos
                piece2 = self.board[y2][x2]
                if not piece2 or color != piece_color(piece2):
                    moves.append((y2, x2))

        y, x = pos

        # Using cardinal directions:
        check_pos((y + 2, x + 1)) # NNE
        check_pos((y + 1, x + 2)) # ENE
        check_pos((y - 1, x + 2)) # ESE
        check_pos((y - 2, x + 1)) # SSE
        check_pos((y - 2, x - 1)) # SSW
        check_pos((y - 1, x - 2)) # WSW
        check_pos((y + 1, x - 2)) # WNW
        check_pos((y + 2, x - 1)) # NNW

    # Adds all valid king moves for the given color to the moves list
    def __get_king_moves__(self, pos, color, moves):
        # TODO: Consider castling

        # Checks a position on the board and adds it to the moves list if valid
        def check_pos(new_pos):
            if valid_pos(new_pos):
                y2, x2 = new_pos
                piece2 = self.board[y2][x2]
                if not piece2 or color != piece_color(piece2):
                    moves.append((y2, x2))

        y, x = pos

        # Using cardinal directions:
        check_pos((y + 1, x)) # N
        check_pos((y + 1, x + 1)) # NE
        check_pos((y, x + 1)) # E
        check_pos((y - 1, x + 1)) # SE
        check_pos((y - 1, x)) # S
        check_pos((y - 1, x - 1)) # SW
        check_pos((y, x - 1)) # W
        check_pos((y + 1, x - 1)) # NW

    # Adds all valid pawn moves for the given color to the moves list
    def __get_pawn_moves__(self, pos, color, moves):
        # TODO: Consider en passant
        # TODO: Consider pawns starting with 2 moves, make sure they don't jump pieces!
        def check_pos(new_pos, diag):
            if valid_pos(new_pos):
                y2, x2 = new_pos
                piece2 = self.board[y2][x2]
                if (not diag and not piece2) or (diag and piece2 and color != piece_color(piece2)):
                    if y2 in [0, 7]:
                        # Promote to queen by default
                        moves.append((y2, x2, "Q" if color == 'white' else "q"))
                    else:
                        moves.append((y2, x2))

        y, x = pos

        if color == 'black':
            check_pos((y + 1, x), False)
            check_pos((y + 1, x + 1), True)
            check_pos((y + 1, x - 1), True)
            if y == 1:
                check_pos((y + 2, x), False)

        if color == 'white':
            check_pos((y - 1, x), False)
            check_pos((y - 1, x + 1), True)
            check_pos((y - 1, x - 1), True)
            if y == 6:
                check_pos((y - 2, x), False)

    # Returns whether the king of a certain color is in check or is dead
    def check_for_attacks(self, color):
        # Find king
        found = False
        target = 'K' if color == 'white' else 'k'
        for (y, x) in all_squares():
            if self.board[y][x] == target:
                king = (y, x)
                found = True
                break
        if not found:
            # print(f"Looking for {target}, {color}, but not found!")
            return False # To allow a dead side to make hypothetical postmortem moves
        # Check for attacking pieces
        for (y2, x2) in all_squares():
            piece2 = self.board[y2][x2]
            color2 = piece_color(piece2)
            if color != color2 and king in self.get_moves((y2, x2), color2, check_for_check=False):
                return True
        return False

    # Tells whether a move will put the king into check
    def puts_into_check(self, start, end, color):
        move_cache = self.move(start, end)[1]
        ret = self.check_for_attacks(color)
        self.unmove(move_cache)
        return ret

    # Returns a list of all valid destinations (y, x) for a piece at a given position
    def get_moves(self, pos, color, *, check_for_check = True):
        y, x = pos
        piece = self.board[y][x]
        if not piece:
            return []
        if piece:
            p_color = piece_color(piece)

            moves = []

            # Check that we are not moving the opponent's pieces
            if p_color == color:
                lower = piece.lower()
                # Rook or Queen
                if lower == 'r' or lower == 'q':
                    self.__get_rook_moves__(pos, color, moves)

                # Knight
                if lower == 'n':
                    self.__get_knight_moves__(pos, color, moves)
                
                # Bishop or Queen
                if lower == 'b' or lower == 'q':
                    self.__get_bishop_moves__(pos, color, moves)

                # King
                if lower == 'k':
                    self.__get_king_moves__(pos, color, moves)

                # Pawn
                if lower == 'p':
                    self.__get_pawn_moves__(pos, color, moves)

                # if pos == (2, 7): print("PRECHECK", moves)
                if check_for_check:
                    moves = list(filter(lambda move: not self.puts_into_check(pos, move, color), moves))
                # if pos == (2, 7): print("\tPOSTCHECK", moves)
            return moves

    # Get all available moves for a given player on the board
    def get_all_moves(self, color, *, check_for_check = True):
        for pos in all_squares():
            piece_moves = self.get_moves(pos, color, check_for_check=check_for_check)
            random.shuffle(piece_moves)
            for move in piece_moves:
                yield (pos, move)

    # Get all available moves for a given player on the board, arranged with a smart ordering to them
    def get_all_moves_smart(self, color, *, check_for_check = True):
        values = {'p': 1, 'n': 3, 'b': 3, 'q': 9, 'k': 8, 'r': 5}

        high_captures = []
        equal_captures = []
        low_captures = []
        no_captures = []

        for pos in all_squares():
            piece = self.board[pos[0]][pos[1]]
            if piece:
                piece_moves = self.get_moves(pos, color, check_for_check=check_for_check)
                if piece_moves:
                    value = values[piece.lower()]
                    # random.shuffle(piece_moves)
                    for dest in piece_moves:
                        target = self.board[dest[0]][dest[1]]
                        move = (pos, dest)
                        if target: # Captures
                            target_value = values[target.lower()]
                            diff = target_value - value
                            if diff > 0:
                                high_captures.append(move)
                            elif diff < 0:
                                low_captures.append(move)
                            else:
                                equal_captures.append(move)
                        else:
                            no_captures.append(move)
        return high_captures + equal_captures + low_captures + no_captures


    def __repr__(self):
        return '\n'.join('\t'.join((f'[{piece}]' if piece else '*') for piece in row) for row in self.board)
