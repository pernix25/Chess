import pygame
from abc import ABC, abstractmethod
from enum import Enum

class Piece(ABC):
    def __init__(self, row, col, color) -> None:
        self.row = row
        self.col = col
        self.x = (self.col * 80) + 10
        self.y = (self.row * 80) + 8
        self.color = color
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
    def collidepoint(self, mouse_pos) -> bool:
        if (mouse_pos[0] >= self.rect[0] and mouse_pos[0] <= (self.rect[0] + self.rect[2])) and mouse_pos[1] >= self.rect[1] and mouse_pos[1] <= (self.rect[1] + self.rect[3]):
            return True
        else:
            return False
    def move(self, row, col):
        self.row = row
        self.col = col
        self.x = (self.col * 80) + 10
        self.y = (self.row * 80) + 8
        if isinstance(self, Pawn) or isinstance(self, King) or isinstance(self, Rook):
            self.has_moved = True
    @abstractmethod
    def get_valid_moves(self, board):
        pass
    @abstractmethod
    def get_attacking_moves(self, board):
        pass

class Pawn(Piece):
    def __init__(self, row, col, color) -> None:
        super().__init__(row, col, color)
        self.has_moved = False
        if self.color == 'w':
            self.image = pygame.image.load("images/wht_pawn.png").convert_alpha()
        elif self.color == 'b':
            self.image = pygame.image.load("images/blk_pawn.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x,self.y)
        self.mask = pygame.mask.from_surface(self.image)
    
    def get_valid_moves(self, board) -> list:
        moves = []

        #checks for captures and updates them to moves
        if self.color == 'w':
            #checks for valid tiles (white pieces)
            if self.col == 0:
                r_tile = board.board[self.row - 1][self.col + 1]
                l_tile = 0
            elif self.col == 7:
                l_tile = board.board[self.row - 1][self.col - 1]
                r_tile = 0
            else:
                r_tile = board.board[self.row - 1][self.col + 1]
                l_tile = board.board[self.row - 1][self.col - 1]
            
            if r_tile != 0 and r_tile.color != self.color:
                moves.append((self.row - 1, self.col + 1))
            if l_tile != 0 and l_tile.color != self.color:
                moves.append((self.row - 1, self.col - 1))    
        else:
            #checks for valid tiles (black piece)
            if self.col == 0: 
                r_tile = board.board[self.row + 1][self.col + 1]
                l_tile = 0
            elif self.col == 7:
                l_tile = board.board[self.row + 1][self.col - 1]
                r_tile = 0
            else:
                r_tile = board.board[self.row + 1][self.col + 1]
                l_tile = board.board[self.row + 1][self.col - 1]

            if r_tile != 0 and r_tile.color != self.color:
                moves.append((self.row + 1, self.col + 1))
            if l_tile != 0 and l_tile.color != self.color:
                moves.append((self.row + 1, self.col - 1))

        #if pawn has not moved it updates moves with the farther pawn push move
        if not self.has_moved:
            if self.color == 'w':
                if board.board[self.row - 1][self.col] == 0 and board.board[self.row - 2][self.col] == 0:
                    moves.append((self.row - 2, self.col))
            else:
                if board.board[self.row + 1][self.col] == 0 and board.board[self.row + 2][self.col] == 0:
                    moves.append((self.row + 2, self.col))
        
        #updates moves with basic pawn push move
        if self.color == 'w':
            if board.board[self.row - 1][self.col] == 0:
                    moves.append((self.row - 1, self.col))
        else:
            if board.board[self.row + 1][self.col] == 0:
                    moves.append((self.row + 1, self.col))
        return moves
    
    def get_attacking_moves(self, board) -> list:
        moves = []
        if self.color == 'w':
            #checks for valid tiles (white pieces)
            if self.col == 0:
                moves.append((self.row - 1, self.col + 1))
            elif self.col == 7:
                moves.append((self.row - 1, self.col - 1))
            else:
                moves.append((self.row - 1, self.col + 1))
                moves.append((self.row - 1, self.col - 1))
        else:
            #checks for valid tiles (black piece)
            if self.col == 0: 
                moves.append((self.row + 1, self.col + 1))
            elif self.col == 7:
                moves.append((self.row + 1, self.col - 1))
            else:
                moves.append((self.row + 1, self.col + 1))
                moves.append((self.row + 1, self.col - 1))

        return moves

class Bishop(Piece):
    def __init__(self, row, col, color) -> None:
        super().__init__(row, col, color)
        if self.color == 'w':
            self.image = pygame.image.load("images/wht_bishop.png").convert_alpha()
        elif self.color == 'b':
            self.image = pygame.image.load("images/blk_bishop.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x,self.y)
        self.mask = pygame.mask.from_surface(self.image)
    
    def get_valid_moves(self, board) -> list:
        def traverse(x, y, x_int, y_int, lyst):
            x += x_int
            y += y_int
            while x > -1 and x < 8 and y > -1 and y < 8:
                tile = board.board[y][x]
                if tile == 0:
                    lyst.append((y, x))
                elif tile.color != self.color:
                    lyst.append((y, x))
                    return
                else:
                    return
                x += x_int
                y += y_int
        moves = []
        traverse(self.col, self.row, -1, -1, moves)
        traverse(self.col, self.row, 1, -1, moves)
        traverse(self.col, self.row, 1, 1, moves)
        traverse(self.col, self.row, -1, 1, moves)
        return moves
    
    def get_attacking_moves(self, board) -> list:
        def traverse(x, y, x_int, y_int, lyst):
            x += x_int
            y += y_int
            while x > -1 and x < 8 and y > -1 and y < 8:
                tile = board.board[y][x]
                if tile == 0:
                    lyst.append((y, x))
                elif tile.color != self.color:
                    lyst.append((y, x))
                    if not isinstance(tile, King):
                        return
                elif tile.color == self.color:
                    lyst.append((y, x))
                    return
                else:
                    return
                x += x_int
                y += y_int
        moves = []
        traverse(self.col, self.row, -1, -1, moves)
        traverse(self.col, self.row, 1, -1, moves)
        traverse(self.col, self.row, 1, 1, moves)
        traverse(self.col, self.row, -1, 1, moves)
        return moves

class Knight(Piece):
    def __init__(self, row, col, color) -> None:
        super().__init__(row, col, color)
        if self.color == 'w':
            self.image = pygame.image.load("images/wht_knight.png").convert_alpha()
        elif self.color == 'b':
            self.image = pygame.image.load("images/blk_knight.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x,self.y)
        self.mask = pygame.mask.from_surface(self.image)
    
    def get_valid_moves(self, board) -> list:
        def find_tiles(x, y, x_int, y_int, lyst):
            try:
                tile = board.board[y + y_int][x + x_int]
                if tile == 0 or tile.color != self.color:
                    lyst.append((y + y_int, x + x_int))
            except(IndexError):
                pass
            try:
                tile = board.board[y + y_int][x - x_int]
                if tile == 0 or tile.color != self.color:
                    lyst.append((y + y_int, x - x_int))
            except(IndexError):
                pass
            try:
                tile = board.board[y - y_int][x + x_int]
                if tile == 0 or tile.color != self.color:
                    lyst.append((y - y_int, x + x_int))
            except(IndexError):
                pass
            try:
                tile = board.board[y - y_int][x - x_int]
                if tile == 0 or tile.color != self.color:
                    lyst.append((y - y_int, x - x_int))
            except(IndexError):
                pass
            return

        moves = []
        find_tiles(self.col, self.row, 1, 2, moves)
        find_tiles(self.col, self.row, 2, 1, moves)
        return moves
    
    def get_attacking_moves(self, board) -> list:
        def find_tiles(x, y, x_int, y_int, lyst):
            try:
                board.board[y + y_int][x + x_int]
                lyst.append((y + y_int, x + x_int))
            except(IndexError):
                pass
            try:
                board.board[y + y_int][x - x_int]
                lyst.append((y + y_int, x - x_int))
            except(IndexError):
                pass
            try:
                board.board[y - y_int][x + x_int]
                lyst.append((y - y_int, x + x_int))
            except(IndexError):
                pass
            try:
                board.board[y - y_int][x - x_int]
                lyst.append((y - y_int, x - x_int))
            except(IndexError):
                pass
            return

        moves = []
        find_tiles(self.col, self.row, 1, 2, moves)
        find_tiles(self.col, self.row, 2, 1, moves)
        return moves

class Rook(Piece):
    def __init__(self, row, col, color) -> None:
        super().__init__(row, col, color)
        self.has_moved = False
        if self.color == 'w':
            self.image = pygame.image.load("images/wht_rook.png").convert_alpha()
        elif self.color == 'b':
            self.image = pygame.image.load("images/blk_rook.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x,self.y)
        self.mask = pygame.mask.from_surface(self.image)
    
    def get_valid_moves(self, board) -> list:
        def traverse(x, y, x_int, y_int, lyst):
            x += x_int
            y += y_int
            while x > -1 and x < 8 and y < 8 and y > -1:
                tile = board.board[y][x]
                if tile == 0:
                    lyst.append((y, x))
                elif tile.color != self.color:
                    lyst.append((y, x))
                    return
                else:
                    return
                x += x_int
                y += y_int
        moves = []
        traverse(self.col, self.row, 1, 0, moves)
        traverse(self.col, self.row, -1, 0, moves)
        traverse(self.col, self.row, 0, 1, moves)
        traverse(self.col, self.row, 0, -1, moves)
        return moves
    
    def get_attacking_moves(self, board) -> list:
        def traverse(x, y, x_int, y_int, lyst):
            x += x_int
            y += y_int
            while x > -1 and x < 8 and y < 8 and y > -1:
                tile = board.board[y][x]
                if tile == 0:
                    lyst.append((y, x))
                elif tile.color != self.color:
                    lyst.append((y, x))
                    if not isinstance(tile, King):
                        return
                elif tile.color == self.color:
                    lyst.append((y,x))
                    return
                else:
                    return
                x += x_int
                y += y_int
        moves = []
        traverse(self.col, self.row, 1, 0, moves)
        traverse(self.col, self.row, -1, 0, moves)
        traverse(self.col, self.row, 0, 1, moves)
        traverse(self.col, self.row, 0, -1, moves)
        return moves

class King(Piece):
    def __init__(self, row, col, color) -> None:
        super().__init__(row, col, color)
        self.has_moved = False
        if self.color == 'w':
            self.image = pygame.image.load("images/wht_king.png").convert_alpha()
        elif self.color == 'b':
            self.image = pygame.image.load("images/blk_king.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x,self.y)
        self.mask = pygame.mask.from_surface(self.image)
    
    def get_valid_moves(self, board, opp_moves) -> list:
        def check(x, y, x_int, y_int, lyst):
            try:
                if y + y_int < 0 or x + x_int < 0 or y + y_int > 7 or x + x_int > 7:
                    raise IndexError
                tile = board.board[y + y_int][x + x_int]
                if tile == 0 and (y + y_int, x + x_int) not in opposite_moves:
                    lyst.append((y + y_int, x + x_int))
                elif tile != 0 and tile.color != self.color and (y + y_int, x + x_int) not in opposite_moves:
                    lyst.append((y + y_int, x + x_int))
                return
            except(IndexError):
                return
        moves = []

        opposite_moves = []
        for lyst in opp_moves.values():
            for move in lyst:
                opposite_moves.append(move)

        check(self.col, self.row, 1, 0, moves)
        check(self.col, self.row, 1, 1, moves)
        check(self.col, self.row, -1, 0, moves)
        check(self.col, self.row, -1, -1, moves)
        check(self.col, self.row, 0, 1, moves)
        check(self.col, self.row, 0, -1, moves)
        check(self.col, self.row, -1, 1, moves)
        check(self.col, self.row, 1, -1, moves)

        #checks for castles
        if self.color == 'w' and not self.has_moved:
            if board.board[7][5] == 0 and board.board[7][6] == 0 and isinstance(board.board[7][7], Rook) and not board.board[7][7].has_moved and (self.row, self.col) not in opposite_moves and (7,6) not in opposite_moves and (7,7) not in opposite_moves:
                moves.append((7,6))
            if board.board[7][1] == 0 and board.board[7][2] == 0 and board.board[7][3] == 0 and isinstance(board.board[7][0], Rook) and not board.board[7][0].has_moved and (self.row, self.col) not in opposite_moves and (7,2) not in opposite_moves and (7,0) not in opposite_moves:
                moves.append((7,2))
        elif self.color == 'b':
            if board.board[0][5] == 0 and board.board[0][6] == 0 and isinstance(board.board[0][7], Rook) and not board.board[0][7].has_moved and (self.row, self.col) not in opposite_moves and (0,6) not in opposite_moves and (0,7) not in opposite_moves:
                moves.append((0,6))
            if board.board[0][1] == 0 and board.board[0][2] == 0 and board.board[0][3] == 0 and isinstance(board.board[0][0], Rook) and not board.board[0][0].has_moved and (self.row, self.col) not in opposite_moves and (0,2) not in opposite_moves and (0,0) not in opposite_moves:
                moves.append((0,2))

        return moves
    
    def get_attacking_moves(self) -> list:
        def check(x, y, x_int, y_int, lyst):
            try:
                if y + y_int < 0 or x + x_int < 0 or y + y_int > 7 or x + x_int > 7:
                    raise IndexError
                else:
                    lyst.append((y + y_int, x + x_int))
                return
            except(IndexError):
                return
        moves = []

        check(self.col, self.row, 1, 0, moves)
        check(self.col, self.row, 1, 1, moves)
        check(self.col, self.row, -1, 0, moves)
        check(self.col, self.row, -1, -1, moves)
        check(self.col, self.row, 0, 1, moves)
        check(self.col, self.row, 0, -1, moves)
        check(self.col, self.row, -1, 1, moves)
        check(self.col, self.row, 1, -1, moves)

        return moves

class Queen(Piece):
    def __init__(self, row, col, color) -> None:
        super().__init__(row, col, color)
        if self.color == 'w':
            self.image = pygame.image.load("images/wht_queen.png").convert_alpha()
        elif self.color == 'b':
            self.image = pygame.image.load("images/blk_queen.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x,self.y)
        self.mask = pygame.mask.from_surface(self.image)

    def get_valid_moves(self, board) -> list:
        def bishop_traverse(x, y, x_int, y_int, lyst):
            x += x_int
            y += y_int
            while x > -1 and x < 8 and y > -1 and y < 8:
                tile = board.board[y][x]
                if tile == 0:
                    lyst.append((y, x))
                elif tile.color != self.color:
                    lyst.append((y, x))
                    return
                else:
                    return
                x += x_int
                y += y_int
        def rook_traverse(x, y, x_int, y_int, lyst):
            x += x_int
            y += y_int
            while x > -1 and x < 8 and y < 8 and y > -1:
                tile = board.board[y][x]
                if tile == 0:
                    lyst.append((y, x))
                elif tile.color != self.color:
                    lyst.append((y, x))
                    return
                else:
                    return
                x += x_int
                y += y_int
        moves = []
        bishop_traverse(self.col, self.row, -1, -1, moves)
        bishop_traverse(self.col, self.row, 1, -1, moves)
        bishop_traverse(self.col, self.row, 1, 1, moves)
        bishop_traverse(self.col, self.row, -1, 1, moves)
        rook_traverse(self.col, self.row, 1, 0, moves)
        rook_traverse(self.col, self.row, -1, 0, moves)
        rook_traverse(self.col, self.row, 0, 1, moves)
        rook_traverse(self.col, self.row, 0, -1, moves)
        return moves
    
    def get_attacking_moves(self, board) -> list:
        def bishop_traverse(x, y, x_int, y_int, lyst):
            x += x_int
            y += y_int
            while x > -1 and x < 8 and y > -1 and y < 8:
                tile = board.board[y][x]
                if tile == 0:
                    lyst.append((y, x))
                elif tile.color != self.color:
                    lyst.append((y, x))
                    if not isinstance(tile, King):
                        return
                elif tile.color == self.color:
                    lyst.append((y, x))
                    return
                else:
                    return
                x += x_int
                y += y_int
        def rook_traverse(x, y, x_int, y_int, lyst):
            x += x_int
            y += y_int
            while x > -1 and x < 8 and y < 8 and y > -1:
                tile = board.board[y][x]
                if tile == 0:
                    lyst.append((y, x))
                elif tile.color != self.color:
                    lyst.append((y, x))
                    if not isinstance(tile, King):
                        return
                elif tile.color == self.color:
                    lyst.append((y, x))
                    return
                else:
                    return
                x += x_int
                y += y_int
        moves = []
        bishop_traverse(self.col, self.row, -1, -1, moves)
        bishop_traverse(self.col, self.row, 1, -1, moves)
        bishop_traverse(self.col, self.row, 1, 1, moves)
        bishop_traverse(self.col, self.row, -1, 1, moves)
        rook_traverse(self.col, self.row, 1, 0, moves)
        rook_traverse(self.col, self.row, -1, 0, moves)
        rook_traverse(self.col, self.row, 0, 1, moves)
        rook_traverse(self.col, self.row, 0, -1, moves)
        return moves
