import threading
import sys
import time
from typing import Self

MAX_DOTS: int = 20

def send_to_console(string: str) -> None:
    sys.stdout.write(string)
    sys.stdout.flush()

class ThinkingDots:
    def __init__(self, label: str, interval: float = 0.5, dots: int = MAX_DOTS):
        self.label = label
        self.interval = interval
        self.dots = dots

    def __enter__(self) -> Self:
        self.stop_event: threading.Event = self.start_thinking_dots()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.stop_event.set()
        return False

    def start_thinking_dots(self) -> threading.Event:
        stop_event = threading.Event()
        def worker() -> None:
            send_to_console(self.label)
            dots: int = 0
            while not stop_event.is_set():
                send_to_console(".")
                dots += 1
                if dots > self.dots:
                    send_to_console("\n"+self.label)
                    dots = 0
                time.sleep(self.interval)
        
        th: threading.Thread = threading.Thread(target=worker)
        th.start()

        return stop_event