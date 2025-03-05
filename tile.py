class Tile:
    def __init__(self, row: int, column: int, point_value: int | None) -> None:
        self.row = row
        self.column = column
        self.point_value = point_value

    def move(self, new_row: int, new_column: int) -> bool:
        pass

    def update(self, new_value: int) -> None:
        pass

    # Should add display method
