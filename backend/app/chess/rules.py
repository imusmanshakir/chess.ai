from backend.app.chess.board import Board
from backend.app.chess.moves import get_en_passant_capture_square, get_piece_moves
from backend.app.chess.pieces import Color, PieceType


def get_king_square(board: Board, color: Color) -> str | None:
    for square, piece in board.squares.items():
        if piece.color == color and piece.type == PieceType.KING:
            return square

    return None


def is_square_attacked(board: Board, square: str, by_color: Color) -> bool:
    for source_square, piece in board.squares.items():
        if piece.color != by_color:
            continue

        if square in get_piece_moves(board, source_square):
            return True

    return False


def is_in_check(board: Board, color: Color) -> bool:
    king_square = get_king_square(board, color)

    if king_square is None:
        raise ValueError(f"The board has no {color.value} king.")

    opponent_color = Color.BLACK if color == Color.WHITE else Color.WHITE

    return is_square_attacked(board, king_square, opponent_color)


def would_move_leave_king_in_check(
    board: Board,
    from_square: str,
    to_square: str,
    color: Color,
    en_passant_capture_square: str | None = None,
    castling_rook_move: tuple[str, str] | None = None,
) -> bool:
    simulated_board = board.clone()
    moving_piece = simulated_board.remove_piece(from_square)

    simulated_board.remove_piece(to_square)
    if en_passant_capture_square is not None:
        simulated_board.remove_piece(en_passant_capture_square)
    simulated_board.set_piece(to_square, moving_piece)

    if castling_rook_move is not None:
        rook_from_square, rook_to_square = castling_rook_move
        rook = simulated_board.remove_piece(rook_from_square)
        simulated_board.set_piece(rook_to_square, rook)

    return is_in_check(simulated_board, color)


def get_castling_rook_move(
    color: Color,
    from_square: str,
    to_square: str,
) -> tuple[str, str] | None:
    rank = "1" if color == Color.WHITE else "8"

    if from_square != f"e{rank}":
        return None

    if to_square == f"g{rank}":
        return (f"h{rank}", f"f{rank}")

    if to_square == f"c{rank}":
        return (f"a{rank}", f"d{rank}")

    return None


def get_castling_moves(
    board: Board,
    color: Color,
    castling_rights: set[str],
) -> list[str]:
    rank = "1" if color == Color.WHITE else "8"
    king_square = f"e{rank}"
    king = board.get_piece(king_square)
    opponent_color = Color.BLACK if color == Color.WHITE else Color.WHITE

    if (
        king is None
        or king.color != color
        or king.type != PieceType.KING
        or is_in_check(board, color)
    ):
        return []

    options = {
        "king_side": {
            "rook_square": f"h{rank}",
            "empty_squares": (f"f{rank}", f"g{rank}"),
            "king_path": (f"f{rank}", f"g{rank}"),
            "destination": f"g{rank}",
        },
        "queen_side": {
            "rook_square": f"a{rank}",
            "empty_squares": (f"b{rank}", f"c{rank}", f"d{rank}"),
            "king_path": (f"d{rank}", f"c{rank}"),
            "destination": f"c{rank}",
        },
    }
    moves = []

    for side, option in options.items():
        if side not in castling_rights:
            continue

        rook = board.get_piece(option["rook_square"])

        if (
            rook is None
            or rook.color != color
            or rook.type != PieceType.ROOK
            or any(board.get_piece(square) is not None for square in option["empty_squares"])
            or any(
                is_square_attacked(board, square, opponent_color)
                for square in option["king_path"]
            )
        ):
            continue

        moves.append(option["destination"])

    return moves


def get_legal_moves(
    board: Board,
    color: Color,
    en_passant_target: str | None = None,
    castling_rights: set[str] | None = None,
) -> list[tuple[str, str]]:
    legal_moves = []

    for from_square, piece in board.squares.items():
        if piece.color != color:
            continue

        pseudo_legal_moves = get_piece_moves(
            board,
            from_square,
            en_passant_target,
        )

        if piece.type == PieceType.KING:
            pseudo_legal_moves += get_castling_moves(
                board,
                color,
                castling_rights or set(),
            )

        for to_square in pseudo_legal_moves:
            target_piece = board.get_piece(to_square)
            en_passant_capture_square = get_en_passant_capture_square(
                board,
                from_square,
                to_square,
                en_passant_target,
            )
            castling_rook_move = get_castling_rook_move(
                color,
                from_square,
                to_square,
            )

            # Kings are never captured; checkmate ends the game instead.
            if target_piece is not None and target_piece.type == PieceType.KING:
                continue

            if not would_move_leave_king_in_check(
                board,
                from_square,
                to_square,
                color,
                en_passant_capture_square,
                castling_rook_move,
            ):
                legal_moves.append((from_square, to_square))

    return legal_moves


def is_checkmate(
    board: Board,
    color: Color,
    en_passant_target: str | None = None,
    castling_rights: set[str] | None = None,
) -> bool:
    return is_in_check(board, color) and not get_legal_moves(
        board,
        color,
        en_passant_target,
        castling_rights,
    )


def is_stalemate(
    board: Board,
    color: Color,
    en_passant_target: str | None = None,
    castling_rights: set[str] | None = None,
) -> bool:
    return not is_in_check(board, color) and not get_legal_moves(
        board,
        color,
        en_passant_target,
        castling_rights,
    )
