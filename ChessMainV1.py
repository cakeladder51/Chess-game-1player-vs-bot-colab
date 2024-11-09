#to get coords of a piece, do piece_name.row, piece_name.col

import pygame 
import random

pygame.init()

valid_moves = []
pieces = []
current_turn = "White"
running = True
selected_piece = None
white_king = None
black_king = None

width = 500
height = 500
screen = pygame.display.set_mode((width, height))
 
white = (237, 232, 208)
black = (85, 43, 0)
red = (255, 87, 51)

rows = 8
columns = 8
square_size = width // columns

def draw_board():
    for i in range(rows):
        for j in range(columns):
            if (i + j) % 2 == 0:
                colour = white
            else:
                colour = black
            x = j * square_size
            y = i * square_size
            width = square_size
            height = square_size
            pygame.draw.rect(screen, colour, (x, y, width, height))


white_pawn = pygame.transform.scale(pygame.image.load("Chess bot folder\white_pawn.png"), (square_size, square_size))
Black_pawn = pygame.transform.scale(pygame.image.load("Chess bot folder\Black_pawn.png"), (square_size, square_size))
white_rook = pygame.transform.scale(pygame.image.load("Chess bot folder\white_rook.png"), (square_size, square_size))
Black_rook = pygame.transform.scale(pygame.image.load("Chess bot folder\Black_rook.png"), (square_size, square_size))
white_knight = pygame.transform.scale(pygame.image.load("Chess bot folder\white_knight.png"), (square_size, square_size))
Black_knight = pygame.transform.scale(pygame.image.load("Chess bot folder\Black_knight.png"), (square_size, square_size))
white_bishop = pygame.transform.scale(pygame.image.load("Chess bot folder\white_bishop.png"), (square_size, square_size))
Black_bishop = pygame.transform.scale(pygame.image.load("Chess bot folder\Black_bishop.png"), (square_size, square_size))
white_queen = pygame.transform.scale(pygame.image.load("Chess bot folder\white_queen.png"), (square_size, square_size))
Black_queen = pygame.transform.scale(pygame.image.load("Chess bot folder\Black_queen.png"), (square_size, square_size))
white__king = pygame.transform.scale(pygame.image.load("Chess bot folder\white_king.png"), (square_size, square_size))
Black__king = pygame.transform.scale(pygame.image.load("Chess bot folder\Black_king.png"), (square_size, square_size))

#Every piece has its own colour, row, column and image
class Piece:
    def __init__(self, colour, row, col, image):
        self.colour = colour
        self.row = row
        self.col = col
        self.image = image
        self.moved = False

    def draw(self, screen):
        x = self.col * square_size                     
        y = self.row * square_size
        screen.blit(self.image, (x, y))

#Returns piece position
def get_piece_at(row, col):
    for piece in pieces:
        if piece.row == row and piece.col == col:
            return piece
    return None


def is_in_check(colour):
    king_pos = (white_king.row, white_king.col) if colour == "White" else (black_king.row, black_king.col) 
    for piece in pieces:
        if piece.colour != colour:
            if is_valid_move(piece, king_pos[0], king_pos[1]):
                return True
    return False


def is_checkmate(colour):
    if not is_in_check(colour):
        return False

    for piece in pieces:
        if piece.colour == colour:
            for row in range(rows):
                for col in range(columns):
                    if is_valid_move(piece, row, col):
                        original_row, original_col = piece.row, piece.col
                        piece.row, piece.col = row, col
                        if not is_in_check(colour):
                            piece.row, piece.col = original_row, original_col  
                            return False
                        piece.row, piece.col = original_row, original_col  
    return True


def is_valid_move(piece, target_row, target_col):
    target_piece = get_piece_at(target_row, target_col)
   
    # Prevent moving to squares occupied by the same color
    if target_piece is not None and target_piece.colour == piece.colour:
        return False  

    # Define move rules for different types of pieces
    if piece.image == white_pawn or piece.image == Black_pawn:  # Pawn movement
        direction = -1 if piece.colour == "White" else 1
        start_row = 6 if piece.colour == "White" else 1
        # Forward move
        if target_col == piece.col and (target_row == piece.row + direction or (piece.row == start_row and target_row == piece.row + 2 * direction)):
            return target_piece is None  # Must be an empty square
        # Capture
        if abs(target_col - piece.col) == 1 and target_row == piece.row + direction:
            return target_piece is not None and target_piece.colour != piece.colour  # Must capture an enemy piece

    elif piece.image == white_rook or piece.image == Black_rook:  # Rook movement
        if piece.col == target_col or piece.row == target_row:
            for r in range(min(piece.row, target_row) + 1, max(piece.row, target_row)):
                if get_piece_at(r, piece.col) is not None:
                    return False
            for c in range(min(piece.col, target_col) + 1, max(piece.col, target_col)):
                if get_piece_at(piece.row, c) is not None:
                    return False
            return True

    elif piece.image == white_knight or piece.image == Black_knight:  # Knight movement
        if (abs(piece.row - target_row) == 2 and abs(piece.col - target_col) == 1) or (abs(piece.row - target_row) == 1 and abs(piece.col - target_col) == 2):
            return True

    elif piece.image == white_bishop or piece.image == Black_bishop:  # Bishop movement
        if abs(piece.row - target_row) == abs(piece.col - target_col):
            row_step = 1 if target_row > piece.row else -1
            col_step = 1 if target_col > piece.col else -1
            for i in range(1, abs(target_row - piece.row)):
                if get_piece_at(piece.row + i * row_step, piece.col + i * col_step) is not None:
                    return False
            return True

    elif piece.image == white_queen or piece.image == Black_queen:  # Queen movement
        if (piece.col == target_col or piece.row == target_row) or (abs(piece.row - target_row) == abs(piece.col - target_col)):
            if piece.col == target_col:
                for r in range(min(piece.row, target_row) + 1, max(piece.row, target_row)):
                    if get_piece_at(r, piece.col) is not None:
                        return False
            elif piece.row == target_row:
                for c in range(min(piece.col, target_col) + 1, max(piece.col, target_col)):
                    if get_piece_at(piece.row, c) is not None:
                        return False
            else:
                row_step = 1 if target_row > piece.row else -1
                col_step = 1 if target_col > piece.col else -1
                for i in range(1, abs(target_row - piece.row)):
                    if get_piece_at(piece.row + i * row_step, piece.col + i * col_step) is not None:
                        return False
            return True

    elif piece.image == white__king or piece.image == Black__king:  # King movement
        if max(abs(piece.row - target_row), abs(piece.col - target_col)) == 1:
            return True

    return False


