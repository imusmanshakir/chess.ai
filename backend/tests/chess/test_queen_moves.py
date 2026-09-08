from backend.app.chess.board import Board
from backend.app.chess.moves import get_queen_moves
from backend.app.chess.pieces import Color, Piece, PieceType


def test_queen_can_move_along_ranks_files_and_diagonals():
    board = Board()
    board.squares = {"d4": Piece(Color.WHITE, PieceType.QUEEN)}

    moves = get_queen_moves(board, "d4")

    assert set(moves) == {
        "a1", "a4", "a7", "b2", "b4", "b6", "c3", "c4", "c5",
        "d1", "d2", "d3", "d5", "d6", "d7", "d8", "e3", "e4",
        "e5", "f2", "f4", "f6", "g1", "g4", "g7", "h4", "h8",
    }


def test_queen_cannot_move_through_or_capture_own_piece():
    board = Board()
    board.squares = {
        "d4": Piece(Color.WHITE, PieceType.QUEEN),
        "d6": Piece(Color.WHITE, PieceType.PAWN),
    }

    moves = get_queen_moves(board, "d4")

    assert "d5" in moves
    assert "d6" not in moves
    assert "d7" not in moves


def test_queen_can_capture_enemy_piece_but_stops_after_it():
    board = Board()
    board.squares = {
        "d4": Piece(Color.WHITE, PieceType.QUEEN),
        "f6": Piece(Color.BLACK, PieceType.KNIGHT),
    }

    moves = get_queen_moves(board, "d4")

    assert "e5" in moves
    assert "f6" in moves
    assert "g7" not in moves


def test_non_queen_has_no_queen_moves():
    board = Board()

    assert get_queen_moves(board, "e2") == []
