import pygame 
import random


pygame.init()


width, height = 400, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess Game")
white = (255, 255, 255)
green = (0, 200, 0)


rows, columns = 8, 8
square_size = width // columns


wpi = pygame.transform.scale(pygame.image.load("white_pawn.png"), (square_size, square_size))
bpi = pygame.transform.scale(pygame.image.load("black_pawn.png"), (square_size, square_size))
wri = pygame.transform.scale(pygame.image.load("white_rook.png"), (square_size, square_size))
bri = pygame.transform.scale(pygame.image.load("black_rook.png"), (square_size, square_size))
wki = pygame.transform.scale(pygame.image.load("white_knight.png"), (square_size, square_size))
bki = pygame.transform.scale(pygame.image.load("black_knight.png"), (square_size, square_size))
wbi = pygame.transform.scale(pygame.image.load("white_bishop.png"), (square_size, square_size))
bbi = pygame.transform.scale(pygame.image.load("black_bishop.png"), (square_size, square_size))
wqi = pygame.transform.scale(pygame.image.load("white_queen.png"), (square_size, square_size))
bqi = pygame.transform.scale(pygame.image.load("black_queen.png"), (square_size, square_size))
wkii = pygame.transform.scale(pygame.image.load("white_king.png"), (square_size, square_size))
bkii = pygame.transform.scale(pygame.image.load("black_king.png"), (square_size, square_size))


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


pieces = []
current_turn = "White"
running = True
selected_piece = None
white_king = None
black_king = None

def draw_board():
    for row in range(rows):
        for col in range(columns):
            colour = white if (row + col) % 2 == 0 else green
            pygame.draw.rect(screen, colour, (col * square_size, row * square_size, square_size, square_size))


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

   
    if target_piece is not None and target_piece.colour == piece.colour:
        return False  
    
    if piece.image == wpi or piece.image == bpi: 
        direction = -1 if piece.colour == "White" else 1
        start_row = 6 if piece.colour == "White" else 1
        if target_col == piece.col and (target_row == piece.row + direction or (piece.row == start_row and target_row == piece.row + 2 * direction)):
            return target_piece is None  
        if abs(target_col - piece.col) == 1 and target_row == piece.row + direction:
            return target_piece is not None and target_piece.colour != piece.colour  

    elif piece.image == wri or piece.image == bri:  
        if piece.col == target_col or piece.row == target_row:
            for r in range(min(piece.row, target_row) + 1, max(piece.row, target_row)):
                if get_piece_at(r, piece.col) is not None:
                    return False
            for c in range(min(piece.col, target_col) + 1, max(piece.col, target_col)):
                if get_piece_at(piece.row, c) is not None:
                    return False
            return True

    elif piece.image == wki or piece.image == bki:  
        if (abs(piece.row - target_row) == 2 and abs(piece.col - target_col) == 1) or (abs(piece.row - target_row) == 1 and abs(piece.col - target_col) == 2):
            return True

    elif piece.image == wbi or piece.image == bbi:  
        if abs(piece.row - target_row) == abs(piece.col - target_col):
            row_step = 1 if target_row > piece.row else -1
            col_step = 1 if target_col > piece.col else -1
            for i in range(1, abs(target_row - piece.row)):
                if get_piece_at(piece.row + i * row_step, piece.col + i * col_step) is not None:
                    return False
            return True

    elif piece.image == wqi or piece.image == bqi:
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

    elif piece.image == wkii or piece.image == bkii:  # Kings
        if max(abs(piece.row - target_row), abs(piece.col - target_col)) == 1:
            return True

    return False

def handle_player_click(pos):
    global selected_piece, current_turn

    col = pos[0] // square_size
    row = pos[1] // square_size

    if selected_piece:
        if is_valid_move(selected_piece, row, col):
            target_piece = get_piece_at(row, col)
            if target_piece:
                pieces.remove(target_piece) 
            original_row, original_col = selected_piece.row, selected_piece.col
            selected_piece.row = row
            selected_piece.col = col
            selected_piece.moved = True

            if is_in_check("Black"):
                if is_checkmate("Black"):
                    print("Checkmate! White wins!")
                    
                else:
                    print("/n")
                    
            
            elif is_in_check("White"):
                selected_piece.row = original_row
                selected_piece.col = original_col
                
            else:
                current_turn = "Black" if current_turn == "White" else "White"
                
            selected_piece = None  
        else:
            selected_piece = None  
    else:
        for piece in pieces:
            if piece.col == col and piece.row == row and piece.colour == current_turn:
                selected_piece = piece
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
                print("/n")
        else:
            current_turn = "White" 


for i in range(columns):
    pieces.append(Piece("White", 6, i, wpi))
    pieces.append(Piece("Black", 1, i, bpi))
pieces.append(Piece("White", 7, 0, wri))
pieces.append(Piece("White", 7, 1, wki))
pieces.append(Piece("White", 7, 2, wbi))
pieces.append(Piece("White", 7, 3, wqi))
white_king = Piece("White", 7, 4, wkii)  
pieces.append(white_king)
pieces.append(Piece("White", 7, 5, wbi))
pieces.append(Piece("White", 7, 6, wki))
pieces.append(Piece("White", 7, 7, wri))
pieces.append(Piece("Black", 0, 0, bri))
pieces.append(Piece("Black", 0, 1, bki))
pieces.append(Piece("Black", 0, 2, bbi))
pieces.append(Piece("Black", 0, 3, bqi))
black_king = Piece("Black", 0, 4, bkii)  
pieces.append(black_king)
pieces.append(Piece("Black", 0, 5, bbi))
pieces.append(Piece("Black", 0, 6, bki))
pieces.append(Piece("Black", 0, 7, bri))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_player_click(pygame.mouse.get_pos())

    screen.fill(white)
    draw_board()
    for piece in pieces:
        piece.draw(screen)

    pygame.display.flip()


    if current_turn == "Black":
        bot_turn()

pygame.quit() 

