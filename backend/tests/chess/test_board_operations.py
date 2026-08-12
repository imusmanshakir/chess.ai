from backend.app.chess.board import Board
from backend.app.chess.pieces import Color, Piece, PieceType


def test_get_piece():
    board = Board()

    piece = board.get_piece("e1")

    assert piece.color == Color.WHITE
    assert piece.type == PieceType.KING


def test_set_piece():
    board = Board()

    knight = Piece(Color.WHITE, PieceType.KNIGHT)
    board.set_piece("e4", knight)

    assert board.get_piece("e4") == knight


def test_remove_piece():
    board = Board()

    piece = board.remove_piece("e2")

    assert piece.color == Color.WHITE
    assert piece.type == PieceType.PAWN
    assert board.get_piece("e2") is None
