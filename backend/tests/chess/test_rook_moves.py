from backend.app.chess.board import Board
from backend.app.chess.moves import get_rook_moves
from backend.app.chess.pieces import Color, Piece, PieceType


def test_rook_can_move_horizontally_and_vertically_on_an_open_board():
    board = Board()
    board.squares = {"d4": Piece(Color.WHITE, PieceType.ROOK)}

    moves = get_rook_moves(board, "d4")

    assert set(moves) == {
        "a4",
        "b4",
        "c4",
        "e4",
        "f4",
        "g4",
        "h4",
        "d1",
        "d2",
        "d3",
        "d5",
        "d6",
        "d7",
        "d8",
    }


def test_rook_cannot_move_through_or_capture_own_piece():
    board = Board()
    board.squares = {
        "d4": Piece(Color.WHITE, PieceType.ROOK),
        "d6": Piece(Color.WHITE, PieceType.PAWN),
    }

    moves = get_rook_moves(board, "d4")

    assert "d5" in moves
    assert "d6" not in moves
    assert "d7" not in moves


def test_rook_can_capture_enemy_piece_but_stops_after_it():
    board = Board()
    board.squares = {
        "d4": Piece(Color.WHITE, PieceType.ROOK),
        "f4": Piece(Color.BLACK, PieceType.KNIGHT),
    }

    moves = get_rook_moves(board, "d4")

    assert "e4" in moves
    assert "f4" in moves
    assert "g4" not in moves


def test_non_rook_has_no_rook_moves():
    board = Board()

    assert get_rook_moves(board, "e2") == []
