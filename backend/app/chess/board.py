from backend.app.chess.pieces import Color, Piece, PieceType


class Board:
    def __init__(self):
        self.squares = {}
        self._setup_initial_position()

    def _setup_initial_position(self):
        # White pieces
        self.squares["a1"] = Piece(Color.WHITE, PieceType.ROOK)
        self.squares["b1"] = Piece(Color.WHITE, PieceType.KNIGHT)
        self.squares["c1"] = Piece(Color.WHITE, PieceType.BISHOP)
        self.squares["d1"] = Piece(Color.WHITE, PieceType.QUEEN)
        self.squares["e1"] = Piece(Color.WHITE, PieceType.KING)
        self.squares["f1"] = Piece(Color.WHITE, PieceType.BISHOP)
        self.squares["g1"] = Piece(Color.WHITE, PieceType.KNIGHT)
        self.squares["h1"] = Piece(Color.WHITE, PieceType.ROOK)

        for file in "abcdefgh":
            self.squares[f"{file}2"] = Piece(Color.WHITE, PieceType.PAWN)

        # Black pieces
        self.squares["a8"] = Piece(Color.BLACK, PieceType.ROOK)
        self.squares["b8"] = Piece(Color.BLACK, PieceType.KNIGHT)
        self.squares["c8"] = Piece(Color.BLACK, PieceType.BISHOP)
        self.squares["d8"] = Piece(Color.BLACK, PieceType.QUEEN)
        self.squares["e8"] = Piece(Color.BLACK, PieceType.KING)
        self.squares["f8"] = Piece(Color.BLACK, PieceType.BISHOP)
        self.squares["g8"] = Piece(Color.BLACK, PieceType.KNIGHT)
        self.squares["h8"] = Piece(Color.BLACK, PieceType.ROOK)

        for file in "abcdefgh":
            self.squares[f"{file}7"] = Piece(Color.BLACK, PieceType.PAWN)

    def get_piece(self, square):
        return self.squares.get(square)

    def set_piece(self, square, piece):
        self.squares[square] = piece

    def remove_piece(self, square):
        return self.squares.pop(square, None) # The expression pop(square, None) is used with a Python dictionary. It removes the key square from the dictionary and returns its value. If the key does not exist, it safely returns None instead of raising a KeyError.
   
    def is_valid_square(self, square):
     if len(square) != 2: # len("e4")--> 2, len("abc")-->3
      return False
     file, rank = square # This is called unpacking.
     return file in "abcdefgh" and rank in "12345678"
