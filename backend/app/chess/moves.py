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

    # Forward one square
    one_step = f"{file}{rank + direction}"

    if board.is_valid_square(one_step) and board.get_piece(one_step) is None:
        moves.append(one_step)

        # Forward two squares from starting position
        two_step = f"{file}{rank + (2 * direction)}"

        if rank == starting_rank and board.get_piece(two_step) is None:
            moves.append(two_step)

    # Diagonal captures
    file_index = "abcdefgh".index(file)

    for offset in (-1, 1):
        capture_file_index = file_index + offset

        if not 0 <= capture_file_index < 8:
            continue

        capture_file = "abcdefgh"[capture_file_index]
        capture_square = f"{capture_file}{rank + direction}"

        if not board.is_valid_square(capture_square):
            continue

        target_piece = board.get_piece(capture_square)

        if target_piece is not None and target_piece.color != piece.color:
            moves.append(capture_square)

    return moves
