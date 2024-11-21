import pygame

pygame.init()
width = 720
height = width
single_square_size = width // 8
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
square_colour = ""
peach = (237, 232, 208)
chocolate = (85, 43, 0)
highlight_colour = (128, 128, 128)

white_pawn = pygame.transform.scale(pygame.image.load("Chess bot folder/white_pawn.png"), (single_square_size, single_square_size))
Black_pawn = pygame.transform.scale(pygame.image.load("Chess bot folder/Black_pawn.png"), (single_square_size, single_square_size))
white_rook = pygame.transform.scale(pygame.image.load("Chess bot folder/white_rook.png"), (single_square_size, single_square_size))
Black_rook = pygame.transform.scale(pygame.image.load("Chess bot folder/Black_rook.png"), (single_square_size, single_square_size))
white_knight = pygame.transform.scale(pygame.image.load("Chess bot folder/white_knight.png"), (single_square_size, single_square_size))
Black_knight = pygame.transform.scale(pygame.image.load("Chess bot folder/Black_knight.png"), (single_square_size, single_square_size))
white_bishop = pygame.transform.scale(pygame.image.load("Chess bot folder/white_bishop.png"), (single_square_size, single_square_size))
Black_bishop = pygame.transform.scale(pygame.image.load("Chess bot folder/Black_bishop.png"), (single_square_size, single_square_size))
white_queen = pygame.transform.scale(pygame.image.load("Chess bot folder/white_queen.png"), (single_square_size, single_square_size))
Black_queen = pygame.transform.scale(pygame.image.load("Chess bot folder/Black_queen.png"), (single_square_size, single_square_size))
white__king = pygame.transform.scale(pygame.image.load("Chess bot folder/white_king.png"), (single_square_size, single_square_size))
Black__king = pygame.transform.scale(pygame.image.load("Chess bot folder/Black_king.png"), (single_square_size, single_square_size))

def load_position_from_fen(initilised_board, fen):
    piece_type_from_symbol = {
        "k" : Piece.King, "p" : Piece.Pawn, "n" : Piece.Knight,
        "b" : Piece.Bishop, "r" : Piece.Rook, "q" : Piece.Queen
        }
    fenBoard = fen.split(" ")[0]
    file = 0 
    rank = 7

    for symbol in fenBoard:
        if symbol == "/":
            rank -= 1   # / in fen string means to move to the next rank
            file = 0    # always start on file 0
        else:
            if (symbol.isdigit()):
                file += int(symbol)
            else:
                if symbol.isupper():
                    piece_colour = Piece.White
                else:
                    piece_colour = Piece.Black
                piece_type = piece_type_from_symbol[symbol.lower()]
                initilised_board.Square[rank * 8 + file] = piece_type | piece_colour
                file += 1

class Piece:
    Empty = 0
    King = 1
    Pawn = 2
    Knight = 3
    Bishop = 4
    Rook = 5
    Queen = 6

    White = 8
    Black = 16 

    # These numbers chosen because, if represented in 5 bits, 0 0 0 0 0 , the first two
    # represent the colour and last three represent the piece.
    # e.g. 1 0  1 0 1  is a black rook, 1 0 = black and 1 0 1 = rook

