from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from requests import Session, Response, RequestException

URL: str = "https://www.sergeysuhoverhov.space/api/hello"
DEFAULT_REQUEST_COUNT: int = 128
MAX_WORKERS: int = 4

def one_request(session: Session, url: str, request_id) -> tuple[int, int]:
    try:
        response: Response = session.get(url, timeout=5)
        return request_id, response.status_code
    except RequestException as re:
        return request_id, -1

def spam_requests(request_count: int = DEFAULT_REQUEST_COUNT) -> None:
    with Session() as session:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_tasks = [
                executor.submit(one_request, session, URL, req_no)
                for req_no in range(1, request_count + 1)
            ]
            for made_tasks in as_completed(future_tasks):
                id, status = made_tasks.result()
                print(f'Request id={id} is finished with the status code={status}')

if __name__ == "__main__":
    NUM_OF_MINUTES = 5
    TIMES_PER_MINUTE = 5
    time_to_sleep = 60.0/TIMES_PER_MINUTE
    for minute in range(NUM_OF_MINUTES):
        for episode in range(TIMES_PER_MINUTE):
            print(f"Minute {minute}, episode {episode}. Run session:")
            spam_requests(32)
            print(f"Into a sleep mode for {time_to_sleep} seconds...")
            time.sleep(time_to_sleep)
    spam_requests()