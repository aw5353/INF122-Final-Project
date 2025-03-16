import sys
from pathlib import Path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

sys.path.append(str(Path(__file__).parent.parent.parent))

from columns import ColumnsGame
from engine.timer import Timer

class ColumnsGUI:
    def __init__(self):
        self.timer = Timer()
        self.root = Tk()
        self.root.title("Columns Game")
        
        self.frm = ttk.Frame(self.root, padding=10)
        
        self.game = ColumnsGame()
        
        self.colors = {
            'R': 'red',
            'Y': 'yellow',
            'G': 'green',
            'F': 'blue',
            'L': 'purple',
            '_': '#faedcd'
        }
        
        self.cell_size = 45
        self.board_columns = len(self.game.gameBoard.grid[0])
        self.board_rows = len(self.game.gameBoard.grid)
        
        self.canvas = Canvas(
            self.root, 
            width=self.board_columns * self.cell_size + 20,
            height=self.board_rows * self.cell_size + 20,
            bg='white',
            highlightthickness=2,
            highlightbackground='#ECF0F1'
        )
        self.canvas.pack()

        self.root.bind('<Left>', lambda e: self.move_piece(-1))
        self.root.bind('<Right>', lambda e: self.move_piece(1))
        self.root.bind('<Up>', lambda e: self.rotate_piece())
        self.root.bind('<Down>', lambda e: self.force_drop())

        self.update_interval = 16
        self.start_game()

    def draw_board(self):
        self.canvas.delete("all")
        padding = 10
        
        for row in range(self.board_rows):
            for col in range(self.board_columns):
                x1 = col * self.cell_size + padding
                y1 = row * self.cell_size + padding
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill='#34495E',
                    outline='#2C3E50',
                    width=1
                )
        
        board = self.game.gameBoard.getBoardState()
        
        for row in range(self.board_rows):
            for col in range(self.board_columns):
                value = board[row][col].point_value
                color = self.colors.get(value, 'white')
                self.draw_cell(row, col, color)

        for i in range(3):
            if 0 <= self.game.piece_row - i < self.board_rows:
                color = self.colors.get(self.game.current_piece[i], 'white')
                self.draw_cell(self.game.piece_row - i, self.game.piece_col, color)

    def draw_cell(self, row, col, color):
        padding = 10
        cell_padding = 2
        
        x1 = col * self.cell_size + padding + cell_padding
        y1 = row * self.cell_size + padding + cell_padding
        x2 = x1 + self.cell_size - (2 * cell_padding)
        y2 = y1 + self.cell_size - (2 * cell_padding)
        
        shadow_offset = 2
        self.canvas.create_rectangle(
            x1 + shadow_offset, 
            y1 + shadow_offset, 
            x2 + shadow_offset, 
            y2 + shadow_offset, 
            fill='#1a1a1a', 
            outline=''
        )
        
        self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=color,
            outline='#ECF0F1',
            width=1
        )

    def move_piece(self, direction):
        if self.game.running:
            self.game.move_piece(direction)
            self.draw_board()
            self.root.update()

    def rotate_piece(self):
        if self.game.running:
            self.game.rotate_piece()
            self.draw_board()
            self.root.update()

    def force_drop(self):
        if self.game.running:
            while (self.game.piece_row + 2 < len(self.game.gameBoard.grid) + 1 and 
                   self.game.gameBoard.getBoardState()[self.game.piece_row + 1][self.game.piece_col].point_value == 0):
                self.game.drop_piece()
                self.draw_board()
                self.root.update()
                self.root.after(10)
            self.game.lock_piece()
            self.draw_board()

    def update_game(self):
        if self.game.running:
            self.game.drop_piece()
            self.draw_board()
            
            if (self.game.piece_row == 0 and 
                self.game.gameBoard.getBoardState()[0][self.game.piece_col].point_value != 0):
                self.game.running = False
                self.timer.stop()
                messagebox.showinfo("Game Over", f"Game Over!\nScore: {self.game.score}\nYou lasted {int(self.timer.tick/60)+1} seconds")
                self.root.destroy()
                return

    def game_loop(self):
        if self.timer.is_running:
            self.timer.update()
            if self.timer.tick % self.update_interval == 0:
                self.update_game()
            self.root.after(self.update_interval, self.game_loop)

    def start_game(self):
        self.timer.start()
        self.draw_board()
        self.game_loop()

if __name__ == "__main__":
    app = ColumnsGUI()
    app.root.mainloop()