class Board:
    def __init__(self):
        self.Square = [Piece.Empty] * 64
        self.piece_images = {
            Piece.White | Piece.Pawn: white_pawn,
            Piece.Black | Piece.Pawn: Black_pawn,
            Piece.White | Piece.Rook: white_rook,
            Piece.Black | Piece.Rook: Black_rook,
            Piece.White | Piece.Knight: white_knight,
            Piece.Black | Piece.Knight: Black_knight,
            Piece.White | Piece.Bishop: white_bishop,
            Piece.Black | Piece.Bishop: Black_bishop,
            Piece.White | Piece.Queen: white_queen,
            Piece.Black | Piece.Queen: Black_queen,
            Piece.White | Piece.King: white__king,
            Piece.Black | Piece.King: Black__king
        }
    
    def get_Pawn_moves(self, row, file, colour):
        legal_moves = []
        if colour == Piece.White:
            direction = -1
        else:
            direction = 1
        if colour == Piece.White:
            start_row = 6         #if a pawn is on its start row, it can have different behavior
        else:
            start_row = 1

        if self.is_empty(row + direction, file): # single ands double forward for pawn
            legal_moves.append((row + direction, file))
            if row == start_row and self.is_empty(row + 2 * direction, file):
                legal_moves.append((row + 2 * direction, file))
    
        if self.is_enemy(row + direction, file + 1, colour): # capture for pawn
            legal_moves.append((row + direction, file + 1))
        if self.is_enemy(row + direction, file - 1, colour):
            legal_moves.append((row + direction, file - 1))
        return legal_moves
    
    def get_Rook_moves(self, row, file, colour):
        legal_moves = []

        # Up direction
        for r in range(row - 1, -1, -1):   # if row = 7, for example, it would ignore the square its on and iterate to row 0 (inclusive, exclusive)
            if self.is_empty(r, file):
                legal_moves.append((r, file))
            elif self.is_enemy(r, file, colour):
                legal_moves.append((r, file))
                break
            else:
                break

        # down direction
        for r in range(row + 1, 8):    # if row = 0, for example, it would ignore the square its on and iterate to row 7 (inclusive, exclusive)
            if self.is_empty(r, file):
                legal_moves.append((r, file))
            elif self.is_enemy(r, file, colour):
                legal_moves.append((r, file))
                break
            else:
                break
        
        # Left direction
        for f in range(file - 1, -1, -1):   # if file = 7, for example, it would ignore the square its on and iterate to file 0 (inclusive, exclusive)
            if self.is_empty(row, f):
                legal_moves.append((row, f))
            elif self.is_enemy(row, f, colour):
                legal_moves.append((row, f))  # Capture
                break
            else:
                break  # Stop if a piece blocks the way                    
        
        # Right direction
        for f in range(file + 1, 8):    # if file = 0, for example, it would ignore the square its on and iterate to file 7 (inclusive, exclusive)
            if self.is_empty(row, f):
                legal_moves.append((row, f))
            elif self.is_enemy(row, f, colour):
                legal_moves.append((row, f))  # Capture
                break
            else:
                break  # Stop if a piece blocks the way            

        return legal_moves
    
    def get_Bishop_moves(self, row, file, colour):
        legal_moves = []
        # This is uses the same logic the rook uses, but a while loop is needed insted.
        # Because a nested for loop would iterate through all the file positions,
        # then iterate a single time in the row position (for row..:
        #                                                   for file..:)
        # As a result, generated a grid like pattern for viable moves.
        # In a while loop, you can iterate through rows and files simultaneously.
        # So you can generate the diagonal move set. 
         
        # Top left diagonal
        r = row - 1
        f = file - 1
        while r >= 0 and f >= 0:
            if self.is_empty(r, f):
                legal_moves.append((r, f))
            elif self.is_enemy(r, f, colour):
                legal_moves.append((r, f))
                break
            else:
                break
            r -= 1
            f -= 1
        
        
        # Bottom right diagonal
        r = row + 1
        f = file + 1
        while r < 8 and f < 8:
            if self.is_empty(r, f):
                legal_moves.append((r, f))
            elif self.is_enemy(r, f, colour):
                legal_moves.append((r, f))
                break
            else:
                break
            r += 1
            f += 1
        
        # Top right diagonal
        r = row - 1
        f = file + 1
        while r >= 0 and f < 8:
            if self.is_empty(r, f):
                legal_moves.append((r, f))
            elif self.is_enemy(r, f, colour):
                legal_moves.append((r, f))
                break
            else:
                break
            r -= 1
            f += 1
        
        # Bottom left diagonal
        r = row + 1
        f = file - 1
        while r < 8 and f >= 0:
            if self.is_empty(r, f):
                legal_moves.append((r, f))
            elif self.is_enemy(r, f, colour):
                legal_moves.append((r, f))
                break
            else:
                break
            r += 1
            f -= 1        
        
        return legal_moves
    
    def get_Queen_moves(self, row, file, colour):
        # Peak Pattern spotting:
        bishop_moves = self.get_Bishop_moves(row, file, colour)
        rook_moves = self.get_Rook_moves(row, file, colour)
    
        legal_moves = bishop_moves + rook_moves

        return legal_moves    
    
    def get_King_moves(self, row, file, colour):
        legal_moves = []
        # All the possible king moves
        directions = [
        (-1, 0), (1, 0),                    # vertical (up, down)
        (0, -1), (0, 1),                    # horizontal (left, right)
        (-1, -1), (-1, 1), (1, -1), (1, 1)  # diagonal (top-left, top-right, bottom-left, bottom-right)
        ]

        for d_row, d_file in directions:
            r = row + d_row
            f = file + d_file
            if 0 <= r < 8 and 0 <= f < 8:  # Ensure within board bounds
                if self.is_empty(r, f) or self.is_enemy(r, f, colour):
                    legal_moves.append((r, f))
        return legal_moves
    
    def get_Knight_moves(self, row, file, colour):
        legal_moves = []
        # All the possible moves a knight can make
        directions = [     
        (2, 1), (2, -1),    # In hindsight, I think I could have used this method               
        (-2, 1), (-2, -1),  # for all the pieces.... It is much simpler.                 
        (1, -2), (-1, -2),  #(maybe except the pawn, but the point still stands)
        (1, 2), (-1, 2)  
        ]
        
        for d_row, d_file in directions:
            r = row + d_row
            f = file + d_file
            if 0 <= r < 8 and 0 <= f < 8:  # Ensure within board bounds
                if self.is_empty(r, f) or self.is_enemy(r, f, colour):
                    legal_moves.append((r, f))
        return legal_moves
    
    def get_legal_moves(self, piece_type, colour, position):
        row, file = position // 8, position % 8    # this works, pick a number from 0 - 720 to test
        global moves
        moves = []
        if piece_type == Piece.Pawn:
            moves = self.get_Pawn_moves(row, file, colour)
        if piece_type == Piece.Rook:
            moves = self.get_Rook_moves(row, file, colour)
        if piece_type == Piece.Knight:
            moves = self.get_Knight_moves(row, file, colour)
        if piece_type == Piece.Bishop:
            moves = self.get_Bishop_moves(row, file, colour)
        if piece_type == Piece.Queen:
            moves = self.get_Queen_moves(row, file, colour)
        if piece_type == Piece.King:
            moves = self.get_King_moves(row, file, colour)
        
        return moves
    
    def is_empty(self, row, file):
        index = row * 8 + file
        return 0 <= row < 8 and 0 <= file < 8 and self.Square[index] == Piece.Empty

    def is_enemy(self, row, file, colour):
        index = row * 8 + file
        if 0 <= row < 8 and 0 <= file < 8:      # Ensure piece is within board boundaries (boundary check)
            piece = self.Square[index]          # refers to the piece at that index of the board
            return piece != Piece.Empty and (piece & Piece.White) != (colour & Piece.White) # check if square is empty and if the colours don't match
        return False                            # ^ here we use the bitwise AND operator (&) so we can compare specific attributes with varibles.
                                                # This is because to assign those attributes, we used the bitwiise OR operator (|) meaning the attributes of the pieces are stored in binary.
                                                # Therefore, this the second argument for that And gate asks, if the colour of the piece is Not equal to white.
    
    def draw_pieces(self, screen, dragging_piece=None, dragging_pos=(0, 0)):
        for index, piece in enumerate(self.Square):
            if piece != Piece.Empty and piece != dragging_piece:  #checks if a piece is to be rendered.
                piece_image = self.piece_images.get(piece)
                if piece_image:
                    row = index // 8            #do the math with an arbritary index
                    col = index % 8             #if you think this doesnt work
                    screen.blit(piece_image, (col * single_square_size, row * single_square_size))
        if dragging_piece:
            screen.blit(selected_piece_img, dragging_pos)

