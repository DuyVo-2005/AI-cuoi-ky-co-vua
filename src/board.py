from const import *
from square import Square
from piece import Piece, Pawn, Knight, Bishop, Rook, Queen, King
from move import Move
from sound import Sound

import copy
import os
import chess

class Board:
    def __init__(self, game, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.game = game        
        # Tạo mảng 8x8 để thêm các quân cờ sau đó
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        # Chứa thông tin của nước đi gần nhất
        self.last_move = None   
        # logic_board xử lý logic của game
        self.logic_board = chess.Board(fen)

        # Thêm các ô trống vào bảng
        self._create()
        # Thêm các quân cờ vào squares
        self.updata_squares()

        # Để xử lý nước đi thăng cấp
        self.is_on_pawn_promotion = False
        self.pre_pawn_promotion_move = None


    def move(self, move:Move, promotion_choosed=None):
        '''
            Hàm xử lý khi di chuyển quân cờ
            - Nhận một Move(Square(row, col), Square(row, col))
            - Cập nhật lại self.squares và self.logic_board
            - promotion_choosed có thể là: 'n', 'b', 'r', 'q' hoặc None nếu chưa chọn
        '''

        # Xử lý đặc biệt khi là nước đi thăng cấp của người chơi
        if self.check_player_promotion(move):
            # Nếu chưa chọn quân cờ để thăng cấp
            if not promotion_choosed:
                self.is_on_pawn_promotion = True
                self.pre_pawn_promotion_move = move
                return
            
            # Nếu đã chọn quân cờ để thăng cấp
            else:
                uci_move = move.to_uci() + promotion_choosed
                # sounds
                captured = self.squares[move.final.row][move.final.col].has_piece()
                self.game.play_sound(captured)
                # Cập nhật logic_board 
                self.logic_board.push_uci(uci_move)
                # Cập nhật squares
                if promotion_choosed == "q":
                    piece = self.squares[move.initial.row][move.initial.col].piece
                    self.squares[move.final.row][move.final.col].piece = Queen(piece.color)
                    self.squares[move.initial.row][move.initial.col].piece = None
                elif promotion_choosed == "r":
                    piece = self.squares[move.initial.row][move.initial.col].piece
                    self.squares[move.final.row][move.final.col].piece = Rook(piece.color)
                    self.squares[move.initial.row][move.initial.col].piece = None
                elif promotion_choosed == "b":
                    piece = self.squares[move.initial.row][move.initial.col].piece
                    self.squares[move.final.row][move.final.col].piece = Bishop(piece.color)
                    self.squares[move.initial.row][move.initial.col].piece = None
                elif promotion_choosed == "n":
                    piece = self.squares[move.initial.row][move.initial.col].piece
                    self.squares[move.final.row][move.final.col].piece = Knight(piece.color)
                    self.squares[move.initial.row][move.initial.col].piece = None

                self.is_on_pawn_promotion = False
                self.pre_pawn_promotion_move = None
                # Chuyển lượt
                self.game.next_turn()
                # Cập nhật last_move
                self.last_move = copy.deepcopy(move)
                    
                return

        # Xử lý đặc biệt khi là nước đi thăng cấp CỦA BOT
        if self.check_bot_promotion(move):
            '''Tự động thăng cấp thành quân Hậu'''

            uci_move = move.to_uci() + 'q'
            # sounds
            captured = self.squares[move.final.row][move.final.col].has_piece()
            self.game.play_sound(captured)
            # Cập nhật logic_board 
            self.logic_board.push_uci(uci_move)
            # Cập nhật squares
            piece = self.squares[move.initial.row][move.initial.col].piece
            self.squares[move.final.row][move.final.col].piece = Queen(piece.color)
            self.squares[move.initial.row][move.initial.col].piece = None
            # Chuyển lượt
            self.game.next_turn()
            # Cập nhật last_move
            self.last_move = copy.deepcopy(move)

            return

        uci_move = move.to_uci()

        # sounds
        captured = self.squares[move.final.row][move.final.col].has_piece()
        self.game.play_sound(captured)
        # Cập nhật logic_board 
        self.logic_board.push_uci(uci_move)
        # Cập nhật squares
        self.updata_squares()
        # Đổi lượt
        self.game.next_turn()
        # Cập nhật last_move
        self.last_move = copy.deepcopy(move)

    def valid_move(self, piece, move):
        '''
            Hàm check nước đi có hợp lệ
        '''
        return move in piece.moves

    def check_player_promotion(self, move):
        piece = self.squares[move.initial.row][move.initial.col].piece
        if (isinstance(piece, Pawn)) and (move.final.row == (0 if PLAYER_COLOR == "white" else 7)):
            # Phát âm thanh thăng cấp
            sound = Sound(
                os.path.join('assets/sounds/power-pawn.mp3'))
            sound.play()

            return True
        return False
    
    def check_bot_promotion(self, move):
        piece = self.squares[move.initial.row][move.initial.col].piece
        if (isinstance(piece, Pawn)) and (move.final.row == (7 if PLAYER_COLOR == "white" else 0)):
            # Phát âm thanh thăng cấp
            sound = Sound(
                os.path.join('assets/sounds/power-pawn.mp3'))
            sound.play()

            return True
        return False
    
    def promotion_to(self, piece, final, initial, name="Queen"):
        pro_piece = None
        if name == "Queen": 
            self.squares[final.row][final.col].piece = Queen(piece.color)
            pro_piece = 'q'
        elif name == "Rook": 
            self.squares[final.row][final.col].piece = Rook(piece.color)
            pro_piece = 'r'
        elif name == "Bishop": 
            self.squares[final.row][final.col].piece = Bishop(piece.color)
            pro_piece = 'b'
        elif name == "Knight": 
            self.squares[final.row][final.col].piece = Knight(piece.color)
            pro_piece = 'n'

    def calculate_moves(self, piece:Piece, row, col):
        # Tính toán toàn bộ các nước đi hợp lệ của 1 quân cờ
        logic_board = self.logic_board

        valid_moves = logic_board.legal_moves
        
        for chess_move in valid_moves:
            uci_move = chess_move.uci()
            index_move = Move.uci_to_index(uci_move)

            # Bỏ qua các nước đi không phải của quân cờ hiện tại
            if index_move[0][0] != row or index_move[0][1] != col:
                continue

            initial = Square(index_move[0][0], index_move[0][1])
            final = Square(index_move[1][0], index_move[1][1])
            prog_move = Move(initial, final)
            piece.add_move(prog_move)

    def updata_squares(self):
        for row in range(8, 0, -1):  # Duyệt từ hàng 8 đến 1
            for col in range(8):  # Duyệt từ cột a (0) đến h (7)
                square = chess.square(col, row - 1)  # Lấy chỉ mục ô hiện tại
                piece = self.logic_board.piece_at(square)

                if not piece:
                    self.squares[8 - row][col].piece = None
                # Quân Pawn
                elif piece.symbol() == "P":
                    self.squares[8 - row][col] = Square(8 - row, col, Pawn("white"))
                elif piece.symbol() == "p":
                    self.squares[8 - row][col] = Square(8 - row, col, Pawn("black"))
                # Quân Knight
                elif piece.symbol() == "N":
                    self.squares[8 - row][col] = Square(8 - row, col, Knight("white"))
                elif piece.symbol() == "n":
                    self.squares[8 - row][col] = Square(8 - row, col, Knight("black"))
                # Quân Bishop
                elif piece.symbol() == "B":
                    self.squares[8 - row][col] = Square(8 - row, col, Bishop("white"))
                elif piece.symbol() == "b":
                    self.squares[8 - row][col] = Square(8 - row, col, Bishop("black"))
                # Quân Rook
                elif piece.symbol() == "R":
                    self.squares[8 - row][col] = Square(8 - row, col, Rook("white"))
                elif piece.symbol() == "r":
                    self.squares[8 - row][col] = Square(8 - row, col, Rook("black"))
                # Quân Queen
                elif piece.symbol() == "Q":
                    self.squares[8 - row][col] = Square(8 - row, col, Queen("white"))
                elif piece.symbol() == "q":
                    self.squares[8 - row][col] = Square(8 - row, col, Queen("black"))
                # Quân King
                elif piece.symbol() == "K":
                    self.squares[8 - row][col] = Square(8 - row, col, King("white"))
                elif piece.symbol() == "k":
                    self.squares[8 - row][col] = Square(8 - row, col, King("black"))

    def _create(self):
        # Tạo các đối tượng Square trên bàn cờ
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

