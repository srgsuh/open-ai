import re

def extract_json(source_str: str, words: list[str] = []) -> str:
    look_ahead: str = ""
    if words:
        look_ahead = "".join([f"(?=.*{re.escape(word)})" for word in words])
    
    pattern: str = rf"{look_ahead}(\{{.*\}})"
    match: re.Match | None = re.search(pattern=pattern, string = source_str, flags=re.DOTALL)

    json_str: str = ""
    if match:
        json_str = match.group(1)

    return json_str

if __name__ == "__main__":
    string: str = """
    Hi there this is JSON: {
        "role": "player",
        "content": {
            "foo": "value"}
            }
    }
    some text there too.
    """

    print(extract_json(string, ["content", "role"]))