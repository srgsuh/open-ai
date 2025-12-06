import re

def extract_json(source_str: str, words: list[str] = []) -> str:
    look_ahead = "".join([f"(?=.*{re.escape(word)})" for word in words])
    pattern: str = rf"{look_ahead}\{{.*\}}"
    match: re.Match | None = re.search(pattern=pattern, string = source_str, flags=re.DOTALL)

    return "" if match is None else match.group(0)

if __name__ == "__main__":
    string: str = """
    JSON example: {
        "role": "user",
        "content": {
            "key": "value"}
            }
    }
    some text there too.
    """

    print(extract_json(string, ["content", "key", "role"]))