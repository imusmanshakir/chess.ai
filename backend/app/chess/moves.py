from backend.app.chess.board import Board
from backend.app.chess.pieces import Color, PieceType


def get_pawn_moves(board, square):
    piece = board.get_piece(square)

    if piece is None or piece.type != PieceType.PAWN:
        return []

    file = square[0]
    rank = int(square[1])

    moves = []

    if piece.color == Color.WHITE:
        direction = 1
        starting_rank = 2
    else:
        direction = -1
        starting_rank = 7

    one_step = f"{file}{rank + direction}"  # Calculate the one-square move

    if (
        board.is_valid_square(one_step) and board.get_piece(one_step) is None
    ):  # This checks whether the destination is actually on the chess board.Second condition checks whether the destination square is empty.
        moves.append(one_step)

        two_step = f"{file}{rank + (2 * direction)}"  # Calculate the two-step move

        if (
            rank == starting_rank and board.get_piece(two_step) is None
        ):  # board.get_piece(two_step) --> checks whether the final destination is empty.
            moves.append(two_step)

    return moves
