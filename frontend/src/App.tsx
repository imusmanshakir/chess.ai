import { useEffect, useState } from 'react'
import './App.css'

type Color = 'white' | 'black'
type PieceType = 'king' | 'queen' | 'rook' | 'bishop' | 'knight' | 'pawn'

type Piece = {
  color: Color
  type: PieceType
}

type Game = {
  game_id: string
  board: Record<string, Piece>
  current_turn: Color
  status: string
}

const files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
const ranks = ['8', '7', '6', '5', '4', '3', '2', '1']
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

const pieceSymbols: Record<Color, Record<PieceType, string>> = {
  white: { king: '♔', queen: '♕', rook: '♖', bishop: '♗', knight: '♘', pawn: '♙' },
  black: { king: '♚', queen: '♛', rook: '♜', bishop: '♝', knight: '♞', pawn: '♟' },
}

const formatStatus = (status: string) => status.replaceAll('_', ' ')

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${apiBaseUrl}${path}`, options)

  if (!response.ok) {
    const body = (await response.json().catch(() => null)) as { detail?: string } | null
    throw new Error(body?.detail ?? 'The server could not complete that request.')
  }

  return response.json() as Promise<T>
}

function App() {
  const [game, setGame] = useState<Game | null>(null)
  const [selectedSquare, setSelectedSquare] = useState<string | null>(null)
  const [legalMoves, setLegalMoves] = useState<string[]>([])
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const createGame = async () => {
    setIsLoading(true)
    setError(null)
    setSelectedSquare(null)
    setLegalMoves([])

    try {
      setGame(await request<Game>('/api/games', { method: 'POST' }))
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Unable to create a game.')
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    let isCurrent = true

    void request<Game>('/api/games', { method: 'POST' })
      .then((createdGame) => {
        if (isCurrent) setGame(createdGame)
      })
      .catch((requestError: unknown) => {
        if (isCurrent) {
          setError(requestError instanceof Error ? requestError.message : 'Unable to create a game.')
        }
      })
      .finally(() => {
        if (isCurrent) setIsLoading(false)
      })

    return () => {
      isCurrent = false
    }
  }, [])

  const selectSquare = async (square: string) => {
    if (!game) return

    setSelectedSquare(square)
    setLegalMoves([])
    setError(null)
    setIsSubmitting(true)

    try {
      const response = await request<{ moves: string[] }>(
        `/api/games/${game.game_id}/legal-moves?from_square=${square}`,
      )
      setLegalMoves(response.moves)
    } catch (requestError) {
      setSelectedSquare(null)
      setError(requestError instanceof Error ? requestError.message : 'Unable to load legal moves.')
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleSquareClick = async (square: string) => {
    if (!game || isSubmitting || game.status !== 'in_progress') return

    const piece = game.board[square]

    if (selectedSquare === null) {
      if (piece?.color === game.current_turn) await selectSquare(square)
      return
    }

    if (square === selectedSquare) {
      setSelectedSquare(null)
      setLegalMoves([])
      return
    }

    if (piece?.color === game.current_turn) {
      await selectSquare(square)
      return
    }

    if (!legalMoves.includes(square)) {
      setError('That is not a legal move for the selected piece.')
      return
    }

    const movingPiece = game.board[selectedSquare]
    const promotion =
      movingPiece?.type === 'pawn' && (square[1] === '1' || square[1] === '8')
        ? 'queen'
        : undefined

    setIsSubmitting(true)
    setError(null)

    try {
      const nextGame = await request<Game>(`/api/games/${game.game_id}/moves`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          from_square: selectedSquare,
          to_square: square,
          promotion,
        }),
      })
      setGame(nextGame)
      setSelectedSquare(null)
      setLegalMoves([])
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Unable to apply that move.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <main className="app-shell">
      <header className="site-header">
        <a className="brand" href="/" aria-label="Chess AI home">
          Chess<span>AI</span>
        </a>
        <p>Play. Review. Improve.</p>
      </header>

      <section className="game-layout" aria-label="Chess game">
        <div className="game-intro">
          <p className="eyebrow">Live game</p>
          <h1>Your game, made clearer.</h1>
          <p className="intro-copy">
            Every move is validated by the Python chess engine before the board updates.
          </p>
        </div>

        <div className="board-frame" aria-busy={isLoading || isSubmitting}>
          <div className="board-status">
            <div>
              <span className={`turn-dot ${game?.current_turn ?? 'white'}`} aria-hidden="true" />
              <strong>
                {isLoading ? 'Starting game…' : `${game?.current_turn === 'white' ? 'White' : 'Black'} to move`}
              </strong>
            </div>
            <span className="prototype-label">{game ? formatStatus(game.status) : 'Loading'}</span>
          </div>

          <div className="board" role="grid" aria-label="Chess board">
            {ranks.flatMap((rank, rankIndex) =>
              files.map((file, fileIndex) => {
                const square = `${file}${rank}`
                const isLight = (fileIndex + rankIndex) % 2 === 0
                const piece = game?.board[square]

                return (
                  <button
                    className={`square ${isLight ? 'light' : 'dark'} ${
                      selectedSquare === square ? 'selected' : ''
                    } ${legalMoves.includes(square) ? 'legal-move' : ''}`}
                    disabled={isLoading || isSubmitting || game?.status !== 'in_progress'}
                    key={square}
                    onClick={() => void handleSquareClick(square)}
                    type="button"
                    role="gridcell"
                    aria-label={`${square}${piece ? `, ${piece.color} ${piece.type}` : ', empty'}`}
                  >
                    {file === 'a' && <span className="rank-label">{rank}</span>}
                    {piece && <span className="piece">{pieceSymbols[piece.color][piece.type]}</span>}
                    {rank === '1' && <span className="file-label">{file}</span>}
                  </button>
                )
              }),
            )}
          </div>
        </div>

        <aside className="game-panel">
          <p className="eyebrow">Engine connected</p>
          <h2>Move tester</h2>
          <p>
            Select one of your pieces, then choose a highlighted destination. Legal
            moves, check safety, castling, en passant, and promotion are validated by Python.
          </p>
          {error && <p className="error-message" role="alert">{error}</p>}
          <button className="reset-button" onClick={() => void createGame()} type="button">
            New game
          </button>
          <div className="next-step">
            <span>Connected to</span>
            <strong>FastAPI chess engine</strong>
          </div>
        </aside>
      </section>
    </main>
  )
}

export default App
