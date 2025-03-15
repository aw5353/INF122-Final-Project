import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

import random
from engine.board import Board
from engine.game import Game
from engine.timer import Timer

class ColumnsGame(Game):
  def __init__(self, rows=14, columns=6):
    super().__init__(gameBoard=Board(rows, columns, default_point_value=0), timer=Timer())
    self.current_piece = self.generate_piece()
    self.piece_col = random.randrange(6)
    self.piece_row = 0
    self.running = True
    self.score = 0

  def generate_piece(self):
    colors = ['R', 'Y', 'G', 'F' , 'L']
    return [random.choice(colors) for _ in range(3)]

  def move_piece(self, direction):
    new_col = self.piece_col + direction
    if 0 <= new_col < len(self.gameBoard.grid[0]) and not self._is_piece_block(direction):
      self.piece_col = new_col

  def _is_piece_block(self, direction: int) -> bool:
    for i in range(3):
      new_col = self.piece_col + direction
      if self.piece_row-i >= 0 and self.gameBoard.getBoardState()[self.piece_row-i][new_col].point_value != 0:
        return True
    return False

  def drop_piece(self):
    if self.piece_row + 2 < (len(self.gameBoard.grid)+1) and \
      self.gameBoard.getBoardState()[self.piece_row+1][self.piece_col].point_value == 0:
        self.piece_row += 1
    else:
        self.lock_piece()

  def rotate_piece(self):
    self.current_piece = self.current_piece[-1:] + self.current_piece[:-1]

  def check_matches(self):
    board = self.gameBoard.getBoardState()
    rows, cols = len(board), len(board[0])
    matched_positions = set()

    for r in range(rows):
      for c in range(cols - 2):
        if board[r][c].point_value != 0 and board[r][c].point_value == board[r][c+1].point_value == board[r][c+2].point_value:
          matched_positions.update([(r, c), (r, c+1), (r, c+2)])

    for c in range(cols):
      for r in range(rows - 2):
        if board[r][c].point_value != 0 and board[r][c].point_value == board[r+1][c].point_value == board[r+2][c].point_value:
          matched_positions.update([(r, c), (r+1, c), (r+2, c)])

    self.score += len(matched_positions) // 3 * 10

    for r, c in matched_positions:
      board[r][c].point_value = 0

    for c in range(cols):
      non_zero_values = [board[r][c].point_value for r in range(rows) if board[r][c].point_value != 0]
      for r in range(rows - len(non_zero_values)):
        board[r][c].point_value = 0
      for r, value in enumerate(non_zero_values, start=rows - len(non_zero_values)):
        board[r][c].point_value = value

  def lock_piece(self):
    for i in range(3):
      if self.piece_row - i >= 0:
        self.gameBoard.getBoardState()[self.piece_row - i][self.piece_col].point_value = self.current_piece[i]
    self.check_matches()
    self.current_piece = self.generate_piece()
    self.piece_row = 0
    self.piece_col = random.randrange(6)

  def play(self):
    while self.running:
      self.drop_piece()
      self.updateDisplay()

      user_input = input("Move (a/d), Rotate (w), Quit (q): ").lower()
      if user_input == 'a':
        self.move_piece(-1)
      elif user_input == 'd':
        self.move_piece(1)
      elif user_input == 'w':
        self.rotate_piece()
      elif user_input == 'q':
        print("Game Over!")
        self.running = False

  def updateDisplay(self):
    display_grid = [[tile.point_value if tile.point_value != 0 else '_' for tile in row] for row in self.gameBoard.grid]
    
    for i in range(3):
      if 0 <= self.piece_row - i < len(display_grid):
        display_grid[self.piece_row - i][self.piece_col] = self.current_piece[i]

    print("Score:", self.score)

    for row in display_grid:
      print(row)
    print("\n")

if __name__ == "__main__":
  game = ColumnsGame()
  game.play()
