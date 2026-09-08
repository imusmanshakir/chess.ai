from backend.app.chess.board import Board
from backend.app.chess.moves import get_bishop_moves
from backend.app.chess.pieces import Color, Piece, PieceType


def test_bishop_can_move_diagonally_on_an_open_board():
    board = Board()
    board.squares = {"d4": Piece(Color.WHITE, PieceType.BISHOP)}

    moves = get_bishop_moves(board, "d4")

    assert set(moves) == {
        "a1",
        "a7",
        "b2",
        "b6",
        "c3",
        "c5",
        "e3",
        "e5",
        "f2",
        "f6",
        "g1",
        "g7",
        "h8",
    }


def test_bishop_cannot_move_beyond_the_board_edge():
    board = Board()
    board.squares = {"a1": Piece(Color.WHITE, PieceType.BISHOP)}

    assert set(get_bishop_moves(board, "a1")) == {
        "b2",
        "c3",
        "d4",
        "e5",
        "f6",
        "g7",
        "h8",
    }


def test_bishop_cannot_move_through_or_capture_own_piece():
    board = Board()
    board.squares = {
        "d4": Piece(Color.WHITE, PieceType.BISHOP),
        "f6": Piece(Color.WHITE, PieceType.PAWN),
    }

    moves = get_bishop_moves(board, "d4")

    assert "e5" in moves
    assert "f6" not in moves
    assert "g7" not in moves


def test_bishop_can_capture_enemy_piece_but_stops_after_it():
    board = Board()
    board.squares = {
        "d4": Piece(Color.WHITE, PieceType.BISHOP),
        "f2": Piece(Color.BLACK, PieceType.KNIGHT),
    }

    moves = get_bishop_moves(board, "d4")

    assert "e3" in moves
    assert "f2" in moves
    assert "g1" not in moves


def test_non_bishop_has_no_bishop_moves():
    board = Board()

    assert get_bishop_moves(board, "e2") == []
