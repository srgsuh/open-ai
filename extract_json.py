import re
import json

def extract_json_str(source_str: str, words: list[str] = []) -> str:
    look_ahead = "".join([f"(?=.*{re.escape(word)})" for word in words])
    pattern: str = rf"{look_ahead}\{{.*\}}"
    match: re.Match | None = re.search(pattern=pattern, string = source_str, flags=re.DOTALL)

    return "" if match is None else match.group(0)

def extract_json(source_str: str, words: list[str] = []) -> dict | None:
    result: dict | None = None
    try:
        result = json.loads(extract_json_str(source_str, words))
    except Exception:
        pass

    return result