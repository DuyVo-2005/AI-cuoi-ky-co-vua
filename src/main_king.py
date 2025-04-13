import pygame
import sys

from king_const import *
from game import Game
from move import Move
from square import Square
import chess
from bot_module.bot_logic import evaluate_board
from board import Board

def to_fen(king_pos: tuple)->str:
    # Khởi tạo bàn cờ trống 8x8
    board = [['1' for _ in range(8)] for _ in range(8)]

    # Chuyển đổi tọa độ ví dụ: 'e4' => (hàng 4, cột 4)
    # def to_index(pos):
    #     col = ord(pos[0].lower()) - ord('a')
    #     row = 8 - int(pos[1])
    #     return row, col

    # Đặt vua và hậu lên bàn cờ
    # row_k, col_k = to_index(vua)
    # row_q, col_q = to_index(hau)
    
    row_k, col_k = king_pos[0], king_pos[1]
    #row_q, col_q = queen_pos[0], queen_pos[1]

    # if (row_k, col_k) == (row_q, col_q):
    #     raise ValueError("Vua và hậu không thể ở cùng một vị trí.")

    board[row_k][col_k] = 'K'

    # Tạo FEN từ bàn cờ
    fen_rows = []
    for row in board:
        fen_row = ''
        empty_count = 0
        for cell in row:
            if cell == '1':
                empty_count += 1
            else:
                if empty_count > 0:
                    fen_row += str(empty_count)
                    empty_count = 0
                fen_row += cell
        if empty_count > 0:
            fen_row += str(empty_count)
        fen_rows.append(fen_row)

    # Ghép các hàng thành chuỗi FEN (chỉ phần vị trí quân)
    fen = '/'.join(fen_rows) + " w - - 0 1"
    return fen

clock = pygame.time.Clock()

class Main:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("King")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.game = Game()
        self.path = None
        
        # Biến đặc biệt để vẽ không bị khựng
        self.cal_on_next_loop = False

    def mainloop(self):

        screen = self.screen
        game = self.game
        board = self.game.board

        i = 0
        while True:
            # FPS
            clock.tick(60)
            pygame.time.delay(1000)
            
            self.game.board = Board(self.game, fen=to_fen(self.path[i]))
            if i < len(self.path) - 1:
                i +=1

            # Hiển thị màn hình kết thúc nếu đã hết game
            if game.end_state:
                game.show_end(screen, game.end_state)

                # Xử lý event
                for event in pygame.event.get():
                    # Khi thoát
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                # pygame update 
                pygame.display.update()

                continue

            '''
                Xử lý thông thường của trò chơi
            '''
            # Hiển thị các thành phần
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen) # Hiện các nước đi hợp lệ
            game.show_hover(screen)
            game.show_pieces(screen)


            # Bắt đầu tính toán ở Loop này
            # if self.cal_on_next_loop:
            #     self.cal_on_next_loop = False
            #     board.move(move)     

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()