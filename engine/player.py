class Player:
  def __init__(self, username: str, password: str, score: int = 0):
    self.username = username
    self.password = password
    self.score = score

  def get_username(self) -> str:
    return self.username

  def update_score(self, new_score: int) -> None:
    self.score = new_score