import os
from threading import Lock
from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.app.chess.game import GameState, InvalidMoveError, Move
from backend.app.chess.pieces import Color, Piece, PieceType
from backend.app.chess.rules import get_legal_moves


class PieceResponse(BaseModel):
    color: Color
    type: PieceType


class GameResponse(BaseModel):
    game_id: str
    board: dict[str, PieceResponse]
    current_turn: Color
    status: str


class MoveRequest(BaseModel):
    from_square: str = Field(pattern="^[a-h][1-8]$")
    to_square: str = Field(pattern="^[a-h][1-8]$")
    promotion: PieceType | None = None


class LegalMovesResponse(BaseModel):
    moves: list[str]


app = FastAPI(title="Chess AI API", version="0.1.0")

frontend_origins = os.getenv(
    "FRONTEND_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173",
).split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

games: dict[str, GameState] = {}
games_lock = Lock()


def serialize_piece(piece: Piece) -> PieceResponse:
    return PieceResponse(color=piece.color, type=piece.type)


def serialize_game(game_id: str, game: GameState) -> GameResponse:
    return GameResponse(
        game_id=game_id,
        board={square: serialize_piece(piece) for square, piece in game.board.squares.items()},
        current_turn=game.current_turn,
        status=game.get_status().value,
    )


def get_game_or_404(game_id: str) -> GameState:
    with games_lock:
        game = games.get(game_id)

    if game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found.")

    return game


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/games", response_model=GameResponse, status_code=status.HTTP_201_CREATED)
def create_game() -> GameResponse:
    game_id = str(uuid4())
    game = GameState()

    with games_lock:
        games[game_id] = game

    return serialize_game(game_id, game)


@app.get("/api/games/{game_id}", response_model=GameResponse)
def get_game(game_id: str) -> GameResponse:
    game = get_game_or_404(game_id)

    return serialize_game(game_id, game)


@app.get("/api/games/{game_id}/legal-moves", response_model=LegalMovesResponse)
def get_legal_moves_for_square(game_id: str, from_square: str) -> LegalMovesResponse:
    game = get_game_or_404(game_id)
    piece = game.board.get_piece(from_square)

    if piece is None or piece.color != game.current_turn:
        return LegalMovesResponse(moves=[])

    moves = [
        to_square
        for source_square, to_square in get_legal_moves(
            game.board,
            game.current_turn,
            game.en_passant_target,
            game.castling_rights[game.current_turn],
        )
        if source_square == from_square
    ]

    return LegalMovesResponse(moves=moves)


@app.post("/api/games/{game_id}/moves", response_model=GameResponse)
def apply_move(game_id: str, move_request: MoveRequest) -> GameResponse:
    game = get_game_or_404(game_id)

    try:
        game.apply_move(
            Move(
                from_square=move_request.from_square,
                to_square=move_request.to_square,
                promotion=move_request.promotion,
            )
        )
    except InvalidMoveError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    return serialize_game(game_id, game)
