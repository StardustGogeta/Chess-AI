# Gives color of piece (white if uppercase, black if lowercase)
piece_color_ends = [ord('a'), ord('z'), ord('A'), ord('Z')]

# Returns "white" or "black" based on upper-/lower-case
def piece_color(piece):
    if not piece:
        return None
    n = ord(piece)
    return "black" if piece_color_ends[0] <= n <= piece_color_ends[1] else "white"

# Converts a move in human form ("e7") to a tuple in (row, col) form
def human_move_to_tuple(move):
    col = ord(move[0]) - ord('a')
    row = 8 - int(move[1])
    return (row, col)

# Converts a tuple in (row, col) form to a move in human form ("e7")
def tuple_to_human_move(move):
    row, col = move
    return chr(col + ord('a')) + str(8 - row)

# Returns whether a position is located on the board
def valid_pos(pos):
    y, x = pos
    return 0 <= y < 8 and 0 <= x < 8

# Returns a list of all valid squares on the board
def all_squares():
    for y in range(8):
        for x in range(8):
            yield (y, x)
