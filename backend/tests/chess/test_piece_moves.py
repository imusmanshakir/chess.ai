from backend.app.chess.board import Board
from backend.app.chess.moves import get_piece_moves


def test_get_piece_moves_dispatches_to_the_correct_piece_generator():
    board = Board()

    assert set(get_piece_moves(board, "e2")) == {"e3", "e4"}
    assert set(get_piece_moves(board, "b1")) == {"a3", "c3"}


def test_empty_square_has_no_piece_moves():
    board = Board()

    assert get_piece_moves(board, "e4") == []
