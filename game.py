import pygame
from board import Board
from pieces import *

class Game:
    def __init__(self, surface) -> None:
        self.selected = None
        self.board = Board()
        self.turn = 'w'
        self.valid_moves = []
        self.surface = surface
        self.white_moves = {}
        self.black_moves = {}
        self.checked = False
        self.checkmate = False
        self.w_king = self.board.w_king
        self.b_king = self.board.b_king

    def update(self):
        self.board.draw(self.surface)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def reset(self):
        self.selected = None
        self.board = Board()
        self.turn = 'w'
        self.valid_moves = []
        self.white_moves = {}
        self.black_moves = {}
        self.checked = False
        self.checkmate = False
        self.w_king = self.board.w_king
        self.b_king = self.board.b_king

    def select(self, row, col):
        if self.selected:
            result = self.move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        piece = self.board.get_piece(row, col)
        if self.checked:
            self.selected = piece
            self.valid_moves = self.get_checked_moves()
            if self.valid_moves == []:
                self.checkmate = True
            return True
        elif piece != 0 and piece.color == self.turn:
            self.selected = piece
            if isinstance(piece, King) and piece.color == 'w':
                self.valid_moves = piece.get_valid_moves(self.board, self.black_moves)
            elif isinstance(piece, King) and piece.color == 'b':
                self.valid_moves = piece.get_valid_moves(self.board, self.white_moves)
            else:
                self.valid_moves = piece.get_valid_moves(self.board)
            return True
        return False
    
    def move(self, row, col):
        piece = self.board.get_piece(row, col)
        #handles all pawn moves (promotions)
        if isinstance(self.selected, Pawn):
            if self.selected.color == 'w':
                if self.selected.row == 0:
                    row = self.selected.row
                    col = self.selected.col
                    self.remove(self.selected)
                    self.board.board[row][col] = Queen(row, col, 'w')
                    self.change_turn()
                    self.get_all_avalible_moves()
                    self.in_check()
                else:
                    if self.selected and piece == 0 and (row, col) in self.valid_moves and (row, col) in self.selected.get_valid_moves(self.board):
                        self.board.move(self.selected, row, col)            
                        self.change_turn()
                        self.get_all_avalible_moves()
                        self.in_check()
                    elif self.selected and piece != 0 and (row, col) in self.valid_moves and (row, col) in self.selected.get_valid_moves(self.board):
                        self.remove(piece)
                        self.board.move(self.selected, row, col)
                        self.change_turn()
                        self.get_all_avalible_moves()
                        self.in_check()
                    else:
                        return False
            else:
                if self.selected.row == 7:
                    row = self.selected.row
                    col = self.selected.col
                    self.remove(self.selected)
                    self.board.board[row][col] = Queen(row, col, 'b')
                    self.change_turn()
                    self.get_all_avalible_moves()
                    self.in_check()
                else:
                    if self.selected and piece == 0 and (row, col) in self.valid_moves and (row, col) in self.selected.get_valid_moves(self.board):
                        self.board.move(self.selected, row, col)            
                        self.change_turn()
                        self.get_all_avalible_moves()
                        self.in_check()
                    elif self.selected and piece != 0 and (row, col) in self.valid_moves and (row, col) in self.selected.get_valid_moves(self.board):
                        self.remove(piece)
                        self.board.move(self.selected, row, col)
                        self.change_turn()
                        self.get_all_avalible_moves()
                        self.in_check()
                    else:
                        return False
        #handles all king moves (castles)
        elif isinstance(self.selected, King):
            if self.selected.color == 'w':
                if not self.selected.has_moved:
                    if row == 7 and (col == 6 or col == 2) and (row, col) in self.valid_moves:
                        if col == 6:
                            self.board.move(self.selected, 7, 6)
                            self.board.move(self.board.board[7][7], 7, 5)
                            self.change_turn()
                            self.get_all_avalible_moves()
                        else:
                            self.board.move(self.selected, 7, 2)
                            self.board.move(self.board.board[7][0], 7, 3)
                            self.change_turn()
                            self.get_all_avalible_moves()
                    else:
                        if self.selected and (piece == 0 or piece.color != self.turn) and (row, col) in self.valid_moves:
                            if piece != 0:
                                self.remove(piece)
                                self.board.move(self.selected, row, col)            
                                self.change_turn()
                                self.get_all_avalible_moves()
                            else:
                                self.board.move(self.selected, row, col)            
                                self.change_turn()
                                self.get_all_avalible_moves()
                else:
                    if self.selected and piece == 0 and (row, col) in self.valid_moves and (row, col) in self.selected.get_valid_moves(self.board, self.black_moves):
                        self.board.move(self.selected, row, col)            
                        self.change_turn()
                        self.get_all_avalible_moves()
                        self.in_check()
                    elif self.selected and piece != 0 and (row, col) in self.valid_moves and (row, col) in self.selected.get_valid_moves(self.board, self.black_moves):
                        self.remove(piece)
                        self.board.move(self.selected, row, col)
                        self.change_turn()
                        self.get_all_avalible_moves()
                        self.in_check()
                    else:
                        return False
            else:
                if not self.selected.has_moved:
                    if row == 0 and (col == 6 or col == 2) and (row, col) in self.valid_moves:
                        if row == 0 and (col == 6 or col == 2) and (row, col) in self.valid_moves:
                            if col == 6:
                                self.board.move(self.selected, 0, 6)
                                self.board.move(self.board.board[0][7], 0, 5)
                                self.change_turn()
                                self.get_all_avalible_moves()
                            else:
                                self.board.move(self.selected, 0, 2)
                                self.board.move(self.board.board[0][0], 0, 3)
                                self.change_turn()
                                self.get_all_avalible_moves()
                    else:
                        if self.selected and (piece == 0 or piece.color != self.turn) and (row, col) in self.valid_moves:
                            if piece != 0:
                                self.remove(piece)
                                self.board.move(self.selected, row, col)            
                                self.change_turn()
                                self.get_all_avalible_moves()
                            else:
                                self.board.move(self.selected, row, col)            
                                self.change_turn()
                                self.get_all_avalible_moves()
                else:
                    if self.selected and piece == 0 and (row, col) in self.valid_moves and (row, col) in self.selected.get_valid_moves(self.board, self.white_moves):
                        self.board.move(self.selected, row, col)            
                        self.change_turn()
                        self.get_all_avalible_moves()
                        self.in_check()
                    elif self.selected and piece != 0 and (row, col) in self.valid_moves and (row, col) in self.selected.get_valid_moves(self.board, self.white_moves):
                        self.remove(piece)
                        self.board.move(self.selected, row, col)
                        self.change_turn()
                        self.get_all_avalible_moves()
                        self.in_check()
                    else:
                        return False
        #handles all other moves
        elif self.selected and piece == 0 and (row, col) in self.valid_moves and (row, col) in self.selected.get_valid_moves(self.board) and self.selected.color == self.turn:
            self.board.move(self.selected, row, col)            
            self.change_turn()
            self.get_all_avalible_moves()
            self.in_check()
        elif self.selected and piece != 0 and (row, col) in self.valid_moves and (row, col) in self.selected.get_valid_moves(self.board) and self.selected.color == self.turn:
            self.remove(piece)
            self.board.move(self.selected, row, col)
            self.change_turn()
            self.get_all_avalible_moves()
            self.in_check()
        else:
            return False
        return True
    
    def change_turn(self):
        self.valid_moves = []
        if self.turn == 'w':
            self.turn = 'b'
            self.checked = False
        else:
            self.turn = 'w'
            self.checked = False
    
    def draw_valid_moves(self, moves):
        for move in moves:
            row = move[0]
            col = move[1]
            pygame.draw.circle(self.surface, (0,0,255), (col * 80 + 40, row * 80 + 40), 10)
    
    def remove(self, piece):
        self.board.board[piece.row][piece.col] = 0
    
    def get_all_avalible_moves(self):
        self.white_moves = {}
        self.black_moves = {}

        def find_all_white_moves():
            for row in self.board.board:
                for piece in row:
                    if piece != 0 and piece.color == 'w':
                        if isinstance(piece, King):
                            continue
                        else:
                            moves = piece.get_attacking_moves(self.board)
                            self.white_moves.update({piece: moves})
        def find_all_black_moves():
            for row in self.board.board:
                for piece in row:
                    if piece != 0 and piece.color == 'b':
                        if isinstance(piece, King):
                            continue
                        else:
                            moves = piece.get_attacking_moves(self.board)
                            self.black_moves.update({piece: moves})
        
        find_all_white_moves()
        find_all_black_moves()
        if self.turn == 'b':
            moves = self.w_king.get_attacking_moves()
            self.white_moves.update({self.w_king: moves})
            moves = self.b_king.get_valid_moves(self.board, self.white_moves)
            self.black_moves.update({self.b_king: moves})
        else:
            moves = self.b_king.get_attacking_moves()
            self.black_moves.update({self.b_king: moves})
            moves = self.w_king.get_valid_moves(self.board, self.black_moves)
            self.white_moves.update({self.w_king: moves})

    def in_check(self):
        if self.turn == 'w':
            row = self.w_king.row
            col = self.w_king.col
            for lyst in self.black_moves.values():
                for move in lyst:
                    if (row, col) == move:
                        self.checked = True
        else:
            row = self.b_king.row
            col = self.b_king.col
            for lyst in self.white_moves.values():
                for move in lyst:
                    if (row, col) == move:
                        self.checked = True
    
    def get_checked_moves(self):
        pieces_checking_king = {}
        if self.turn == 'w':
            king_location = (self.w_king.row, self.w_king.col)
            for piece in self.black_moves.keys():
                black_moves = self.black_moves[piece]
                if king_location in black_moves:
                    if isinstance(piece, Pawn):
                        live_tiles = [(piece.row, piece.col)]
                        pieces_checking_king.update({piece: live_tiles})
                    elif isinstance(piece, Knight):
                        live_tiles = [(piece.row, piece.col)]
                        pieces_checking_king.update({piece: live_tiles})
                    elif isinstance(piece, Bishop):
                        bishop_location = (piece.row, piece.col)
                        live_tiles = [bishop_location]
                        if bishop_location[0] < king_location[0] and bishop_location[1] < king_location[1]:
                            interval = 1
                            while bishop_location[0] + interval < king_location[0] and bishop_location[1] + interval < king_location[1]:
                                live_tiles.append((bishop_location[0] + interval, bishop_location[1] + interval))
                                interval += 1
                        elif bishop_location[0] < king_location[0] and bishop_location[1] > king_location[1]:
                            x_int = 1
                            y_int = 1
                            while bishop_location[0] + y_int < king_location[0] and bishop_location[1] - x_int > king_location[1]:
                                live_tiles.append((bishop_location[0] + y_int, bishop_location - x_int))
                                x_int += 1
                                y_int += 1
                        elif bishop_location[0] > king_location[0] and bishop_location[1] > king_location[1]:
                            interval = 1
                            while bishop_location[0] - interval > king_location[0] and bishop_location[1] - interval > king_location[1]:
                                live_tiles.append((bishop_location[0] - interval, bishop_location - interval))
                                interval += 1
                        elif bishop_location[0] > king_location[0] and bishop_location[1] < king_location[1]:
                            x_int = 1
                            y_int = 1
                            while bishop_location[0] - y_int > king_location[0] and bishop_location[1] + x_int < king_location[1]:
                                live_tiles.append((bishop_location[0] - y_int, bishop_location[1] + x_int))
                                x_int += 1
                                y_int += 1
                        pieces_checking_king.update({piece: live_tiles})
                    elif isinstance(piece, Rook):
                        rook_location = (piece.row, piece.col)
                        live_tiles = [rook_location]
                        if rook_location[0] == king_location[0]:
                            if rook_location[1] < king_location[1]:
                                interval = 1
                                while rook_location[1] + interval < king_location[1]:
                                    live_tiles.append((rook_location[0], rook_location[1] + interval))
                                    interval += 1
                            else:
                                interval = 1
                                while rook_location[1] - interval > king_location[1]:
                                    live_tiles.append((rook_location[0], rook_location[1] - interval))
                                    interval += 1
                        elif rook_location[1] == king_location[1]:
                            if rook_location[0] < king_location[0]:
                                interval = 1
                                while rook_location[0] + interval < king_location[0]:
                                    live_tiles.append((rook_location[0] + interval, rook_location[1]))
                                    interval += 1
                            else:
                                interval = 1
                                while rook_location[0] - interval > king_location[0]:
                                    live_tiles.append((rook_location[0] - interval, rook_location[1]))
                                    interval += 1
                        pieces_checking_king.update({piece: live_tiles})
                    elif isinstance(piece, Queen):
                        queen_location = (piece.row, piece.col)
                        live_tiles = [queen_location]
                        if queen_location[0] == king_location[0] or queen_location[1] == king_location[1]:
                            if queen_location[0] == king_location[0]:
                                if queen_location[1] < king_location[1]:
                                    interval = 1
                                    while queen_location[1] + interval < king_location[1]:
                                        live_tiles.append((queen_location[0], queen_location[1] + interval))
                                        interval += 1
                                else:
                                    interval = 1
                                    while queen_location[1] - interval > king_location[1]:
                                        live_tiles.append((queen_location[0], queen_location[1] - interval))
                                        interval += 1
                            elif queen_location[1] == king_location[1]:
                                if queen_location[0] < king_location[0]:
                                    interval = 1
                                    while queen_location[0] + interval < king_location[0]:
                                        live_tiles.append((queen_location[0] + interval, queen_location[1]))
                                        interval += 1
                                else:
                                    interval = 1
                                    while queen_location[0] - interval > king_location[0]:
                                        live_tiles.append((queen_location[0] - interval, queen_location[1]))
                                        interval += 1
                            pieces_checking_king.update({piece: live_tiles})
                        else:
                            if queen_location[0] < king_location[0] and queen_location[1] < king_location[1]:
                                interval = 1
                                while queen_location[0] + interval < king_location[0] and queen_location[1] + interval < king_location[1]:
                                    live_tiles.append((queen_location[0] + interval, queen_location[1] + interval))
                                    interval += 1
                            elif queen_location[0] < king_location[0] and queen_location[1] > king_location[1]:
                                x_int = 1
                                y_int = 1
                                while queen_location[0] + y_int < king_location[0] and queen_location[1] - x_int > king_location[1]:
                                    live_tiles.append((queen_location[0] + y_int, queen_location[1] - x_int))
                                    x_int += 1
                                    y_int += 1
                            elif queen_location[0] > king_location[0] and queen_location[1] > king_location[1]:
                                interval = 1
                                while queen_location[0] - interval > king_location[0] and queen_location[1] - interval > king_location[1]:
                                    live_tiles.append((queen_location[0] - interval, queen_location[1] - interval))
                                    interval += 1
                            elif queen_location[0] > king_location[0] and queen_location[1] < king_location[1]:
                                x_int = 1
                                y_int = 1
                                while queen_location[0] - y_int > king_location[0] and queen_location[1] + x_int < king_location[1]:
                                    live_tiles.append((queen_location[0] - y_int, queen_location[1] + x_int))
                                    x_int += 1
                                    y_int += 1
                            pieces_checking_king.update({piece: live_tiles})

            if len(pieces_checking_king.keys()) > 1:
                all_moves = self.w_king.get_valid_moves(self.board, self.black_moves)
            else:
                all_moves = self.w_king.get_valid_moves(self.board, self.black_moves)
                for row in self.board.board:
                    for piece in row:
                        if piece != 0 and piece.color == 'w' and not isinstance(piece, King):
                            valid_moves = piece.get_valid_moves(self.board)
                            for move in valid_moves:
                                if move in list(pieces_checking_king.values())[0]:
                                    all_moves.append(move)
        else:
            king_location = (self.b_king.row, self.b_king.col)
            for piece in self.white_moves.keys():
                white_moves = self.white_moves[piece]
                if king_location in white_moves:
                    if isinstance(piece, Pawn):
                        live_tiles = [(piece.row, piece.col)]
                        pieces_checking_king.update({piece: live_tiles})
                    elif isinstance(piece, Knight):
                        live_tiles = [(piece.row, piece.col)]
                        pieces_checking_king.update({piece: live_tiles})
                    elif isinstance(piece, Bishop):
                        bishop_location = (piece.row, piece.col)
                        live_tiles = [bishop_location]
                        if bishop_location[0] < king_location[0] and bishop_location[1] < king_location[1]:
                            interval = 1
                            while bishop_location[0] + interval < king_location[0] and bishop_location[1] + interval < king_location[1]:
                                live_tiles.append((bishop_location[0] + interval, bishop_location[1] + interval))
                                interval += 1
                        elif bishop_location[0] < king_location[0] and bishop_location[1] > king_location[1]:
                            x_int = 1
                            y_int = 1
                            while bishop_location[0] + y_int < king_location[0] and bishop_location[1] - x_int > king_location[1]:
                                live_tiles.append((bishop_location[0] + y_int, bishop_location - x_int))
                                x_int += 1
                                y_int += 1
                        elif bishop_location[0] > king_location[0] and bishop_location[1] > king_location[1]:
                            interval = 1
                            while bishop_location[0] - interval > king_location[0] and bishop_location[1] - interval > king_location[1]:
                                live_tiles.append((bishop_location[0] - interval, bishop_location - interval))
                                interval += 1
                        elif bishop_location[0] > king_location[0] and bishop_location[1] < king_location[1]:
                            x_int = 1
                            y_int = 1
                            while bishop_location[0] - y_int > king_location[0] and bishop_location[1] + x_int < king_location[1]:
                                live_tiles.append((bishop_location[0] - y_int, bishop_location[1] + x_int))
                                x_int += 1
                                y_int += 1
                        pieces_checking_king.update({piece: live_tiles})
                    elif isinstance(piece, Rook):
                        rook_location = (piece.row, piece.col)
                        live_tiles = [rook_location]
                        if rook_location[0] == king_location[0]:
                            if rook_location[1] < king_location[1]:
                                interval = 1
                                while rook_location[1] + interval < king_location[1]:
                                    live_tiles.append((rook_location[0], rook_location[1] + interval))
                                    interval += 1
                            else:
                                interval = 1
                                while rook_location[1] - interval > king_location[1]:
                                    live_tiles.append((rook_location[0], rook_location[1] - interval))
                                    interval += 1
                        elif rook_location[1] == king_location[1]:
                            if rook_location[0] < king_location[0]:
                                interval = 1
                                while rook_location[0] + interval < king_location[0]:
                                    live_tiles.append((rook_location[0] + interval, rook_location[1]))
                                    interval += 1
                            else:
                                interval = 1
                                while rook_location[0] - interval > king_location[0]:
                                    live_tiles.append((rook_location[0] - interval, rook_location[1]))
                                    interval += 1
                        pieces_checking_king.update({piece: live_tiles})
                    elif isinstance(piece, Queen):
                        queen_location = (piece.row, piece.col)
                        live_tiles = [queen_location]
                        if queen_location[0] == king_location[0] or queen_location[1] == king_location[1]:
                            if queen_location[0] == king_location[0]:
                                if queen_location[1] < king_location[1]:
                                    interval = 1
                                    while queen_location[1] + interval < king_location[1]:
                                        live_tiles.append((queen_location[0], queen_location[1] + interval))
                                        interval += 1
                                else:
                                    interval = 1
                                    while queen_location[1] - interval > king_location[1]:
                                        live_tiles.append((queen_location[0], queen_location[1] - interval))
                                        interval += 1
                            elif queen_location[1] == king_location[1]:
                                if queen_location[0] < king_location[0]:
                                    interval = 1
                                    while queen_location[0] + interval < king_location[0]:
                                        live_tiles.append((queen_location[0] + interval, queen_location[1]))
                                        interval += 1
                                else:
                                    interval = 1
                                    while queen_location[0] - interval > king_location[0]:
                                        live_tiles.append((queen_location[0] - interval, queen_location[1]))
                                        interval += 1
                            pieces_checking_king.update({piece: live_tiles})
                        else:
                            if queen_location[0] < king_location[0] and queen_location[1] < king_location[1]:
                                interval = 1
                                while queen_location[0] + interval < king_location[0] and queen_location[1] + interval < king_location[1]:
                                    live_tiles.append((queen_location[0] + interval, queen_location[1] + interval))
                                    interval += 1
                            elif queen_location[0] < king_location[0] and queen_location[1] > king_location[1]:
                                x_int = 1
                                y_int = 1
                                while queen_location[0] + y_int < king_location[0] and queen_location[1] - x_int > king_location[1]:
                                    live_tiles.append((queen_location[0] + y_int, queen_location - x_int))
                                    x_int += 1
                                    y_int += 1
                            elif queen_location[0] > king_location[0] and queen_location[1] > king_location[1]:
                                interval = 1
                                while queen_location[0] - interval > king_location[0] and queen_location[1] - interval > king_location[1]:
                                    live_tiles.append((queen_location[0] - interval, queen_location[1] - interval))
                                    interval += 1
                            elif queen_location[0] > king_location[0] and queen_location[1] < king_location[1]:
                                x_int = 1
                                y_int = 1
                                while queen_location[0] - y_int > king_location[0] and queen_location[1] + x_int < king_location[1]:
                                    live_tiles.append((queen_location[0] - y_int, queen_location[1] + x_int))
                                    x_int += 1
                                    y_int += 1
                            pieces_checking_king.update({piece: live_tiles})
            if len(pieces_checking_king.keys()) > 1:
                all_moves = self.b_king.get_valid_moves(self.board, self.white_moves)
            else:
                all_moves = self.b_king.get_valid_moves(self.board, self.white_moves)
                for row in self.board.board:
                    for piece in row:
                        if piece != 0 and piece.color == 'b' and not isinstance(piece, King):
                            valid_moves = piece.get_valid_moves(self.board)
                            for move in valid_moves:
                                if move in list(pieces_checking_king.values())[0]:
                                    all_moves.append(move)
        return all_moves
