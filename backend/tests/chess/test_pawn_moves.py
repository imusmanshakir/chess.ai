from backend.app.chess.board import Board
from backend.app.chess.moves import get_pawn_moves


def test_white_pawn_can_move_one_or_two_squares():
    board = Board()

    moves = get_pawn_moves(board, "e2")

    assert "e3" in moves
    assert "e4" in moves


def test_black_pawn_can_move_one_or_two_squares():
    board = Board()

    moves = get_pawn_moves(board, "e7")

    assert "e6" in moves
    assert "e5" in moves


def test_white_pawn_cannot_move_three_squares():
    board = Board()

    moves = get_pawn_moves(board, "e2")

    assert "e5" not in moves


def test_black_pawn_cannot_move_three_squares():
    board = Board()

    moves = get_pawn_moves(board, "e7")

    assert "e4" not in moves


def test_non_pawn_has_no_pawn_moves():
    board = Board()

    moves = get_pawn_moves(board, "e1")

    assert moves == []