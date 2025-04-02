import os
from move import Move

class Piece:
    def __init__(self, name:str, color:str, value:int, texture=None, texture_rect=None)->None:
        self.name = name
        self.color = color
        self.moves = [] # Các ô mà quân cờ có thể di chuyển
        self.moved = False # check có phải đã di chuyển chưa, để check nhập thành ở quân vua và xe
        self.texture = texture
        self.set_texture() # Thuộc tính texture sẽ được chuyển thành path tương đối dẫn đến file texture của quân 
        self.texture_rect = texture_rect
        
        # value_sign: để phân biệt dấu âm dương cho giải thuật Minimax
        value_sign = 1 if color == "white" else -1
        self.value = value_sign * value
        
    def set_texture(self, size:int=80)->None:
        self.texture = os.path.join(f'assets/images/imgs-{size}px/{self.color}_{self.name}.png')
    def add_move(self, move:Move)->None:
        self.moves.append(move)
    def clear_moves(self)->None:
        self.moves = []
    def is_black_king(self)->bool:
        return self.name == "king" and self.color == "black"
    def is_white_king(self)->bool:
        return self.name == "king" and self.color == "white"

class Pawn(Piece):
    def __init__(self, color:str) -> None:
        self.dir = -1 if color == 'white' else 1#hướng di chuyển tốt
        self.en_passant = False
        super().__init__("pawn", color, 10.0)

class Knight(Piece):
    def __init__(self, color:str)->None:
        super().__init__("knight", color, 30.0)

class Bishop(Piece):
    def __init__(self, color:str)->None:
        super().__init__("bishop", color, 31.1)

class Rook(Piece):
    def __init__(self, color:str)->None:
        super().__init__("rook", color, 50.0)

class Queen(Piece):   
    def __init__(self, color:str)->None:
        super().__init__("queen", color, 90.0)

class King(Piece):
    def __init__(self, color:str)->None:
        super().__init__("king", color, 100000.0)
