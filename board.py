import pygame
from pieces import *

class Board:
    def __init__(self) -> None:
        self.w_king = King(7, 4, 'w')
        self.b_king = King(0, 4, 'b')
        self.pawn_jump = False
        self.create_board()

    def draw_tiles(self, surface):
        surface.fill((255,255,255))
        for row in range(8):
            for col in range((row + 1) % 2, 8, 2):
                pygame.draw.rect(surface, (0, 255, 0), (row * 80, col * 80, 80, 80))

    def create_board(self):
        self.board = [[Rook(0, 0, 'b'),Knight(0, 1, 'b'),Bishop(0, 2, 'b'),Queen(0, 3, 'b'),self.b_king,Bishop(0, 5, 'b'),Knight(0, 6, 'b'),Rook(0, 7, 'b')],
                      [Pawn(1, 0, 'b'),Pawn(1, 1, 'b'),Pawn(1, 2, 'b'),Pawn(1, 3, 'b'),Pawn(1, 4, 'b'),Pawn(1 , 5, 'b'),Pawn(1, 6, 'b'),Pawn(1, 7, 'b')],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [Pawn(6, 0, 'w'),Pawn(6, 1, 'w'),Pawn(6, 2, 'w'),Pawn(6, 3, 'w'),Pawn(6, 4, 'w'),Pawn(6, 5, 'w'),Pawn(6, 6, 'w'),Pawn(6, 7, 'w')],
                      [Rook(7, 0, 'w'),Knight(7, 1, 'w'),Bishop(7, 2, 'w'),Queen(7, 3, 'w'),self.w_king,Bishop(7, 5, 'w'),Knight(7, 6, 'w'),Rook(7, 7, 'w')]
                     ]

    def draw(self, surface):
        self.draw_tiles(surface)
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(surface)
    
    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
    
    def get_piece(self, row, col):
        return self.board[row][col]
