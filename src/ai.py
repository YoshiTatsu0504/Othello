import random
from typing import Tuple, Optional

from .board import Board


def random_move(board: Board, color: str) -> Optional[Tuple[int, int]]:
    moves = board.get_valid_moves(color)
    if not moves:
        return None
    return random.choice(moves)


def greedy_move(board: Board, color: str) -> Optional[Tuple[int, int]]:
    moves = board.get_valid_moves(color)
    if not moves:
        return None
    best_move = None
    best_score = -1
    for x, y in moves:
        temp = board.copy()
        temp.apply_move(color, x, y)
        score = temp.count(color)
        if score > best_score:
            best_score = score
            best_move = (x, y)
    return best_move

# default AI
choose_move = greedy_move
