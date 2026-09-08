from dataclasses import dataclass
from enum import Enum

from backend.app.chess.board import Board
from backend.app.chess.moves import get_en_passant_capture_square, get_piece_moves
from backend.app.chess.pieces import Color, Piece, PieceType
from backend.app.chess.rules import (
    get_castling_moves,
    get_castling_rook_move,
    is_checkmate,
    is_in_check,
    is_stalemate,
    would_move_leave_king_in_check,
)


@dataclass(frozen=True)
class Move:
    from_square: str
    to_square: str
    promotion: PieceType | None = None


class InvalidMoveError(ValueError):
    """Raised when a move cannot be applied in the current game state."""


class GameStatus(Enum):
    IN_PROGRESS = "in_progress"
    WHITE_WON_BY_CHECKMATE = "white_won_by_checkmate"
    BLACK_WON_BY_CHECKMATE = "black_won_by_checkmate"
    STALEMATE = "stalemate"


PROMOTION_PIECE_TYPES = {
    PieceType.QUEEN,
    PieceType.ROOK,
    PieceType.BISHOP,
    PieceType.KNIGHT,
}


class GameState:
    def __init__(
        self,
        board: Board | None = None,
        castling_rights: dict[Color, set[str]] | None = None,
    ):
        self.board = board if board is not None else Board()
        self.current_turn = Color.WHITE
        self.en_passant_target: str | None = None
        default_castling_rights = {
            Color.WHITE: {"king_side", "queen_side"},
            Color.BLACK: {"king_side", "queen_side"},
        }
        provided_rights = (
            castling_rights
            if castling_rights is not None
            else default_castling_rights
        )
        self.castling_rights = {
            color: set(provided_rights.get(color, set())) for color in Color
        }

    def is_in_check(self, color: Color) -> bool:
        return is_in_check(self.board, color)

    def is_checkmate(self, color: Color) -> bool:
        return is_checkmate(
            self.board,
            color,
            self.en_passant_target,
            self.castling_rights[color],
        )

    def is_stalemate(self, color: Color) -> bool:
        return is_stalemate(
            self.board,
            color,
            self.en_passant_target,
            self.castling_rights[color],
        )

    def get_status(self) -> GameStatus:
        if self.is_checkmate(self.current_turn):
            return (
                GameStatus.BLACK_WON_BY_CHECKMATE
                if self.current_turn == Color.WHITE
                else GameStatus.WHITE_WON_BY_CHECKMATE
            )

        if self.is_stalemate(self.current_turn):
            return GameStatus.STALEMATE

        return GameStatus.IN_PROGRESS

    def apply_move(self, move: Move) -> Piece | None:
        if self.get_status() != GameStatus.IN_PROGRESS:
            raise InvalidMoveError("The game is already over.")

        moving_piece = self.board.get_piece(move.from_square)

        if moving_piece is None:
            raise InvalidMoveError(f"There is no piece on {move.from_square}.")

        if moving_piece.color != self.current_turn:
            raise InvalidMoveError(f"It is {self.current_turn.value}'s turn.")

        available_moves = get_piece_moves(
            self.board,
            move.from_square,
            self.en_passant_target,
        )

        if moving_piece.type == PieceType.KING:
            available_moves += get_castling_moves(
                self.board,
                moving_piece.color,
                self.castling_rights[moving_piece.color],
            )

        if move.to_square not in available_moves:
            raise InvalidMoveError(
                f"{moving_piece.type.value} cannot move from "
                f"{move.from_square} to {move.to_square}."
            )

        target_piece = self.board.get_piece(move.to_square)
        en_passant_capture_square = get_en_passant_capture_square(
            self.board,
            move.from_square,
            move.to_square,
            self.en_passant_target,
        )
        castling_rook_move = get_castling_rook_move(
            moving_piece.color,
            move.from_square,
            move.to_square,
        )

        if target_piece is not None and target_piece.type == PieceType.KING:
            raise InvalidMoveError("A king cannot be captured.")

        if would_move_leave_king_in_check(
            self.board,
            move.from_square,
            move.to_square,
            moving_piece.color,
            en_passant_capture_square,
            castling_rook_move,
        ):
            raise InvalidMoveError("A move cannot leave your king in check.")

        reaches_promotion_rank = (
            moving_piece.type == PieceType.PAWN
            and (
                (moving_piece.color == Color.WHITE and move.to_square[1] == "8")
                or (moving_piece.color == Color.BLACK and move.to_square[1] == "1")
            )
        )

        if reaches_promotion_rank:
            promotion_piece_type = move.promotion

            if (
                promotion_piece_type is None
                or promotion_piece_type not in PROMOTION_PIECE_TYPES
            ):
                raise InvalidMoveError(
                    "A pawn reaching the final rank must promote to a queen, rook, "
                    "bishop, or knight."
                )
            placed_piece = Piece(moving_piece.color, promotion_piece_type)
        elif move.promotion is not None:
            raise InvalidMoveError("Only a pawn on the final rank can promote.")
        else:
            placed_piece = moving_piece

        captured_piece = self.board.remove_piece(
            en_passant_capture_square or move.to_square
        )
        self.board.remove_piece(move.from_square)
        self.board.set_piece(move.to_square, placed_piece)

        if castling_rook_move is not None:
            rook_from_square, rook_to_square = castling_rook_move
            rook = self.board.remove_piece(rook_from_square)
            self.board.set_piece(rook_to_square, rook)

        self._update_castling_rights(
            moving_piece,
            move.from_square,
            captured_piece,
            en_passant_capture_square or move.to_square,
        )
        self.en_passant_target = None

        if (
            moving_piece.type == PieceType.PAWN
            and abs(int(move.to_square[1]) - int(move.from_square[1])) == 2
        ):
            middle_rank = (int(move.from_square[1]) + int(move.to_square[1])) // 2
            self.en_passant_target = f"{move.from_square[0]}{middle_rank}"
        self.current_turn = (
            Color.BLACK if self.current_turn == Color.WHITE else Color.WHITE
        )

        return captured_piece

    def _update_castling_rights(
        self,
        moving_piece: Piece,
        from_square: str,
        captured_piece: Piece | None,
        captured_square: str,
    ) -> None:
        if moving_piece.type == PieceType.KING:
            self.castling_rights[moving_piece.color].clear()

        if moving_piece.type == PieceType.ROOK:
            self._remove_rook_castling_right(moving_piece.color, from_square)

        if captured_piece is not None and captured_piece.type == PieceType.ROOK:
            self._remove_rook_castling_right(captured_piece.color, captured_square)

    def _remove_rook_castling_right(self, color: Color, square: str) -> None:
        rank = "1" if color == Color.WHITE else "8"

        if square == f"a{rank}":
            self.castling_rights[color].discard("queen_side")
        elif square == f"h{rank}":
            self.castling_rights[color].discard("king_side")
