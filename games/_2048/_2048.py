from engine.game import Game
from engine.player import Player
from engine.gameRuleEvent import GameRuleEvent
from engine.playerInputEvent import PlayerInputEvent
from engine.tile import Tile
from random import choice, random
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
        self.events.append(SpawnTile(self))

    def check_boundary(self, x, y):
        return 0 <= x < self.height and 0 <= y < self.width
    
    def move_tiles(self, direction):
        def get_value(cell):
            return cell.point_value if hasattr(cell, "point_value") else cell

        def board_snapshot(board):
            return [[get_value(cell) for cell in row] for row in board]

        def slide(row):
            new_row = [cell for cell in row if cell]
            i = 0
            while i < len(new_row) - 1:
                if get_value(new_row[i]) == get_value(new_row[i + 1]):
                    combined_value = get_value(new_row[i]) * 2
                    if hasattr(new_row[i], "point_value"):
                        new_row[i].point_value = combined_value
                    else:
                        new_row[i] = combined_value
                    new_row[i + 1] = 0
                    self.players[0].score += combined_value
                    i += 2
                else:
                    i += 1
            new_row = [cell for cell in new_row if get_value(cell) != 0]
            return new_row + [0] * (self.width - len(new_row))

        old_snapshot = board_snapshot(self.gameBoard)

        if direction == "Left":
            for i in range(self.height):
                self.gameBoard[i] = slide(self.gameBoard[i])
        elif direction == "Right":
            for i in range(self.height):
                self.gameBoard[i] = slide(self.gameBoard[i][::-1])[::-1]
        elif direction == "Up":
            self.gameBoard = [list(col) for col in zip(*self.gameBoard)]
            for i in range(self.width):
                self.gameBoard[i] = slide(self.gameBoard[i])
            self.gameBoard = [list(col) for col in zip(*self.gameBoard)]
        elif direction == "Down":
            self.gameBoard = [list(col) for col in zip(*self.gameBoard)]
            for i in range(self.width):
                self.gameBoard[i] = slide(self.gameBoard[i][::-1])[::-1]
            self.gameBoard = [list(col) for col in zip(*self.gameBoard)]

        new_snapshot = board_snapshot(self.gameBoard)

        if new_snapshot != old_snapshot:
            self.events.append(SpawnTile(self))
    
    def process_input(self, command):
        self.move_tiles(command)
        self.spawn_tile()

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
    def __init__(self, game: Game2048):
        super().__init__("Spawn New Tile", lambda: self.spawn_tile())
        self.game = game

    def spawn_tile(self):
        empty_tiles = [(r, c) for r in range(self.game.height) for c in range(self.game.width) if not self.game.gameBoard[r][c]]
        if empty_tiles:
            r, c = choice(empty_tiles)
            new_value = 2 if random() < 0.9 else 4
            self.game.gameBoard[r][c] = Tile(r,c, new_value)
        
class CheckWin(GameRuleEvent):
    def __init__(self, game: Game2048):
        super().__init__("Check Win", lambda: self.check_win(game))

    def check_win(self, game: Game2048):
        if any(tile and tile.point_value == 2048 for row in game.gameBoard for tile in row):
            game.state = GameState.WIN
            print("You Won!")

class CheckLoss(GameRuleEvent):
    def __init__(self, game: Game2048):
        super().__init__("Check Loss", lambda: self.check_loss(game))

    def check_loss(self, game: Game2048):
        if all(game.gameBoard[r][c] for r in range(game.height) for c in range(game.width)):
            game.state = GameState.LOST
            print("You Lost!")