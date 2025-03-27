import pygame
import os

from sound import Sound
from theme import Theme

class Config:
    # Chứa các Theme, Font, move_sound, capture_sound của game
    
    def __init__(self):
        # Các thông số Theme
        self.themes = []
        self._add_themes()
        self.theme_idx = 0
        self.theme = self.themes[self.theme_idx]

        # Font của trò chơi
        self.font = pygame.font.SysFont("monospace", 13, bold=True)

        # Âm thanh khi di chuyển và ăn quân cờ
        self.move_sound = Sound(os.path.join('assets/sounds/move.wav'))
        self.capture_sound = Sound(os.path.join('assets/sounds/capture.wav'))
        
        # Âm thanh khi kết thúc game
        self.end_game_sound = Sound(os.path.join('assets/sounds/game-end.mp3'))

        # Âm thanh khi quân tốt được nâng cấpcấp
        self.pawn_pro_sound = Sound(os.path.join('assets/sounds/power-pawn.mp3'))

        # Hình ảnh khi kết thúc game
        self.winner_pic_path = os.path.join('assets/images/winner.png')
        # Hình ảnh khi nâng cấp quân tốttốt
        self.pawn_pro_pic_path = os.path.join('assets/images/pawn_pro.png')

    def change_theme(self):
        pass

    def _add_themes(self):
        green_theme = Theme((234, 235, 200), (119, 154, 88), (244, 247, 116), (172, 195, 51), (200, 100, 100), (200, 70, 70))

        self.themes.append(green_theme)
