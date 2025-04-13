def generate_king_moves(state: tuple):
    x, y = state[0], state[1]
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]
    moves = []
    for (dx, dy) in directions:
        new_x = x + dx
        new_y = y + dy
        if 0 <= new_x < 8 and 0 <= new_y < 8:
            moves.append(((dx, dy),(new_x, new_y)))
    return moves