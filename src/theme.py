from color import Color

class Theme:
    # Mỗi Theme có 6 màu khác nhau, thuộc 3 đối tượng khác nhau
    # Màu của nền: sáng - tối
    # Màu của nền quân cờ mới đi (trace): sáng - tối
    # Màu của nước đi có thể: sáng - tối

    def __init__(self, light_bg, dark_bg,
                       light_trace, dark_trace,
                       light_moves, dark_moves):
        self.bg = Color(light_bg, dark_bg)
        self.trace = Color(light_trace, dark_trace)
        self.moves = Color(light_moves, dark_moves)