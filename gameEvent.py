from typing import Callable

class GameEvent:
    def __init__(self, event_action: Callable[[], None]):
        self.event_action = event_action