import pygame 
 
pygame.init()
 
width = 400
height = 400
screen = pygame.display.set_mode((width, height))
 
white = (237, 232, 208)
black = (85, 43, 0)
 
rows = 8
columns = 8
square = width // columns

def draw_board():
    for i in range(rows):
        for j in range(columns):
            if (i + j) % 2 == 0:
                colour = white
            else:
                colour = black
            x = j * square
            y = i * square
            width = square
            height = square
            pygame.draw.rect(screen, colour, (x, y, width, height))
 
 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            running == True
 
 
    draw_board()
    pygame.display.flip()