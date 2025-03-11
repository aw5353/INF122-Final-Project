from engine.game import Game
from engine.player import Player
from engine.gameRuleEvent import GameRuleEvent
from engine.playerInputEvent import PlayerInputEvent
from engine.tile import Tile
from random import Random
from enum import Enum

BOARD_HEIGHT = 4
BOARD_WIDTH = 4

class GameState(Enum):
    RUNNING = 0
    WIN = 1
    LOST = 2
    IDLE = 3

class Game2048(Game):
    def __init__(self, height=BOARD_HEIGHT, width=BOARD_WIDTH):
        board = Game.generateBoard(height, width)
        player = Player("", "", 0)
        self.height = height
        self.width = width
        self.state: GameState = GameState.IDLE
        super().__init__(list([player]), board, None)

    def check_boundary(self, x, y):
        return 0 <= x < self.height and 0 <= y < self.width
    
    def move_tiles(self, direction):
        def slide(row):
            new_row = [tile for tile in row if tile]
            for i in range(len(new_row) - 1):
                if new_row[i] == new_row[i + 1]:
                    new_row[i] *= 2
                    new_row[i + 1] = 0
            new_row = [tile for tile in new_row if tile]
            return new_row + [0] * (self.width - len(new_row))

        rotated = False
        if direction == "Up":
            self.gameBoard = [list(col) for col in zip(*self.gameBoard)]
            rotated = True
        elif direction == "Down":
            self.gameBoard = [list(col[::-1]) for col in zip(*self.gameBoard)] 
            rotated = True
        elif direction == "Right":
            self.gameBoard = [row[::-1] for row in self.gameBoard]

        for i in range(self.height):
            self.gameBoard[i] = slide(self.gameBoard[i])

        if rotated:
            if direction == "Up":
                self.gameBoard = [list(col) for col in zip(*self.gameBoard)]
            else:
                self.gameBoard = [list(col[::-1]) for col in zip(*self.gameBoard)]

        elif direction == "Right":
            self.gameBoard = [row[::-1] for row in self.gameBoard]

        self.events.append(SpawnTile(self))
    
    def update(self):
        pass  # Implement game logic update
    
    def process_input(self, command):
        self.move_tiles(command)
        self.spawn_tile()

    def render(self):
        pass

if __name__ == "__main__":
    game = Game2048()
    game.render()

class UpKey(PlayerInputEvent):
    def __init__(self, game: Game2048):
        super().__init__("Up", lambda: game.move_tiles("Up"))
class DownKey(PlayerInputEvent):
    def __init__(self, game: Game2048):
        super().__init__("Down", lambda: game.move_tiles("Down"))

class RightKey(PlayerInputEvent):
    def __init__(self, game: Game2048):
        super().__init__("Right", lambda: game.move_tiles("Right"))

class LeftKey(PlayerInputEvent):
    def __init__(self, game: Game2048):
        super().__init__("Left", lambda: game.move_tiles("Left"))
        
class SpawnTile(GameRuleEvent):
    def init(self, game: Game2048):
        super().init("Spawn New Tile", lambda: self.spawn_tile())
        self.game = game

    def spawn_tile(self):
        empty_tiles = [(r, c) for r in range(game.height) for c in range(game.width) if not game.board[r][c]]
        if empty_tiles:
            r, c = Random.choice(empty_tiles)
            new_value = 2 if Random.random() < 0.9 else 4
            self.game.board[r][c] = Tile(r,c, new_value)
        
class CheckWin(GameRuleEvent):
    def __init__(self, game: Game2048):
        super().__init__("Check Win", lambda: self.check_win(game))

    def check_win(self, game: Game2048):
        if any(tile and tile.value == 2048 for row in game.gameBoard for tile in row):
            game.state = GameState.WIN

class CheckLoss(GameRuleEvent):
    def __init__(self, game: Game2048):
        super().__init__("Check Loss", lambda: self.check_loss(game))

    def check_loss(self, game: Game2048):
        if all(game.gameBoard[r][c] for r in range(game.height) for c in range(game.width)):
            game.state = GameState.LOST