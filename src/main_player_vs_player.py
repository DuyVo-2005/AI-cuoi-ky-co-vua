import pygame
import sys
import chess

from const import *
from game import Game
from move import Move
from square import Square

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
        game.is_player_vs_player_mode = True

        while True:
            clock.tick(100)

            if game.end_state:
                game.show_end(screen, game.end_state)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                pygame.display.update()
                continue
            
            '''
                Xử lý cho màn hình chọn thăng cấp
            '''
            if game.board.is_on_pawn_promotion:
                game.show_pawn_promotion(screen)
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouseX, mouseY = event.pos
                        if mouseX < WIDTH // 2 and mouseY < HEIGHT // 2:
                            game.promotion_to("q")
                        elif mouseX > WIDTH // 2 and mouseY < HEIGHT // 2:
                            game.promotion_to("b")
                        elif mouseX < WIDTH // 2 and mouseY > HEIGHT // 2:
                            game.promotion_to("r")
                        elif mouseX > WIDTH // 2 and mouseY > HEIGHT // 2:
                            game.promotion_to("n")

                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                pygame.display.update()
                continue

            '''
                Xử lý thông thường của trò chơi
            '''
            #Hiển thị các thành phần
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)# Hiện các nước đi hợp lệ
            game.show_hover(screen)
            game.show_pieces(screen)

            #Hiển thị quân cờ đang được kéo thả
            if dragger.dragging:
                dragger.show_hover_piece(screen)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #Cập nhật thuộc tính tọa độ chuột trong dragger object
                    dragger.update_mouse(event.pos)
                    #Lấy row và col của ô mới click
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

                elif event.type == pygame.MOUSEMOTION:               
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                elif event.type == pygame.MOUSEBUTTONUP:                     
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        #tạo các nước đi có thể
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        # valid move ?
                        if board.valid_move(dragger.piece, move):
                            # normal capture
                            captured = board.squares[released_row][released_col].has_piece()

                            board.move(move)                              
                            game.play_sound(captured)
                            #Nước nếu là nước đi thăng cấp, chưa đổi lượt
                            if game.board.check_player_promotion(move):
                                pass


                        dragger.piece.clear_moves()
                        dragger.undrag_piece()

                # Khi nhấn phím
                elif event.type == pygame.KEYDOWN:
                    # if event.key == pygame.K_SPACE:
                    #     print("current eva:", evaluate_board(board.logic_board))
                    pass

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()

main = Main()
main.mainloop()