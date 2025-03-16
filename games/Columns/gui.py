from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from .columns import ColumnsGame
from engine.timer import Timer

class Application:
    def __init__(self):
        self.timer = Timer()
        self.root = Tk()
        self.root.title("Columns Game")
        
        self.frm = ttk.Frame(self.root, padding=10)
        
        self.game = ColumnsGame()
        self.current_player = 1
        self.scores = {1: 0, 2: 0}
        
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

        self.info_frame = ttk.Frame(self.root)
        self.info_frame.pack(side=TOP, pady=5)
        
        self.player_label = ttk.Label(self.info_frame, text="Player 1's Turn")
        self.player_label.pack(side=LEFT, padx=10)
        
        self.score_label = ttk.Label(self.info_frame, text="P1: 0 | P2: 0")
        self.score_label.pack(side=LEFT, padx=10)

        self.root.bind('<Left>', lambda e: self.handle_input(1, 'left'))
        self.root.bind('<Right>', lambda e: self.handle_input(1, 'right'))
        self.root.bind('<Up>', lambda e: self.handle_input(1, 'rotate'))
        self.root.bind('<Down>', lambda e: self.handle_input(1, 'drop'))
        
        self.root.bind('a', lambda e: self.handle_input(2, 'left'))
        self.root.bind('d', lambda e: self.handle_input(2, 'right'))
        self.root.bind('w', lambda e: self.handle_input(2, 'rotate'))
        self.root.bind('s', lambda e: self.handle_input(2, 'drop'))

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

    def reset_game(self):
        self.game = ColumnsGame()
        self.current_player = 1
        self.scores = {1: 0, 2: 0}
        self.player_label.config(text="Player 1's Turn")
        self.score_label.config(text="P1: 0 | P2: 0")
        self.timer.reset()
        self.start_game()

    def game_over_prompt(self):
        self.timer.stop()
        winner = 1 if self.scores[1] > self.scores[2] else 2
        if self.scores[1] == self.scores[2]:
            winner_text = "It's a tie!"
        else:
            winner_text = f"Player {winner} wins!"
            
        response = messagebox.askyesno(
            "Game Over",
            f"Game Over!\n{winner_text}\n"
            f"Player 1 Score: {self.scores[1]}\n"
            f"Player 2 Score: {self.scores[2]}\n"
            f"Time played: {int(self.timer.tick/60) + 1} seconds\n\n"
            "Would you like to play again?"
        )
        if response:
            self.reset_game()
        else:
            self.root.destroy()

    def update_game(self):
        if self.game.running:
            self.game.drop_piece()
            self.draw_board()
            
            if (self.game.piece_row == 0 and 
                self.game.gameBoard.getBoardState()[0][self.game.piece_col].point_value != 0):
                self.game.running = False
                self.game_over_prompt()
                return
            
            # Check if piece is locked and switch players
            if self.game.piece_locked:
                self.scores[self.current_player] += self.game.last_score
                self.current_player = 2 if self.current_player == 1 else 1
                self.player_label.config(text=f"Player {self.current_player}'s Turn")
                self.score_label.config(text=f"P1: {self.scores[1]} | P2: {self.scores[2]}")
                self.game.piece_locked = False

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

    def run(self):
        self.root.mainloop()

    def handle_input(self, player, action):
        """Handle player input based on current turn"""
        if not self.game.running or player != self.current_player:
            return
            
        if action == 'left':
            self.move_piece(-1)
        elif action == 'right':
            self.move_piece(1)
        elif action == 'rotate':
            self.rotate_piece()
        elif action == 'drop':
            self.force_drop()

if __name__ == "__main__":
    app = Application()
    app.run()