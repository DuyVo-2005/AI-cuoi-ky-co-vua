import os

def queen_board(position_str):
  n = len(position_str)
  board = []
  
  for row in range(n):
    line = ['.'] * n
    col = int(position_str[row]) - 1
    line[col] = 'Q'
    board.append(' '.join(line))
  
  return '\n'.join(board)

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "data", "solution.txt")
def read_lines_to_list(file_path=file_path):
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]  # Bỏ dòng trắng
    return lines


import pygame

def show_pygame_board(data):
    board_size = len(data)
    queen_positions = [(i, int(data[i]) - 1) for i in range(board_size)]
    pygame.init()
    screen_size = 400
    cell_size = screen_size // board_size
    screen = pygame.display.set_mode((screen_size, screen_size))
    pygame.display.set_caption("Eight Queens Visualization")
    icon = pygame.image.load(os.path.join(base_dir, "images", "icon.png"))
    pygame.display.set_icon(icon)

    white = (255, 255, 255)
    black = (0, 0, 0)

    queen_image = pygame.image.load(os.path.join(base_dir, "images", "white_queen.png"))
    queen_image = pygame.transform.scale(queen_image, (cell_size, cell_size))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(white)

        for row in range(board_size):
            for col in range(board_size):
                rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                if (row + col) % 2 == 0:
                    pygame.draw.rect(screen, white, rect)
                else:
                    pygame.draw.rect(screen, black, rect)

        for row, col in queen_positions:
            screen.blit(queen_image, (col * cell_size, row * cell_size))

        pygame.display.flip()

    pygame.quit()