def Create_graphical_board():
    for file in range (8):
        for row in range (8):
            isLightsquare = (file + row) % 2 != 0
            if isLightsquare:
                square_colour = peach
            else:
                square_colour = chocolate
            pygame.draw.rect(screen, square_colour, (single_square_size * file, single_square_size * row , single_square_size , single_square_size ))
            
chess_board = Board()  # Initialised the board class so it can be called throughout the program

selected_piece = None
dragging = False
offset_x = 0
offset_y = 0
original_square = None
load_position_from_fen(chess_board, "RNBQKBNR/PPPPPPPP/8/8/8/8/pppppppp/rnbqkbnr b KQkq - 0 1") # that is a fen string

while running:
    
    mouse_x, mouse_y = pygame.mouse.get_pos() # tracks mouse position
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos         # evnt.pos gives out a tuple of x, y
            file = mouse_x // single_square_size # floor div gives the file/row it's on
            row = mouse_y // single_square_size
            index = row * 8 + file               # gives its index which ranges 0 - 63

            if chess_board.Square[index] != Piece.Empty:
                selected_piece = chess_board.Square[index]
                selected_piece_img = chess_board.piece_images.get(selected_piece)
                dragging = True
                offset_x = mouse_x - (file * single_square_size) # substracts the orignal mouse pos ranging 0 - 720 from the new one also 0 - 720
                offset_y = mouse_y - (row * single_square_size)
                original_square = index # records the original square using the index
                
                selected_piece = chess_board.Square[index]  # The selected piece is the piece at the original square on the board
                if (selected_piece & Piece.White):
                    piece_color = Piece.White & selected_piece
                else:
                    piece_color = Piece.Black
                
                selected_piece_type = selected_piece & 0b111  # Calculate legal moves  # Get the type by isolating last 3 bits
                legal_moves = chess_board.get_legal_moves(selected_piece_type, piece_color, original_square)
                chess_board.Square[original_square] = Piece.Empty # when a move is being chosen, clears the og square

                
                
        elif event.type == pygame.MOUSEMOTION and dragging:
            mouse_x, mouse_y = event.pos # if dragging, update the position
            
                
        elif event.type == pygame.MOUSEBUTTONUP and dragging:
            new_file = mouse_x // single_square_size # records the file/row of the updated pos
            new_row = mouse_y // single_square_size
            new_index = new_row * 8 + new_file
                            
            if (new_row, new_file) in moves:
                chess_board.Square[new_index] = selected_piece     # Move piece
            else:
                # Handle invalid moves  snaps back to original position
                chess_board.Square[original_square] = selected_piece

            selected_piece = None # resets everything to the original state to cancel the dragging
            dragging = False
            original_square = None

    Create_graphical_board()
    chess_board.draw_pieces(screen, selected_piece_img if dragging else None, (mouse_x - offset_x, mouse_y - offset_y) if dragging else (0, 0)) # essentially just draws selected pieces if they are being dragged, else don't draw pieces that are not being dragged.

    if selected_piece:
        for move in legal_moves:
            # Calculate the row and file from the move index
            row, file = move

            # Calculate the center position for the circle
            center_x = (file * single_square_size) + (single_square_size // 2)
            center_y = (row * single_square_size) + (single_square_size // 2)
    
            # Draws the circle
            pygame.draw.circle(screen, highlight_colour, (center_x, center_y), single_square_size // 6)
                

    pygame.display.flip()
    clock.tick(60)
pygame.quit()