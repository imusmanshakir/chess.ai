from backend.app.chess.board import Board
from backend.app.chess.moves import get_knight_moves
from backend.app.chess.pieces import Color, Piece, PieceType


def test_knight_has_eight_l_shaped_moves_on_an_open_board():
    board = Board()
    board.squares = {"d4": Piece(Color.WHITE, PieceType.KNIGHT)}

    moves = get_knight_moves(board, "d4")

    assert set(moves) == {"b3", "b5", "c2", "c6", "e2", "e6", "f3", "f5"}


def test_knight_cannot_move_beyond_the_board_edge():
    board = Board()
    board.squares = {"a1": Piece(Color.WHITE, PieceType.KNIGHT)}

    moves = get_knight_moves(board, "a1")

    assert set(moves) == {"b3", "c2"}


def test_knight_can_capture_enemy_but_not_friendly_piece():
    board = Board()
    board.squares = {
        "d4": Piece(Color.WHITE, PieceType.KNIGHT),
        "b3": Piece(Color.BLACK, PieceType.PAWN),
        "f5": Piece(Color.WHITE, PieceType.PAWN),
    }

    moves = get_knight_moves(board, "d4")

    assert "b3" in moves
    assert "f5" not in moves


def test_knight_can_jump_over_pieces():
    board = Board()
    board.squares = {
        "d4": Piece(Color.WHITE, PieceType.KNIGHT),
        "d5": Piece(Color.WHITE, PieceType.PAWN),
        "e4": Piece(Color.BLACK, PieceType.PAWN),
    }

    moves = get_knight_moves(board, "d4")

    assert "f5" in moves


def test_non_knight_has_no_knight_moves():
    board = Board()

    assert get_knight_moves(board, "e2") == []
