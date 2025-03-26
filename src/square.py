class Square:
    def __init__(self, row:int, col:int, piece=None)->None:
        self.row = row
        self.col = col
        self.piece = piece
        self.alphacol = Square.get_alphacol(col)

    def __eq__(self, other:Square)->bool:
        return self.row == other.row and self.col == other.col

    def has_piece(self)->bool:
        return self.piece

    def isempty(self)->bool:
        return not self.has_piece()

    def has_team_piece(self, team_color:str)->bool:
        return self.has_piece() and self.piece.color == team_color

    def has_enemy_piece(self, team_color:str)->bool:
        return self.has_piece() and self.piece.color != team_color

    def isempty_or_enemy(self, team_color:str)->bool:
        return self.isempty() or self.has_enemy_piece(team_color)

    #static method cho phép gọi trực tiếp từ lớp
    @staticmethod
    def in_range(*args)->bool:
        # Hàm check xem các số cột, hàng có hợp lệ
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True

    @staticmethod
    def get_alphacol(col)->bool:
        # Nhận 1 chỉ mục của cột và trả về chữ tương ứng
        # Ví dụ: 0 -> 'a'
        # Vì cột 0 của bàn cờ được quy ước là cột 'a'
        alpha_cols = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        return alpha_cols[col]
