from dataclasses import dataclass
from enum import Enum

class Color(Enum):
    WHITE = "white"
    BLACK = "black"


class PieceType(Enum):
    KING = "king"
    QUEEN = "queen"
    ROOK = "rook"
    BISHOP = "bishop"
    KNIGHT = "knight"
    PAWN = "pawn"


@dataclass(frozen=True)
class Piece:
    color: Color
    type: PieceType
