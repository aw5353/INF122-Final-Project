from engine.gameEvent import GameEvent
from typing import Callable

class PlayerInputEvent(GameEvent):
    def __init__(self, player_input: str, event_action: Callable[[], None]):
        super().__init__(event_action=event_action)
        self.player_input = player_input