from backend.app.chess.board import Board
from backend.app.chess.pieces import Color, PieceType


def get_pawn_moves(board, square, en_passant_target=None):
    piece = board.get_piece(square)

    if piece is None or piece.type != PieceType.PAWN:
        return []

    file = square[0]
    rank = int(square[1])
    # square = "e2"----->e → file 2 → rank (Python uses indexing starting at zero:)
    # "e2"
    # index:
    #   0  1
    #   ↓  ↓
    #   e  2

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
        elif get_en_passant_capture_square(
            board,
            square,
            capture_square,
            en_passant_target,
        ) is not None:
            moves.append(capture_square)

    return moves


def get_en_passant_capture_square(
    board,
    from_square,
    to_square,
    en_passant_target,
):
    moving_piece = board.get_piece(from_square)

    if (
        en_passant_target != to_square
        or moving_piece is None
        or moving_piece.type != PieceType.PAWN
        or board.get_piece(to_square) is not None
    ):
        return None

    from_file_index = "abcdefgh".index(from_square[0])
    to_file_index = "abcdefgh".index(to_square[0])
    direction = 1 if moving_piece.color == Color.WHITE else -1

    if (
        abs(to_file_index - from_file_index) != 1
        or int(to_square[1]) != int(from_square[1]) + direction
    ):
        return None

    captured_square = f"{to_square[0]}{from_square[1]}"
    captured_piece = board.get_piece(captured_square)

    if (
        captured_piece is None
        or captured_piece.type != PieceType.PAWN
        or captured_piece.color == moving_piece.color
    ):
        return None

    return captured_square


def _get_sliding_moves(board, square, directions):
    piece = board.get_piece(square)
    file_index = "abcdefgh".index(square[0])
    rank = int(square[1])
    moves = []

    for file_step, rank_step in directions:
        current_file_index = file_index + file_step
        current_rank = rank + rank_step

        while 0 <= current_file_index < 8 and 1 <= current_rank <= 8:
            destination = f"{'abcdefgh'[current_file_index]}{current_rank}"
            target_piece = board.get_piece(destination)

            if target_piece is None:
                moves.append(destination)
            else:
                if target_piece.color != piece.color:
                    moves.append(destination)
                break

            current_file_index += file_step
            current_rank += rank_step

    return moves


def get_rook_moves(board, square):
    piece = board.get_piece(square)

    if piece is None or piece.type != PieceType.ROOK:
        return []

    # Rooks slide along ranks and files.
    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

    return _get_sliding_moves(board, square, directions)


def get_bishop_moves(board, square):
    piece = board.get_piece(square)

    if piece is None or piece.type != PieceType.BISHOP:
        return []

    # Bishops slide along diagonals.
    directions = ((1, 1), (1, -1), (-1, 1), (-1, -1))

    return _get_sliding_moves(board, square, directions)


def get_queen_moves(board, square):
    piece = board.get_piece(square)

    if piece is None or piece.type != PieceType.QUEEN:
        return []

    # Queens slide along ranks, files, and diagonals.
    directions = (
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1),
    )

    return _get_sliding_moves(board, square, directions)


def get_knight_moves(board, square):
    piece = board.get_piece(square)

    if piece is None or piece.type != PieceType.KNIGHT:
        return []

    file_index = "abcdefgh".index(square[0])
    rank = int(square[1])
    moves = []

    # Knights move in an L shape: two squares in one direction and one in the other.
    offsets = (
        (-2, -1),
        (-2, 1),
        (-1, -2),
        (-1, 2),
        (1, -2),
        (1, 2),
        (2, -1),
        (2, 1),
    )

    for file_offset, rank_offset in offsets:
        destination_file_index = file_index + file_offset
        destination_rank = rank + rank_offset

        if not (0 <= destination_file_index < 8 and 1 <= destination_rank <= 8):
            continue

        destination = f"{'abcdefgh'[destination_file_index]}{destination_rank}"
        target_piece = board.get_piece(destination)

        if target_piece is None or target_piece.color != piece.color:
            moves.append(destination)

    return moves


def get_king_moves(board, square):
    piece = board.get_piece(square)

    if piece is None or piece.type != PieceType.KING:
        return []

    file_index = "abcdefgh".index(square[0])
    rank = int(square[1])
    moves = []

    # A king can move one square in any direction.
    directions = (
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1),
    )

    for file_step, rank_step in directions:
        destination_file_index = file_index + file_step
        destination_rank = rank + rank_step

        if not (0 <= destination_file_index < 8 and 1 <= destination_rank <= 8):
            continue

        destination = f"{'abcdefgh'[destination_file_index]}{destination_rank}"
        target_piece = board.get_piece(destination)

        if target_piece is None or target_piece.color != piece.color:
            moves.append(destination)

    return moves


def get_piece_moves(board, square, en_passant_target=None):
    piece = board.get_piece(square)

    if piece is None:
        return []

    if piece.type == PieceType.PAWN:
        return get_pawn_moves(board, square, en_passant_target)

    move_generators = {
        PieceType.ROOK: get_rook_moves,
        PieceType.KNIGHT: get_knight_moves,
        PieceType.BISHOP: get_bishop_moves,
        PieceType.QUEEN: get_queen_moves,
        PieceType.KING: get_king_moves,
    }

    return move_generators[piece.type](board, square)