def get_valid_moves(piece):
    valid_moves = []
    for row in range(rows):
        for col in range(columns):
            if is_valid_move(piece, row, col):
                valid_moves.append((row, col))
    return valid_moves

def handle_player_click(pos):
    global selected_piece, current_turn, valid_moves

    col = pos[0] // square_size
    row = pos[1] // square_size

    if selected_piece:
        # If a piece is already selected, try to move it
        if (row, col) in valid_moves:  # Check if the clicked square is a valid move
            target_piece = get_piece_at(row, col)
            if target_piece and target_piece.colour != selected_piece.colour:
                pieces.remove(target_piece)  # Remove the captured piece from the list
            
            # Move the selected piece
            selected_piece.row = row
            selected_piece.col = col
            selected_piece.moved = True
            valid_moves = []  # Clear valid moves after moving
            current_turn = "Black" if current_turn == "White" else "White"
            selected_piece = None  # Deselect the piece
        else:
            selected_piece = None  # Deselect if move is invalid
            valid_moves = []  # Clear valid moves
    else:
        # Select a piece and calculate its valid moves
        for piece in pieces:
            if piece.col == col and piece.row == row and piece.colour == current_turn:
                selected_piece = piece
                valid_moves = get_valid_moves(selected_piece)  # Get valid moves for the selected piece
                break
def bot_turn():
    global current_turn

   
    if is_in_check("Black"):
     
        for row in range(rows):
            for col in range(columns):
                if is_valid_move(black_king, row, col):
                    
                    original_row, original_col = black_king.row, black_king.col
                    black_king.row = row
                    black_king.col = col
                    
                
                    if not is_in_check("Black"):
                      
                        target_piece = get_piece_at(row, col)
                        if target_piece:
                            pieces.remove(target_piece)  
                        
                        current_turn = "White"  
                        return 

                    
                    black_king.row = original_row
                    black_king.col = original_col
      
        return  


    bot_pieces = [piece for piece in pieces if piece.colour == "Black"]
    all_moves = []
    
    for bot_piece in bot_pieces:
        for row in range(rows):
            for col in range(columns):
                if is_valid_move(bot_piece, row, col):
           
                    original_row, original_col = bot_piece.row, bot_piece.col
                    target_piece = get_piece_at(row, col)
                    
                 
                    bot_piece.row = row
                    bot_piece.col = col
                    
                    if target_piece:
                        pieces.remove(target_piece)
                    
            
                    if not is_in_check("Black"):
                        all_moves.append((bot_piece, original_row, original_col, row, col))  
                    
               
                    bot_piece.row = original_row
                    bot_piece.col = original_col
                    if target_piece:
                        pieces.append(target_piece)  
                    
    if all_moves:
        selected_move = random.choice(all_moves)
        piece_to_move, original_row, original_col, new_row, new_col = selected_move
        
        piece_to_move.row = new_row
        piece_to_move.col = new_col
        
 
        if is_in_check("White"):
            if is_checkmate("White"):
                print("Checkmate! Black wins!")
            else:
                print("\n")
        else:
            current_turn = "White" 



for i in range(columns):
    pieces.append(Piece("White", 6, i, white_pawn))
    pieces.append(Piece("Black", 1, i, Black_pawn))
pieces.append(Piece("White", 7, 0, white_rook))
pieces.append(Piece("White", 7, 1, white_knight))
pieces.append(Piece("White", 7, 2, white_bishop))
pieces.append(Piece("White", 7, 3, white_queen))
white_king = Piece("White", 7, 4, white__king)  
pieces.append(white_king)
pieces.append(Piece("White", 7, 5, white_bishop))
pieces.append(Piece("White", 7, 6, white_knight))
pieces.append(Piece("White", 7, 7, white_rook))
pieces.append(Piece("Black", 0, 0, Black_rook))
pieces.append(Piece("Black", 0, 1, Black_knight))
pieces.append(Piece("Black", 0, 2, Black_bishop))
pieces.append(Piece("Black", 0, 3, Black_queen))
black_king = Piece("Black", 0, 4, Black__king)  
pieces.append(black_king)
pieces.append(Piece("Black", 0, 5, Black_bishop))
pieces.append(Piece("Black", 0, 6, Black_knight))
pieces.append(Piece("Black", 0, 7, Black_rook))

# Main loop to draw the board and pieces
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_player_click(pygame.mouse.get_pos())

    screen.fill(white)
    draw_board()
    
    for move in valid_moves:
        row, col = move
        x = col * square_size
        y = row * square_size
        pygame.draw.circle(screen, (0, 255, 0), (x + square_size // 2, y + square_size // 2), 10)
    
    # Draw each piece still in the pieces list
    for piece in pieces:
        piece.draw(screen)

    pygame.display.flip()

    # Let the bot move if it's the bot's turn
    if current_turn == "Black":
        bot_turn()

pygame.quit()
