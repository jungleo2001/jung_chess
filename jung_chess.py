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
engine = chess.engine.SimpleEngine.popen_uci("stockfish/Stockfish/src/stockfish")

# Rest of the code...


def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = (255, 255, 255) if (row + col) % 2 == 0 else (0, 0, 0)
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board.piece_at(chess.square(col, 7 - row))
            if piece:
                piece_color = 'b' if piece.color == chess.BLACK else 'w'
                piece_symbol = piece_color + piece.symbol().upper()  # Construct piece symbol
                print("Piece symbol:", piece_symbol)  # Print piece symbol
                if piece_symbol in piece_images:
                    screen.blit(piece_images[piece_symbol], (col * SQUARE_SIZE, row * SQUARE_SIZE))
                else:
                    print("Image not found for piece:", piece_symbol)





def main():
    # Initialize the chess board
    board = chess.Board()

    running = True
    while running and not board.is_game_over():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the board and pieces
        draw_board()
        draw_pieces(board)

        # Update the display
        pygame.display.flip()

        if board.turn == chess.WHITE:
            # Human player's move
            move = None
            while move is None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        break
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        col = event.pos[0] // SQUARE_SIZE
                        row = 7 - (event.pos[1] // SQUARE_SIZE)
                        move = chess.square(col, row)

            if move is not None:
                board.push(chess.Move.from_uci(chess.square_name(move)))

        else:
            # CPU's turn (Using Stockfish)
            result = engine.play(board, chess.engine.Limit(time=0.1))
            board.push(result.move)

    pygame.quit()
    engine.quit()

if __name__ == "__main__":
    main()
