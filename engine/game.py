from engine.player import Player
from collections import deque

class Game:
  def __init__(self, playerList = [], gameBoard = None, timer = None):
    self.players = playerList
    self.gameBoard = gameBoard
    self.timer = timer
    self.events = deque([])

  def generateBoard(rows: int, cols: int):
      gameBoard = [[None for _ in range(cols)] for _ in range(rows)]
      return gameBoard

  def addPlayer(self, newPlayer: Player) -> None:
      self.players.append(newPlayer)
      
  def handleEvents(self) -> None:
      event = self.events.popleft()
      event.execute()