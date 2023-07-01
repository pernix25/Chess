import pygame
from pieces import *
from game import Game

pygame.init()

#screen details
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chess")

#helper functions
def get_row_col(pos):
    x, y = pos
    row = y // 80
    col = x // 80
    return row, col

def main():
    game = Game(screen)

    #game loop
    running = True
    while running:
        
        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col(pos)
                    game.select(row, col)
        
        game.update()
        if game.checkmate:
            pygame.display.set_caption("Checkmate!")

if __name__ == "__main__":
    main()