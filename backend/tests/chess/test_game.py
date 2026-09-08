from backend.app.chess.game import GameState, GameStatus, InvalidMoveError, Move
from backend.app.chess.board import Board
from backend.app.chess.pieces import Color, Piece, PieceType


def test_game_starts_with_white_to_move():
    game = GameState()

    assert game.current_turn == Color.WHITE


def test_apply_move_moves_piece_and_switches_turn():
    game = GameState()

    captured_piece = game.apply_move(Move("e2", "e4"))

    assert captured_piece is None
    assert game.board.get_piece("e2") is None
    assert game.board.get_piece("e4").type == PieceType.PAWN
    assert game.current_turn == Color.BLACK


def test_apply_move_rejects_a_move_out_of_turn():
    game = GameState()

    try:
        game.apply_move(Move("e7", "e5"))
        assert False, "Expected an InvalidMoveError."
    except InvalidMoveError as error:
        assert "white's turn" in str(error)

    assert game.board.get_piece("e7").type == PieceType.PAWN
    assert game.current_turn == Color.WHITE


def test_apply_move_rejects_a_move_from_an_empty_square():
    game = GameState()

    try:
        game.apply_move(Move("e4", "e5"))
        assert False, "Expected an InvalidMoveError."
    except InvalidMoveError as error:
        assert "no piece" in str(error)


def test_apply_move_rejects_a_piece_move_not_in_its_generated_moves():
    game = GameState()

    try:
        game.apply_move(Move("e2", "e5"))
        assert False, "Expected an InvalidMoveError."
    except InvalidMoveError as error:
        assert "cannot move" in str(error)

    assert game.board.get_piece("e2").type == PieceType.PAWN
    assert game.current_turn == Color.WHITE


def test_apply_move_captures_an_enemy_piece():
    game = GameState()
    game.apply_move(Move("e2", "e4"))
    game.apply_move(Move("d7", "d5"))

    captured_piece = game.apply_move(Move("e4", "d5"))

    assert captured_piece is not None
    assert captured_piece.color == Color.BLACK
    assert captured_piece.type == PieceType.PAWN
    assert game.board.get_piece("d5").color == Color.WHITE
    assert game.current_turn == Color.BLACK


def test_apply_move_rejects_a_move_that_exposes_its_king_to_check():
    board = Board()
    board.squares = {
        "e1": Piece(Color.WHITE, PieceType.KING),
        "e2": Piece(Color.WHITE, PieceType.KNIGHT),
        "a8": Piece(Color.BLACK, PieceType.KING),
        "e8": Piece(Color.BLACK, PieceType.ROOK),
    }
    game = GameState(board)

    try:
        game.apply_move(Move("e2", "c3"))
        assert False, "Expected an InvalidMoveError."
    except InvalidMoveError as error:
        assert "king in check" in str(error)

    assert game.board.get_piece("e2").type == PieceType.KNIGHT
    assert game.current_turn == Color.WHITE


def test_apply_move_allows_a_move_that_blocks_check():
    board = Board()
    board.squares = {
        "e1": Piece(Color.WHITE, PieceType.KING),
        "d2": Piece(Color.WHITE, PieceType.BISHOP),
        "a8": Piece(Color.BLACK, PieceType.KING),
        "e8": Piece(Color.BLACK, PieceType.ROOK),
    }
    game = GameState(board)

    game.apply_move(Move("d2", "e3"))

    assert game.board.get_piece("e3").type == PieceType.BISHOP
    assert not game.is_in_check(Color.WHITE)
    assert game.current_turn == Color.BLACK


def test_apply_move_rejects_a_king_move_to_an_attacked_square():
    board = Board()
    board.squares = {
        "e1": Piece(Color.WHITE, PieceType.KING),
        "a8": Piece(Color.BLACK, PieceType.KING),
        "e8": Piece(Color.BLACK, PieceType.ROOK),
    }
    game = GameState(board)

    try:
        game.apply_move(Move("e1", "e2"))
        assert False, "Expected an InvalidMoveError."
    except InvalidMoveError as error:
        assert "king in check" in str(error)


