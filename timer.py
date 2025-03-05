class Timer:

    def __init__(self) -> None:
        self.tick = 0
        self.tick_rate = 1
        self.is_running = False

    def start(self) -> None:
        self.is_running = True

    def stop(self) -> None:
        self.is_running = False
    
    def reset(self) -> None:
        self.tick = 0

    def update(self) -> None:
        if self.is_running:
            self.tick += self.tick_rate

    def set_TickRate(self, rate: int) -> None:
        self.tick_rate = rate