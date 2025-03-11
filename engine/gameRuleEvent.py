from engine.gameEvent import GameEvent
from typing import Callable

class GameRuleEvent(GameEvent):
    def __init__(self, rule: str, event_action: Callable[[], None]):
        super().__init__(event_action=event_action)
        self.rule = rule