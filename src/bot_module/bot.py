
from const import *
from square import Square
from move import Move
import bot_module.bot_logic as bl

from threading import Event, Thread

class Bot:
    def __init__(self, color:str, game):
        self.color = color
        self.game = game

        # Thuộc tính chứa nước di chuyển của bot
        self.move = None
        self.node_tree = None

        # Thuộc tính để xử lý luồng tính toán
        self.calculating = Event()

    # Các hàm sử dụng trong main
    def make_action(self):
        self.game.board.move(self.move)
        self.move = None

        # Unset cờ calculating
        self.calculating.clear()


    def calculate_action(self):
        # Set cờ này để không block UI
        self.calculating.set()

        def cal(self):
            # Tính toán nước đi tốt nhất
            move = bl.find_best_move(self.game.board.logic_board)
            uci_move = move.uci()
            index_move = Move.uci_to_index(uci_move)
            self.move = Move(Square(index_move[0][0], index_move[0][1]), Square(index_move[1][0], index_move[1][1]))
            return

        # Chạy Thread khác để không block
        cal_thread = Thread(target=cal, args=(self,))
        cal_thread.start()


