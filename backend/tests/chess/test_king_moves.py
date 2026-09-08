from backend.app.chess.board import Board
from backend.app.chess.moves import get_king_moves
from backend.app.chess.pieces import Color, Piece, PieceType


def test_king_can_move_one_square_in_any_direction():
    board = Board()
    board.squares = {"d4": Piece(Color.WHITE, PieceType.KING)}

    moves = get_king_moves(board, "d4")

    assert set(moves) == {"c3", "c4", "c5", "d3", "d5", "e3", "e4", "e5"}


def test_king_cannot_move_beyond_the_board_edge():
    board = Board()
    board.squares = {"a1": Piece(Color.WHITE, PieceType.KING)}

    assert set(get_king_moves(board, "a1")) == {"a2", "b1", "b2"}


def test_king_can_capture_enemy_but_not_friendly_piece():
    board = Board()
    board.squares = {
        "d4": Piece(Color.WHITE, PieceType.KING),
        "c3": Piece(Color.BLACK, PieceType.PAWN),
        "e5": Piece(Color.WHITE, PieceType.PAWN),
    }

    moves = get_king_moves(board, "d4")

    assert "c3" in moves
    assert "e5" not in moves


def test_non_king_has_no_king_moves():
    board = Board()

    assert get_king_moves(board, "e2") == []
