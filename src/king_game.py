
import pygame

from const import *
from board import Board
from dragger import Dragger
from config import Config
from square import Square
from piece import King
from bot_module.bot import Bot

from bot_module.bot_logic import evaluate_board

class Game:
    def __init__(self):
        self.next_player = FIRST_PLAYER
        self.hovered_sqr = None
        self.board = Board(self, fen=START_FEN)
        self.dragger = Dragger()
        self.config = Config()
        
        self.is_draw = False# kiểm tra xem ván cờ có hòa
        self.winner = None
        self.end_state = None# lưu trạng thái kết thúc của ván cờ

        # bot
        self.bot = Bot(BOT_COLOR, self)


    # Hàm vẽ lên màn hình
    def show_bg(self, surface:pygame.Surface):
        theme = self.config.theme
        for row in range(ROWS):
            for col in range(COLS):
                # Màu ô xen kẽ
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                # rect của ô đó
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE) #(x, y, width, height)
                # Vẽ lên màn hình
                pygame.draw.rect(surface, color, rect)

                # Tọa độ hàng (row)
                if col == 0:
                    # Màu chữ
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    # Nhãn để tọa độ
                    lbl = self.config.font.render(str(ROWS - row), 1, color)
                    lbl_pos = (5, 5 + row * SQSIZE)
                    # Vẽ lên màn hình
                    surface.blit(lbl, lbl_pos)

                # Tọa độ cột (col)
                if row == 7:
                    # Màu chữ
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    # Nhãn để tọa độ
                    lbl = self.config.font.render(Square.get_alphacol(col), 1, color)
                    lbl_pos = (col * SQSIZE + SQSIZE - 20, HEIGHT - 20)
                    # Vẽ lên màn hình
                    surface.blit(lbl, lbl_pos)

    def show_last_move(self, surface:pygame.Surface):
        theme = self.config.theme

        if self.board.last_move:
            initial_move = self.board.last_move.initial
            final_move = self.board.last_move.final

            for pos in [initial_move, final_move]:
                color = theme.trace.light if (pos.row + pos.col ) % 2 == 0 else theme.trace.dark
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                # 
                pygame.draw.rect(surface, color, rect)

    def show_moves(self, surface:pygame.Surface):
        # Vẽ lại các ô có thể di chuyển của quân cờ đang được chọn 

        theme = self.config.theme

        if self.dragger.dragging:
            # Quân cờ đang được kéo thả
            piece = self.dragger.piece

            # Lặp qua từng nước đi hợp lệ của quân cờ này
            for move in piece.moves:
                # Ở đây, set màu sáng hay tối của các nước đi
                # sao cho phù hợp với màu nền ban đầu
                color = theme.moves.light if (move.final.row + move.final.col) else theme.moves.dark
                # 
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                # Vẽ
                pygame.draw.rect(surface, color, rect) 

    def show_pieces(self, surface:pygame.Surface):
        for row in range(ROWS):
            for col in range(COLS):
                # Đi qua từng ô trên bàn cờ
                # Nếu có quân cờ
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    # Vẽ mọi quân cờ ngoại trừ quân cờ đang được kéo thả
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def show_hover(self, surface:pygame.Surface):
        pass

    def show_end(self, surface:pygame.Surface, end_message:str):
        # Vẽ nền phía sau
        rect = (0, 0, WIDTH, HEIGHT)
        # Vẽ
        pygame.draw.rect(surface, "black", rect) 

        # Load hình ảnh
        img = pygame.image.load(self.config.winner_pic_path)
        # Thay đổi kích thước
        img = pygame.transform.scale(img, (WIDTH // 2, HEIGHT // 2))
        # Căn giữa màn hình
        img_center = WIDTH // 2, HEIGHT // 2
        img_rect = img.get_rect(center=img_center)
        # 
        surface.blit(img, img_rect)

        # In bên thắng
        lbl = self.config.font.render(end_message, 1, "white")
        lbl_pos = lbl.get_rect(center=(WIDTH // 2, HEIGHT * 0.8))
        surface.blit(lbl, lbl_pos)

    def show_pawn_promotion(self, surface:pygame.Surface):
        # Vẽ nền phía sau
        rect = (0, 0, WIDTH, HEIGHT)
        # Vẽ
        pygame.draw.rect(surface, "purple", rect) 

        # Load hình ảnh
        img = pygame.image.load(self.config.pawn_pro_pic_path)
        # Thay đổi kích thước
        img = pygame.transform.scale(img, (WIDTH // 2, HEIGHT // 2))
        # Căn giữa màn hình
        img_center = WIDTH // 2, HEIGHT // 2
        img_rect = img.get_rect(center=img_center)
        # 
        surface.blit(img, img_rect)


    # Các hàm khác
    def next_turn(self):
        '''
            Hàm đổi lượt, check end mỗi lần đổi
                1. Check xem ván đấu có kết thúc
                2. Nếu ván đấu kết thúc, kết thúc
                3. Đổi lượt
                4. Nếu ván đấu chưa kết thúc, nếu đến lượt bot, nó tính toán nước đi 
        '''

        self.check_end()

        if self.end_state:
            return
        
        self.next_player = 'white' if self.next_player == 'black' else 'black'

        # bot
        if not self.end_state:
            if self.next_player == BOT_COLOR:
                self.bot.calculate_action()


    def promotion_to(self, piece:str):
        board = self.board
        # Thực hiện nước đi thăng cấp với quân cờ được chọn 
        board.move(board.pre_pawn_promotion_move, piece)
        
  
    def set_hover(self, row, col):
        pass

    def change_theme(self):
        pass

    def play_sound(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()
        
    def reset(self):
        self.__init__()

    def check_end(self):
        logic_board = self.board.logic_board
        
        if logic_board.is_checkmate():
            if logic_board.turn:
                self.end_state = "BLACK win"
            else:
                self.end_state = "WHITE win"

        elif logic_board.is_stalemate():
            # Hòa do luật quân vua 1 bên hết nước đi nhưng không bị chiếu
            self.end_state = "DRAW: stalemate"

        elif logic_board.is_insufficient_material():
            # Hòa do không đủ lực chiếu hết
            self.end_state = "DRAW: insufficient material"
            
        elif logic_board.is_seventyfive_moves():
            # Hòa do luật 75 nước đi
            self.end_state = "DRAW: seventy-five move rule"

        elif logic_board.is_fivefold_repetition():
            # Hòa do luật lặp lại 5 lần
            self.end_state = "DRAW: fivefold repetition"
                    
        return self.end_state