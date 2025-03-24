import pygame

from const import *
from piece import Piece

class Dragger:
    def __init__(self):
        # Quân cờ đang được kéo thả
        self.piece = None
        
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0

    def show_hover_piece(self, surface:pygame.Surface):
        piece = self.piece
        mouseX = self.mouseX
        mouseY = self.mouseY

        if piece:
            piece.set_texture(size=128)
            img = pygame.image.load(piece.texture)
            img_center = (self.mouseX, self.mouseY)
            self.piece.texture_rect = img.get_rect(center=img_center)
            # 
            surface.blit(img, self.piece.texture_rect)

    # Hàm chức năng khác
    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos

    def save_initial(self, pos):
        self.initial_row = pos[1] // SQSIZE
        self.initial_col = pos[0] // SQSIZE

    def drag_piece(self, piece:Piece):
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        self.piece = None
        self.dragging = False

    def get_row(self):
        return self.mouseY // SQSIZE

    def get_col(self):
        return self.mouseX // SQSIZE