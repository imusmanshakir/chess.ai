from backend.app.chess.board import Board


def test_valid_squares():
    board = Board()

    assert board.is_valid_square("a1") is True
    assert board.is_valid_square("e4") is True
    assert board.is_valid_square("h8") is True


def test_invalid_squares():
    board = Board()

    assert board.is_valid_square("a9") is False
    assert board.is_valid_square("i4") is False
    assert board.is_valid_square("e") is False
    assert board.is_valid_square("abcd") is False