def test_apply_move_promotes_a_pawn_on_the_final_rank():
    board = Board()
    board.squares = {
        "e1": Piece(Color.WHITE, PieceType.KING),
        "e7": Piece(Color.WHITE, PieceType.PAWN),
        "a8": Piece(Color.BLACK, PieceType.KING),
    }
    game = GameState(board)

    game.apply_move(Move("e7", "e8", promotion=PieceType.QUEEN))

    promoted_piece = game.board.get_piece("e8")
    assert promoted_piece.color == Color.WHITE
    assert promoted_piece.type == PieceType.QUEEN
    assert game.current_turn == Color.BLACK


def test_apply_move_promotes_after_capturing_on_the_final_rank():
    board = Board()
    board.squares = {
        "e1": Piece(Color.WHITE, PieceType.KING),
        "e7": Piece(Color.WHITE, PieceType.PAWN),
        "d8": Piece(Color.BLACK, PieceType.ROOK),
        "a8": Piece(Color.BLACK, PieceType.KING),
    }
    game = GameState(board)

    captured_piece = game.apply_move(Move("e7", "d8", promotion=PieceType.KNIGHT))

    assert captured_piece.type == PieceType.ROOK
    assert game.board.get_piece("d8") == Piece(Color.WHITE, PieceType.KNIGHT)


def test_apply_move_rejects_a_pawn_reaching_final_rank_without_promotion():
    board = Board()
    board.squares = {
        "e1": Piece(Color.WHITE, PieceType.KING),
        "e7": Piece(Color.WHITE, PieceType.PAWN),
        "a8": Piece(Color.BLACK, PieceType.KING),
    }
    game = GameState(board)

    try:
        game.apply_move(Move("e7", "e8"))
        assert False, "Expected an InvalidMoveError."
    except InvalidMoveError as error:
        assert "must promote" in str(error)

    assert game.board.get_piece("e7").type == PieceType.PAWN
    assert game.board.get_piece("e8") is None


def test_apply_move_rejects_invalid_promotion_piece_type():
    board = Board()
    board.squares = {
        "e1": Piece(Color.WHITE, PieceType.KING),
        "e7": Piece(Color.WHITE, PieceType.PAWN),
        "a8": Piece(Color.BLACK, PieceType.KING),
    }
    game = GameState(board)

    try:
        game.apply_move(Move("e7", "e8", promotion=PieceType.KING))
        assert False, "Expected an InvalidMoveError."
    except InvalidMoveError as error:
        assert "must promote" in str(error)


def test_apply_move_rejects_promotion_before_the_final_rank():
    game = GameState()

    try:
        game.apply_move(Move("e2", "e4", promotion=PieceType.QUEEN))
        assert False, "Expected an InvalidMoveError."
    except InvalidMoveError as error:
        assert "Only a pawn" in str(error)


def test_apply_move_captures_en_passant_on_the_immediately_next_turn():
    game = GameState()
    game.apply_move(Move("e2", "e4"))
    game.apply_move(Move("a7", "a6"))
    game.apply_move(Move("e4", "e5"))
    game.apply_move(Move("d7", "d5"))

    captured_piece = game.apply_move(Move("e5", "d6"))

    assert captured_piece == Piece(Color.BLACK, PieceType.PAWN)
    assert game.board.get_piece("d5") is None
    assert game.board.get_piece("d6") == Piece(Color.WHITE, PieceType.PAWN)
    assert game.en_passant_target is None
    assert game.current_turn == Color.BLACK


def test_en_passant_expires_after_another_move():
    game = GameState()
    game.apply_move(Move("e2", "e4"))
    game.apply_move(Move("a7", "a6"))
    game.apply_move(Move("e4", "e5"))
    game.apply_move(Move("d7", "d5"))
    game.apply_move(Move("a2", "a3"))
    game.apply_move(Move("h7", "h6"))

    try:
        game.apply_move(Move("e5", "d6"))
        assert False, "Expected an InvalidMoveError."
    except InvalidMoveError as error:
        assert "cannot move" in str(error)


