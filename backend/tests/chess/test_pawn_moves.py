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
    
from backend.app.chess.board import Board
from backend.app.chess.moves import get_pawn_moves
from backend.app.chess.pieces import Color, Piece, PieceType


def test_white_pawn_can_capture_left():
    board = Board()

    board.set_piece("d3", Piece(Color.BLACK, PieceType.KNIGHT))

    moves = get_pawn_moves(board, "e2")

    assert "d3" in moves


def test_white_pawn_can_capture_right():
    board = Board()

    board.set_piece("f3", Piece(Color.BLACK, PieceType.BISHOP))

    moves = get_pawn_moves(board, "e2")

    assert "f3" in moves


def test_black_pawn_can_capture_left():
    board = Board()

    board.set_piece("d6", Piece(Color.WHITE, PieceType.KNIGHT))

    moves = get_pawn_moves(board, "e7")

    assert "d6" in moves


def test_black_pawn_can_capture_right():
    board = Board()

    board.set_piece("f6", Piece(Color.WHITE, PieceType.BISHOP))

    moves = get_pawn_moves(board, "e7")

    assert "f6" in moves


def test_pawn_cannot_capture_own_piece():
    board = Board()

    board.set_piece("d3", Piece(Color.WHITE, PieceType.KNIGHT))

    moves = get_pawn_moves(board, "e2")

    assert "d3" not in moves


def test_pawn_cannot_capture_empty_square():
    board = Board()

    moves = get_pawn_moves(board, "e2")

    assert "d3" not in moves
    assert "f3" not in moves    