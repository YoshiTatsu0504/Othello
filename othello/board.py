from __future__ import annotations

from typing import List, Optional, Tuple


EMPTY = None
BLACK = 'B'
WHITE = 'W'

BOARD_SIZE = 8

directions = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),          (0, 1),
    (1, -1),  (1, 0), (1, 1)
]

class Board:
    """Represents an Othello game board."""

    def __init__(self) -> None:
        self.grid: List[List[Optional[str]]] = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.reset()

    def reset(self) -> None:
        """Initialize starting position."""
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                self.grid[y][x] = EMPTY
        mid = BOARD_SIZE // 2
        self.grid[mid - 1][mid - 1] = WHITE
        self.grid[mid][mid] = WHITE
        self.grid[mid - 1][mid] = BLACK
        self.grid[mid][mid - 1] = BLACK

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE

    def get(self, x: int, y: int) -> Optional[str]:
        return self.grid[y][x]

    def set(self, x: int, y: int, color: Optional[str]) -> None:
        self.grid[y][x] = color

    def _captures_in_direction(self, color: str, x: int, y: int, dx: int, dy: int) -> List[Tuple[int, int]]:
        path = []
        cx, cy = x + dx, y + dy
        opp = BLACK if color == WHITE else WHITE
        while self.in_bounds(cx, cy) and self.get(cx, cy) == opp:
            path.append((cx, cy))
            cx += dx
            cy += dy
        if self.in_bounds(cx, cy) and self.get(cx, cy) == color:
            return path
        return []

    def captures(self, color: str, x: int, y: int) -> List[Tuple[int, int]]:
        if self.get(x, y) is not EMPTY:
            return []
        captured: List[Tuple[int, int]] = []
        for dx, dy in directions:
            captured.extend(self._captures_in_direction(color, x, y, dx, dy))
        return captured

    def is_valid_move(self, color: str, x: int, y: int) -> bool:
        return len(self.captures(color, x, y)) > 0

    def get_valid_moves(self, color: str) -> List[Tuple[int, int]]:
        moves = []
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                if self.is_valid_move(color, x, y):
                    moves.append((x, y))
        return moves

    def apply_move(self, color: str, x: int, y: int) -> bool:
        captured = self.captures(color, x, y)
        if not captured:
            return False
        self.set(x, y, color)
        for cx, cy in captured:
            self.set(cx, cy, color)
        return True

    def count(self, color: str) -> int:
        return sum(1 for row in self.grid for cell in row if cell == color)

    def is_full(self) -> bool:
        return all(cell is not EMPTY for row in self.grid for cell in row)

    def copy(self) -> 'Board':
        new = Board()
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                new.grid[y][x] = self.grid[y][x]
        return new
