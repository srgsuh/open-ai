import threading
import sys
import time

MAX_DOTS: int = 20

def start_thinking_dots(label: str, interval: float = 0.5) -> threading.Event:
    stop_event = threading.Event()

    def worker() -> None:
        sys.stdout.write(label)
        sys.stdout.flush()
        dots = 0
        while not stop_event.is_set():
            sys.stdout.write(".")
            sys.stdout.flush()
            dots += 1
            if dots > MAX_DOTS:
                sys.stdout.write("\n"+label)
                sys.stdout.flush()
                dots = 0
            time.sleep(interval)
    
    th: threading.Thread = threading.Thread(target=worker)
    th.start()

    return stop_event