class Move:
    def __init__(self, initial, final):
        self.initial = initial
        self.final = final
        self.promotion_to = None# Thuộc tính dùng xử lý nước đi thăng cấp
    def __str__(self):
        s = ''
        s += f'({self.initial.col}, {self.initial.row})'
        s += f' -> ({self.final.col}, {self.final.row})'
        return s
    def __eq__(self, other):
        """Truyền vào 1 Piece"""
        return self.initial == other.initial and self.final == other.final    
    def to_index(self):
        # VD: ((0, 0), (0, 1))
        return (self.initial.row, self.initial.col), (self.final.row, self.final.col) 
    def to_uci(self):
        return Move.index_to_uci(self.to_index()) + (self.promotion_to if self.promotion_to else "")   
    @classmethod
    def uci_to_index(cls, uci: str)->tuple:
        """
        Chuyển tọa độ UCI thành tọa độ (0-7,7-0) với hàng đảo ngược.
        Trả và 1 tuple (tuple toạ độ bắt đầu, tuple toạ độ kết thúc).
        
        """
        rs = {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7}
        cs = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

        init_col, init_row = uci[0], uci[1]
        final_col, final_row = uci[2], uci[3]
        return (rs[init_row], cs[init_col]), (rs[final_row], cs[final_col])
    
    @classmethod
    def index_to_uci(cls, index:tuple)->str:
        rs = {0: '8', 1: '7', 2: '6', 3: '5', 4: '4', 5: '3', 6: '2', 7: '1'}
        cs = {0: 'a', 1: 'b', 2: 'c' , 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

        init_col, init_row = index[0][1], index[0][0]
        final_col, final_row = index[1][1], index[1][0]
        return cs[init_col] + rs[init_row] + cs[final_col] + rs[final_row]
