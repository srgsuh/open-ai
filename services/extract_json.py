import re
import json
from logs import logger

def extract_json_str(source_str: str, words: list[str] = []) -> str:
    look_ahead = "".join([f"(?=.*{re.escape(word)})" for word in words])
    pattern: str = rf"{look_ahead}\{{.*\}}"
    match: re.Match | None = re.search(pattern=pattern, string = source_str, flags=re.DOTALL)
    logger.debug(f"extract_json_str. match={'' if match is None else match.group(0)}")
    return "" if match is None else match.group(0)

def extract_json_strings(source_str: str, words: list[str] = []) -> list[str]:
    json_strings: list[str] = []
    start_index: int = 0
    brace_level: int = 0
    for idx, s in enumerate(source_str):
        if s == '{':
            if brace_level == 0:
                start_index = idx
            brace_level += 1
        elif s == '}':
            brace_level -= 1
            if brace_level == 0:
                json_str: str = source_str[start_index:idx + 1]
                if (all(w in json_str for w in words)):
                    json_strings.append(json_str) 

    return json_strings

def extract_json(source_str: str, words: list[str] = []) -> dict | None:
    result: dict | None = None
    json_strings: list[str] = extract_json_strings(source_str, words)
    logger.debug(f"extract_json. strings={json_strings}")
    if json_strings:
        try:
            result = json.loads(json_strings[0])
        except Exception as e:
            logger.debug(f"JSON error: {str(e)}")

    return result