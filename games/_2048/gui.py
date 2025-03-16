from tkinter import *
from tkinter import ttk

from ._2048 import *

class Application:
    def __init__(self):
        self.root = Tk()
        # Create two game instances
        self.game1 = Game2048()
        self.game2 = Game2048()
        self.frm = ttk.Frame(self.root, padding=10)
        self.root.title("2048 - Two Players")
        self.root.geometry("1600x800")  # Increased width to accommodate two boards
        self.bind_keys()
        self.size = 4
        self.cell_size = 100
        self.grid_padding = 10

        # Create two canvases side by side
        self.canvas1 = Canvas(self.root,
                     width=self.size * self.cell_size + (self.size + 1) * self.grid_padding,
                     height=self.size * self.cell_size + (self.size + 1) * self.grid_padding,
                     bg="#bbada0")
        self.canvas2 = Canvas(self.root,
                     width=self.size * self.cell_size + (self.size + 1) * self.grid_padding,
                     height=self.size * self.cell_size + (self.size + 1) * self.grid_padding,
                     bg="#bbada0")

        self.colors = {
            0: "#cdc1b4", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
            16: "#f59563", 32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72",
            256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"
        }

        # Create frames for each player's score
        self.top_frame1 = Frame(self.root, bg="#bbada0")
        self.top_frame2 = Frame(self.root, bg="#bbada0")
        
        self.top_frame1.pack(side="left", pady=10, padx=20)
        self.top_frame2.pack(side="right", pady=10, padx=20)

        # Score Labels for both players
        self.score_label1 = Label(self.top_frame1, text="P1 Score: " + str(self.game1.players[0].score),
                                font=("Arial", 16), bg="#bbada0", fg="white")
        self.score_label2 = Label(self.top_frame2, text="P2 Score: " + str(self.game2.players[0].score),
                                font=("Arial", 16), bg="#bbada0", fg="white")
        
        self.score_label1.pack(side="left", padx=40)
        self.score_label2.pack(side="left", padx=40)

        # New Game Button (now resets both games)
        self.new_game_button = Button(self.root, text="New Game", font=("Arial", 14, "bold"),
                                    bg="#8f7a66", fg="white", command=self.reset_game)
        self.new_game_button.pack()

        self.canvas1.pack(side="left", padx=20)
        self.canvas2.pack(side="right", padx=20)
        
        self.update_grid()
        self.process_events()

    def reset_game(self):
        """Resets both games and updates the UI."""
        self.game1 = Game2048()
        self.game2 = Game2048()
        self.update_grid()

    def update_grid(self):
        """Update both game boards."""
        self.score_label1.config(text="P1 Score: " + str(self.game1.players[0].score))
        self.score_label2.config(text="P2 Score: " + str(self.game2.players[0].score))
        self.draw_grid(self.canvas1, self.game1)
        self.draw_grid(self.canvas2, self.game2)

    def draw_grid(self, canvas, game):
        """Draws the 4x4 grid with tiles for the specified canvas and game."""
        canvas.delete("all")
        for r in range(self.size):
            for c in range(self.size):
                x0 = c * self.cell_size + (c + 1) * self.grid_padding
                y0 = r * self.cell_size + (r + 1) * self.grid_padding
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size

                tile = game.gameBoard[r][c]

                if tile:
                    color = self.colors.get(tile.point_value, "#3c3a32")
                    canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="#bbada0", width=5)
                    canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=str(tile.point_value),
                                    font=("Arial", 24, "bold"), fill="white" if tile.point_value > 4 else "black")
                else:
                    canvas.create_rectangle(x0, y0, x1, y1, fill=self.colors.get(0, "#3c3a32"), outline="#bbada0", width=5)

    def on_key(self, event):
        key = event.keysym
        input_event1 = None
        input_event2 = None

        # Handle arrow keys for player 1
        match key:
            case "Up":
                input_event1 = UpKey(self.game1)
                input_event2 = UpKey(self.game2)
            case "Down":
                input_event1 = DownKey(self.game1)
                input_event2 = DownKey(self.game2)
            case "Right":
                input_event1 = RightKey(self.game1)
                input_event2 = RightKey(self.game2)
            case "Left":
                input_event1 = LeftKey(self.game1)
                input_event2 = LeftKey(self.game2)
            # Handle WASD for player 2
            case "w":
                input_event2 = UpKey(self.game2)
                input_event1 = UpKey(self.game1)
            case "s":
                input_event2 = DownKey(self.game2)
                input_event1 = DownKey(self.game1)
            case "d":
                input_event2 = RightKey(self.game2)
                input_event1 = RightKey(self.game1)
            case "a":
                input_event2 = LeftKey(self.game2)
                input_event1 = LeftKey(self.game1)

        if input_event1 and input_event2:
            self.game1.events.append(input_event1)
            self.game2.events.append(input_event2)
            self.game1.events.append(CheckWin(self.game1))
            self.game1.events.append(CheckLoss(self.game1))
            self.game2.events.append(CheckWin(self.game2))
            self.game2.events.append(CheckLoss(self.game2))

    def process_events(self):
        if self.game1.events:
            self.game1.handleEvents()
        if self.game2.events:
            self.game2.handleEvents()

        self.update_grid()
        self.root.after(100, self.process_events)

    def bind_keys(self):
        # Bind arrow keys for player 1
        self.root.bind("<Up>", self.on_key)
        self.root.bind("<Down>", self.on_key)
        self.root.bind("<Left>", self.on_key)
        self.root.bind("<Right>", self.on_key)
        
        # Bind WASD for player 2
        self.root.bind("<w>", self.on_key)
        self.root.bind("<s>", self.on_key)
        self.root.bind("<a>", self.on_key)
        self.root.bind("<d>", self.on_key)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = Application()
    gui.run()