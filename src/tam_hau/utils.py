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