import unittest
from mail_triage.core import validate_result, SCHEMA

class CoreTests(unittest.TestCase):
    def test_schema_has_required_fields(self):
        self.assertEqual(set(SCHEMA["required"]), {"category", "priority", "summary", "suggested_reply"})

    def test_valid_result(self):
        value = {"category": "物流配送", "priority": "中", "summary": "包裹未送達", "suggested_reply": "我們將協助查詢。"}
        self.assertEqual(validate_result(value), value)

    def test_invalid_category(self):
        with self.assertRaises(ValueError):
            validate_result({"category": "神秘分類", "priority": "高", "summary": "測試", "suggested_reply": "測試"})

    def test_missing_field(self):
        with self.assertRaises(ValueError):
            validate_result({"category": "其他", "priority": "低", "summary": "測試"})

if __name__ == "__main__":
    unittest.main()
