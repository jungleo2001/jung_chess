import chess
import chess.engine
import pygame
import os

# Initialize pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 800
BOARD_SIZE = 8
SQUARE_SIZE = WIDTH // BOARD_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jung Chess")

# Load piece images
piece_images = {}
for piece in ['bR', 'bK', 'bN', 'bP', 'bQ', 'bB', 'wR', 'wK', 'wN', 'wP', 'wQ', 'wB']:
    piece_images[piece] = pygame.image.load(os.path.join('images', piece + '.png'))

# Load Stockfish engine
engine = chess.engine.SimpleEngine.popen_uci("/home/dexhex/stockfish/stockfish")

# Draw the chessboard
def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = (255, 255, 255) if (row + col) % 2 == 0 else (0, 0, 0)
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Draw the pieces on the board
def draw_pieces(board, selected_piece, valid_moves):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board.piece_at(chess.square(col, 7 - row))
            if piece:
                piece_color = 'b' if piece.color == chess.BLACK else 'w'
                piece_symbol = piece_color + piece.symbol().upper()  # Construct piece symbol
                if piece_symbol in piece_images:
                    screen.blit(piece_images[piece_symbol], (col * SQUARE_SIZE, row * SQUARE_SIZE))
                else:
                    print("Image not found for piece:", piece_symbol)

    if selected_piece is not None:
        pygame.draw.rect(screen, (0, 255, 0), (chess.square_file(selected_piece) * SQUARE_SIZE,
                                               (7 - chess.square_rank(selected_piece)) * SQUARE_SIZE,
                                               SQUARE_SIZE, SQUARE_SIZE), 4)

    for move in valid_moves:
        pygame.draw.circle(screen, (0, 255, 0), ((chess.square_file(move.to_square) + 0.5) * SQUARE_SIZE,
                                                 (7 - chess.square_rank(move.to_square) + 0.5) * SQUARE_SIZE),
                           SQUARE_SIZE // 6)

# Make a move for the engine
def make_engine_move(board):
    result = engine.play(board, chess.engine.Limit(time=0.1))
    board.push(result.move)

# Main game loop
def main():
    # Initialize the chess board
    board = chess.Board()

    running = True
    selected_piece = None
    valid_moves = []
    human_vs_human = True

    # Menu toggle
    font = pygame.font.Font(None, 36)
    menu_text = font.render("Press 'C' to switch mode (Human vs. Human)", True, (0, 255, 0))
    menu_rect = menu_text.get_rect(center=(WIDTH // 2, HEIGHT - 30))

    while running and not board.is_game_over():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                col = event.pos[0] // SQUARE_SIZE
                row = 7 - (event.pos[1] // SQUARE_SIZE)
                square = chess.square(col, row)

                # Check if a piece is present on the clicked square
                piece = board.piece_at(square)
                if piece is not None and piece.color == board.turn:
                    selected_piece = square
                    valid_moves = [move for move in board.legal_moves if move.from_square == selected_piece]

            elif event.type == pygame.MOUSEBUTTONUP and selected_piece is not None:
                col = event.pos[0] // SQUARE_SIZE
                row = 7 - (event.pos[1] // SQUARE_SIZE)
                target_square = chess.square(col, row)

                # Check if the target square is a valid move for the selected piece
                if any(move.to_square == target_square for move in valid_moves):
                    board.push(chess.Move(selected_piece, target_square))
                    selected_piece = None
                    valid_moves = []

                    # If playing against the CPU, make its move
                    if not human_vs_human and not board.is_game_over() and board.turn == chess.BLACK:
                        make_engine_move(board)

                selected_piece = None
                valid_moves = []

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    human_vs_human = not human_vs_human
                    menu_text = font.render(f"Mode: {'Human vs. Human' if human_vs_human else 'Human vs. CPU'}", True, (0, 255, 0))

        # Draw the board and pieces
        draw_board()
        draw_pieces(board, selected_piece, valid_moves)
        screen.blit(menu_text, menu_rect)

        pygame.display.flip()

        # If playing against the CPU, make its move outside event loop
        if not human_vs_human and board.turn == chess.BLACK and not board.is_game_over():
            make_engine_move(board)

    pygame.quit()
    engine.quit()

if __name__ == "__main__":
    main()
