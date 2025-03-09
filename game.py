from player import Player

class Game:
  def __init__(self, playerList = [], gameBoard = None, timer = None):
    self.players = playerList
    self.gameBoard = gameBoard
    self.timer = timer

  def generateBoard(self, rows: int, cols: int):
      self.gameBoard = [[None for _ in range(cols)] for _ in range(rows)]
      return self.gameBoard

  def addPlayer(self, newPlayer: Player) -> None:
      self.players.append(newPlayer)

  def updateDisplay(self) -> None:
      print("Updating game display...")

  def handleEvents(self, event) -> None:
      print(f"Handling event: {event}")