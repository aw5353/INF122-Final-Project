from tkinter import *
from tkinter import ttk

from ._2048 import *

class Application:
    def __init__(self):
        self.root = Tk()
        self.game = Game2048()
        self.frm = ttk.Frame(self.root, padding=10)
        self.root.title("2048")
        self.root.geometry("600x600")
        self.bind_keys()
        self.size = 4
        self.cell_size = 100
        self.grid_padding = 10
        self.canvas = Canvas(self.root, 
                     width=self.size * self.cell_size + (self.size + 1) * self.grid_padding, 
                     height=self.size * self.cell_size + (self.size + 1) * self.grid_padding, 
                     bg="#bbada0")

        self.colors = {
            0: "#cdc1b4", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
            16: "#f59563", 32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72",
            256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"
        }

        # Create a Frame to hold the score and button
        self.top_frame = Frame(self.root, bg="#bbada0")
        self.top_frame.pack(pady=10)

        # Score Label
        self.score_label = Label(self.top_frame, text="Score: " + str(self.game.players[0].score), 
                                font=("Arial", 16), bg="#bbada0", fg="white")
        self.score_label.pack(side="left", padx=40)

        # New Game Button
        self.new_game_button = Button(self.top_frame, text="New Game", font=("Arial", 14, "bold"), 
                                    bg="#8f7a66", fg="white", command=self.reset_game)
        self.new_game_button.pack(side="right")


        self.canvas.pack()
        self.update_grid()
        self.process_events()

    def reset_game(self):
        """Resets the game and updates the UI."""
        self.game = Game2048()
        self.update_grid()

    def update_grid(self):
        """Update the GUI to match the board state."""
        self.score_label.config(text="Score: " + str(self.game.players[0].score))
        self.draw_grid()


    def draw_grid(self):
        """Draws the 4x4 grid with tiles."""
        self.canvas.delete("all")
        for r in range(self.size):
            for c in range(self.size):
                x0 = c * self.cell_size + (c + 1) * self.grid_padding
                y0 = r * self.cell_size + (r + 1) * self.grid_padding
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size

                tile = self.game.gameBoard[r][c]

                if tile:
                    color = self.colors.get(tile.point_value, "#3c3a32")
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="#bbada0", width=5)
                    self.canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=str(tile.point_value),
                                            font=("Arial", 24, "bold"), fill="white" if tile.point_value > 4 else "black")
                else:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill=self.colors.get(0, "#3c3a32"), outline="#bbada0", width=5)
                

    def on_key(self, event):
        key = event.keysym
        input_event = None

        match key:
            case "Up":
                input_event = UpKey(self.game)
            case "Down":
                input_event = DownKey(self.game)
            case "Right":
                input_event = RightKey(self.game)
            case _:
                input_event = LeftKey(self.game)

        self.game.events.append(input_event)
        self.game.events.append(CheckWin(self.game))
        self.game.events.append(CheckLoss(self.game))

    def process_events(self):
        while self.game.events:
            self.game.handleEvents()

        self.update_grid()
        self.root.after(100, self.process_events)

    def bind_keys(self):
        self.root.bind("<Up>", self.on_key)
        self.root.bind("<Down>", self.on_key)
        self.root.bind("<Left>", self.on_key)
        self.root.bind("<Right>", self.on_key)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = Application()
    gui.run()