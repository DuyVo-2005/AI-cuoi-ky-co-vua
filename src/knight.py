def generate_knight_moves(state):
    x, y = state[0], state[1]
    moves = []# Danh sách chứa các nước đi hợp lệ
    directions = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2)
    ]
    
    for (dx, dy) in directions:
        new_x = x + dx
        new_y = y + dy
        if 0 <= new_x <= 7 and 0 <= new_y <= 7:
            moves.append(((x, y),(new_x, new_y)))
    
    return moves