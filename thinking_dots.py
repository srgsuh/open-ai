import threading
import sys
import time
from typing import Self

MAX_DOTS: int = 20

class ThinkingDots:
    def __init__(self, label: str, interval: float = 0.5, dots: int = MAX_DOTS):
        self.label = label
        self.interval = interval
        self.dots = dots

    def __enter__(self) -> Self:
        self.stop_event = self.__start_thinking_dots()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.stop_event.set()
        return False

    def __start_thinking_dots(self) -> threading.Event:
        stop_event = threading.Event()
        def worker() -> None:
            sys.stdout.write(self.label)
            sys.stdout.flush()
            dots = 0
            while not stop_event.is_set():
                sys.stdout.write(".")
                sys.stdout.flush()
                dots += 1
                if dots > self.dots:
                    sys.stdout.write("\n"+self.label)
                    sys.stdout.flush()
                    dots = 0
                time.sleep(self.interval)
        
        th: threading.Thread = threading.Thread(target=worker)
        th.start()

        return stop_event