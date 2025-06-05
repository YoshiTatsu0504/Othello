import tkinter as tk
from tkinter import messagebox
from typing import Optional

from .board import Board, BLACK, WHITE, EMPTY, BOARD_SIZE
from .ai import choose_move

CELL_SIZE = 60


class OthelloGUI:
    def __init__(self) -> None:
        self.board = Board()
        self.current_player = BLACK  # human is BLACK by default

        self.root = tk.Tk()
        self.root.title('Othello')

        self.canvas = tk.Canvas(
            self.root,
            width=BOARD_SIZE * CELL_SIZE,
            height=BOARD_SIZE * CELL_SIZE,
            bg='darkgreen'
        )
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.on_click)

        self.status = tk.Label(self.root, text='', font=('Arial', 14))
        self.status.pack()

        self.draw_board()
        self.update_status()

    def draw_board(self) -> None:
        self.canvas.delete('all')
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                x1 = x * CELL_SIZE
                y1 = y * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, outline='black')
                piece = self.board.get(x, y)
                if piece is not EMPTY:
                    color = 'black' if piece == BLACK else 'white'
                    self.canvas.create_oval(
                        x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill=color
                    )

    def update_status(self) -> None:
        black_count = self.board.count(BLACK)
        white_count = self.board.count(WHITE)
        self.status.config(text=f'Black: {black_count}  White: {white_count}')

    def on_click(self, event: tk.Event) -> None:
        x = event.x // CELL_SIZE
        y = event.y // CELL_SIZE
        if self.board.apply_move(self.current_player, x, y):
            self.switch_player()
            self.draw_board()
            self.update_status()
            self.root.after(200, self.ai_move)
        else:
            messagebox.showinfo('Invalid', 'Invalid move')

    def switch_player(self) -> None:
        self.current_player = WHITE if self.current_player == BLACK else BLACK

    def ai_move(self) -> None:
        move = choose_move(self.board, self.current_player)
        if move is None:
            if not self.board.get_valid_moves(BLACK if self.current_player == WHITE else WHITE):
                self.game_over()
            else:
                self.switch_player()
            return
        x, y = move
        self.board.apply_move(self.current_player, x, y)
        self.switch_player()
        self.draw_board()
        self.update_status()
        if not self.board.get_valid_moves(self.current_player):
            if not self.board.get_valid_moves(BLACK if self.current_player == WHITE else WHITE):
                self.game_over()
            else:
                self.switch_player()
                self.root.after(200, self.ai_move)

    def game_over(self) -> None:
        black = self.board.count(BLACK)
        white = self.board.count(WHITE)
        if black > white:
            winner = 'Black wins!'
        elif white > black:
            winner = 'White wins!'
        else:
            winner = "It's a draw!"
        messagebox.showinfo('Game Over', f'{winner}\nBlack: {black}  White: {white}')
        self.root.quit()

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    gui = OthelloGUI()
    gui.run()


if __name__ == '__main__':
    main()
