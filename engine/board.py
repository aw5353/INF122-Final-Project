from engine.tile import Tile


class Board:
    def __init__(self, rows: int, columns: int, default_point_value: int) -> None:
        self.grid = [[Tile(i, j, default_point_value) for i in range(columns)] for j in range(rows)]

    def getBoardState(self) -> list[list[Tile]]:
        return self.grid

    def displayBoard(self):
        for row in self.grid:
            print([tile.point_value for tile in row])
