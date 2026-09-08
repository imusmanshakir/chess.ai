from backend.app.chess.board import Board
from backend.app.chess.pieces import Color, Piece, PieceType
from backend.app.chess.rules import (
    get_king_square,
    get_legal_moves,
    is_checkmate,
    is_in_check,
    is_square_attacked,
    is_stalemate,
)


def test_get_king_square_finds_the_king_for_a_color():
    board = Board()

    assert get_king_square(board, Color.WHITE) == "e1"
    assert get_king_square(board, Color.BLACK) == "e8"


def test_rook_attacks_a_king_on_an_open_file():
    board = Board()
    board.squares = {
        "e1": Piece(Color.WHITE, PieceType.KING),
        "a8": Piece(Color.BLACK, PieceType.KING),
        "e8": Piece(Color.BLACK, PieceType.ROOK),
    }

    assert is_square_attacked(board, "e1", Color.BLACK)
    assert is_in_check(board, Color.WHITE)


def test_piece_between_rook_and_king_prevents_check():
    board = Board()
    board.squares = {
        "e1": Piece(Color.WHITE, PieceType.KING),
        "e4": Piece(Color.WHITE, PieceType.PAWN),
        "a8": Piece(Color.BLACK, PieceType.KING),
        "e8": Piece(Color.BLACK, PieceType.ROOK),
    }

    assert not is_square_attacked(board, "e1", Color.BLACK)
    assert not is_in_check(board, Color.WHITE)


def test_get_legal_moves_excludes_moves_that_leave_the_king_in_check():
    board = Board()
    board.squares = {
        "e1": Piece(Color.WHITE, PieceType.KING),
        "e2": Piece(Color.WHITE, PieceType.KNIGHT),
        "a8": Piece(Color.BLACK, PieceType.KING),
        "e8": Piece(Color.BLACK, PieceType.ROOK),
    }

    legal_moves = get_legal_moves(board, Color.WHITE)

    assert ("e2", "c3") not in legal_moves
    assert ("e2", "g3") not in legal_moves


def test_checkmate_when_checked_king_has_no_legal_moves():
    board = Board()
    board.squares = {
        "c6": Piece(Color.WHITE, PieceType.KING),
        "b7": Piece(Color.WHITE, PieceType.QUEEN),
        "a8": Piece(Color.BLACK, PieceType.KING),
    }

    assert is_in_check(board, Color.BLACK)
    assert get_legal_moves(board, Color.BLACK) == []
    assert is_checkmate(board, Color.BLACK)
    assert not is_stalemate(board, Color.BLACK)


def test_stalemate_when_king_is_not_checked_but_has_no_legal_moves():
    board = Board()
    board.squares = {
        "c6": Piece(Color.WHITE, PieceType.KING),
        "c7": Piece(Color.WHITE, PieceType.QUEEN),
        "a8": Piece(Color.BLACK, PieceType.KING),
    }

    assert not is_in_check(board, Color.BLACK)
    assert get_legal_moves(board, Color.BLACK) == []
    assert not is_checkmate(board, Color.BLACK)
    assert is_stalemate(board, Color.BLACK)