def test_apply_move_castles_king_side_and_moves_rook():
    board = Board()
    board.squares = {
        "e1": Piece(Color.WHITE, PieceType.KING),
        "h1": Piece(Color.WHITE, PieceType.ROOK),
        "a8": Piece(Color.BLACK, PieceType.KING),
    }
    game = GameState(
        board,
        castling_rights={Color.WHITE: {"king_side"}, Color.BLACK: set()},
    )

    game.apply_move(Move("e1", "g1"))

    assert game.board.get_piece("g1") == Piece(Color.WHITE, PieceType.KING)
    assert game.board.get_piece("f1") == Piece(Color.WHITE, PieceType.ROOK)
    assert game.board.get_piece("e1") is None
    assert game.board.get_piece("h1") is None
    assert game.castling_rights[Color.WHITE] == set()


def test_apply_move_castles_black_queen_side_and_moves_rook():
    board = Board()
    board.squares = {
        "h1": Piece(Color.WHITE, PieceType.KING),
        "a8": Piece(Color.BLACK, PieceType.ROOK),
        "e8": Piece(Color.BLACK, PieceType.KING),
    }
    game = GameState(
        board,
        castling_rights={Color.WHITE: set(), Color.BLACK: {"queen_side"}},
    )
    game.current_turn = Color.BLACK

    game.apply_move(Move("e8", "c8"))

    assert game.board.get_piece("c8") == Piece(Color.BLACK, PieceType.KING)
    assert game.board.get_piece("d8") == Piece(Color.BLACK, PieceType.ROOK)


def test_apply_move_rejects_castling_through_an_attacked_square():
    board = Board()
    board.squares = {
        "e1": Piece(Color.WHITE, PieceType.KING),
        "h1": Piece(Color.WHITE, PieceType.ROOK),
        "a8": Piece(Color.BLACK, PieceType.KING),
        "f8": Piece(Color.BLACK, PieceType.ROOK),
    }
    game = GameState(
        board,
        castling_rights={Color.WHITE: {"king_side"}, Color.BLACK: set()},
    )

    try:
        game.apply_move(Move("e1", "g1"))
        assert False, "Expected an InvalidMoveError."
    except InvalidMoveError as error:
        assert "cannot move" in str(error)


def test_rook_movement_removes_its_castling_right():
    board = Board()
    board.squares = {
        "e1": Piece(Color.WHITE, PieceType.KING),
        "h1": Piece(Color.WHITE, PieceType.ROOK),
        "a8": Piece(Color.BLACK, PieceType.KING),
    }
    game = GameState(
        board,
        castling_rights={Color.WHITE: {"king_side"}, Color.BLACK: set()},
    )

    game.apply_move(Move("h1", "h2"))
    game.current_turn = Color.WHITE
    game.apply_move(Move("h2", "h1"))
    game.current_turn = Color.WHITE

    try:
        game.apply_move(Move("e1", "g1"))
        assert False, "Expected an InvalidMoveError."
    except InvalidMoveError as error:
        assert "cannot move" in str(error)


def test_game_status_reports_checkmate_and_prevents_further_moves():
    board = Board()
    board.squares = {
        "c6": Piece(Color.WHITE, PieceType.KING),
        "b7": Piece(Color.WHITE, PieceType.QUEEN),
        "a8": Piece(Color.BLACK, PieceType.KING),
    }
    game = GameState(board, castling_rights={})
    game.current_turn = Color.BLACK

    assert game.get_status() == GameStatus.WHITE_WON_BY_CHECKMATE

    try:
        game.apply_move(Move("a8", "b8"))
        assert False, "Expected an InvalidMoveError."
    except InvalidMoveError as error:
        assert "already over" in str(error)


def test_game_status_reports_stalemate():
    board = Board()
    board.squares = {
        "c6": Piece(Color.WHITE, PieceType.KING),
        "c7": Piece(Color.WHITE, PieceType.QUEEN),
        "a8": Piece(Color.BLACK, PieceType.KING),
    }
    game = GameState(board, castling_rights={})
    game.current_turn = Color.BLACK

    assert game.get_status() == GameStatus.STALEMATE
