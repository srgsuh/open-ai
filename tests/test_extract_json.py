import unittest as ut
from services.extract_json import extract_json

class TestExtractJSON(ut.TestCase):
    string_JSON_ok: str = """
    JSON example: {
        "role": "user",
        "content": {
            "key": "value"
        }
    }
    some text there too.
    """
    string_JSON_no_brace: str = """
    JSON example: {
        "role": "user",
        "content": {
            "key": "value"
        }
    some text there too.
    """
    def test_extract_json_positive(self) -> None:
        d1: dict = extract_json(self.string_JSON_ok) or {}
        d2: dict = extract_json(self.string_JSON_ok, ["role"]) or {}
        d3: dict = extract_json(self.string_JSON_ok, ["content", "key", "role"]) or {}
        self.assertTrue(d1["role"] == "user")
        self.assertTrue(d1["content"]["key"] == "value")
        self.assertEqual(d1, d2)
        self.assertEqual(d2, d3)
        
    
    def test_extract_json_negative(self) -> None:
        self.assertIsNone(extract_json(self.string_JSON_ok, ["roles"]))
        self.assertIsNone(extract_json(self.string_JSON_no_brace))

if __name__ == "__main__":
    ut.main()