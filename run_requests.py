from concurrent.futures import ThreadPoolExecutor, as_completed
from requests import Session, Response, RequestException

URL: str = "https://sergeysuhoverhov.space/api/hello"
REQUEST_COUNT: int = 64
MAX_WORKERS: int = 4

def one_request(session: Session, url: str, request_id) -> tuple[int, int]:
    try:
        response: Response = session.get(url, timeout=5)
        return request_id, response.status_code
    except RequestException as re:
        return request_id, -1

def spam_requests() -> None:
    with Session() as session:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_tasks = [
                executor.submit(one_request, session, URL, req_no)
                for req_no in range(1, REQUEST_COUNT + 1)
            ]
            for made_tasks in as_completed(future_tasks):
                id, status = made_tasks.result()
                print(f'Request id={id} is finished with the status code={status}')

if __name__ == "__main__":
    spam_requests()