from backend.app.chess.board import Board
from backend.app.chess.pieces import Color, Piece, PieceType


def test_clone_has_an_independent_copy_of_board_squares():
    board = Board()

    cloned_board = board.clone()
    cloned_board.remove_piece("e2")
    cloned_board.set_piece("e4", Piece(Color.WHITE, PieceType.PAWN))

    assert board.get_piece("e2").type == PieceType.PAWN
    assert board.get_piece("e4") is None
    assert cloned_board.get_piece("e2") is None
    assert cloned_board.get_piece("e4").type == PieceType.PAWN
