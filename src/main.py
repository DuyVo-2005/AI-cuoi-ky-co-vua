import pygame
import sys

from const import *
from game import Game
from move import Move
from square import Square
import chess
from bot_module.bot_logic import evaluate_board


clock = pygame.time.Clock()


class Main:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Chess")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.game = Game()
        
        # Biến đặc biệt để vẽ không bị khựng
        self.cal_on_next_loop = False

    def mainloop(self):

        screen = self.screen
        game = self.game
        dragger = self.game.dragger
        board = self.game.board

        while True:
            # FPS
            clock.tick(60)

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
                Xử lý cho màn hình chọn thăng cấp
            '''
            # Hiển thị màn hình chọn quân cờ để nâng cấp cho quân tốt
            if game.board.is_on_pawn_promotion:
                game.show_pawn_promotion(screen)

                # Xử lý event
                for event in pygame.event.get():
                    # Khi click
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouseX, mouseY = event.pos
                        # Nếu click chọn quân Queen
                        if mouseX < WIDTH // 2 and mouseY < HEIGHT // 2:
                            game.promotion_to("q")
                        # Nếu click chọn quân Bishop
                        elif mouseX > WIDTH // 2 and mouseY < HEIGHT // 2:
                            game.promotion_to("b")
                        # Nếu click chọn quân Rook
                        elif mouseX < WIDTH // 2 and mouseY > HEIGHT // 2:
                            game.promotion_to("r")
                        # Nếu click chọn quân Knight
                        elif mouseX > WIDTH // 2 and mouseY > HEIGHT // 2:
                            game.promotion_to("n")

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

            # Hiển thị quân cờ đang được kéo thả
            if dragger.dragging:
                dragger.show_hover_piece(screen)

            # Nếu bot có move, thực hiện action của nó trong vòng lặp này
            if game.bot.move:
                game.bot.make_action()
                continue

            # Bắt đầu tính toán ở Loop này
            # if self.cal_on_next_loop:
            #     self.cal_on_next_loop = False
            #     board.move(move)     

            # Xử lý event
            for event in pygame.event.get():
                # Khi click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Click chọn quân cờcờ
                    if game.next_player == PLAYER_COLOR:

                        # Cập nhật thuộc tính tọa độ chuột trong dragger object
                        dragger.update_mouse(event.pos)
                        # Lấy row và col của ô mới click
                        clicked_row = dragger.get_row()
                        clicked_col = dragger.get_col()

                        # Nếu click trúng một ô đang có quân cờ
                        if board.squares[clicked_row][clicked_col].has_piece():
                            piece = board.squares[clicked_row][clicked_col].piece
                            
                            # Check quân cờ đó có đang đúng lượt với người chơi
                            if piece.color == game.next_player:
                                # Tính toán các nước đi hợp lệ của quân cờ
                                board.calculate_moves(piece, clicked_row, clicked_col)
                                dragger.save_initial(event.pos)
                                dragger.drag_piece(piece)
                                # Hiển thị lại các đối tượng
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_moves(screen) # Hiện các nước đi hợp lệ
                                game.show_hover(screen)
                                game.show_pieces(screen)

                # Khi di chuột
                elif event.type == pygame.MOUSEMOTION:
                    # Kéo quân cờ
                    if game.next_player == PLAYER_COLOR:
                        if dragger.dragging:
                            dragger.update_mouse(event.pos)

                # Khi nhả click chuột
                elif event.type == pygame.MOUSEBUTTONUP:
                    # 
                    if game.next_player == PLAYER_COLOR:
                        
                        if dragger.dragging:
                            dragger.update_mouse(event.pos)

                            released_row = dragger.mouseY // SQSIZE
                            released_col = dragger.mouseX // SQSIZE

                            # create possible move
                            initial = Square(dragger.initial_row, dragger.initial_col)
                            final = Square(released_row, released_col)
                            move = Move(initial, final)

                            # valid move ?
                            if board.valid_move(dragger.piece, move):
                                # normal capture
                                captured = board.squares[released_row][released_col].has_piece()

                                board.move(move)                  

                                # sounds
                                game.play_sound(captured)

                                # Nước nếu là nước đi thăng cấp, chưa đổi lượt
                                if game.board.check_player_promotion(move):
                                    pass


                            dragger.piece.clear_moves()
                            dragger.undrag_piece()

                # Khi nhấn phím
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print("current eva:", evaluate_board(board.logic_board))

                # Khi thoát
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


            # pygame update 
            pygame.display.update()

main = Main()
main.mainloop()