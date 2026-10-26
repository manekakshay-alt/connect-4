def _landing_row(board, column_index):
    for row_index, cell in enumerate(board[column_index]):
        if cell == "N":
            return row_index
    return None

def _line_length(board, column, row, dc, dr):
    total = 1

    for direction in (-1, 1):
        c = column + dc * direction
        r = row + dr * direction

        while (
            0 <= c < len(board)
            and 0 <= r < len(board[c])
            and board[c][r] == "Y"
        ):
            total += 1
            c += dc * direction
            r += dr * direction

    return total


def _find_building_move(board, line_type, target_length):
    for column_index in range(len(board)):
        row_index = _landing_row(board, column_index)

        # Skip full columns.
        if row_index is None:
            continue

        # Test the move .
        board[column_index][row_index] = "Y"

        if line_type == "column":
            length = _line_length(
                board, column_index, row_index, 0, 1
            )
        else:
            length = _line_length(
                board, column_index, row_index, 1, 0
            )

        # ~Get back original board.
        board[column_index][row_index] = "N"

        if length >= target_length:
            return column_index

    return None


def TwoInAColumn(board):
    # Find a move that extends a vertical pair to three or more.
    return _find_building_move(board, "column", 3)


def TwoInARow(board):
    # Find a move that extends a horizontal pair to three or more.
    return _find_building_move(board, "row", 3)


def ThreeInAColumn(board):
    # Find an immediate vertical win.
    return _find_building_move(board, "column", 4)


def ThreeInARow(board):
    # Find an immediate horizontal win.
    return _find_building_move(board, "row", 4)


def EasyWin(board):
    # Priority 1: Win immediately.
    move = ThreeInAColumn(board)
    if move is not None:
        return move

    move = ThreeInARow(board)
    if move is not None:
        return move

    # Priority 2: Extend an existing pair to three.
    move = TwoInAColumn(board)
    if move is not None:
        return move

    move = TwoInARow(board)
    if move is not None:
        return move

    # No suitable move found.
    return None




