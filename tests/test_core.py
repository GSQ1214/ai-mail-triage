import unittest
from unittest.mock import patch
from io import BytesIO
import json
from mail_triage.core import validate_result, SCHEMA, classify

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


    def test_non_string_category_rejected(self):
        with self.assertRaises(ValueError):
            validate_result({"category": ["退換貨"], "priority": "中", "summary": "測試", "suggested_reply": "測試"})

    def test_empty_email_rejected(self):
        with self.assertRaises(ValueError):
            classify("   ")

    def test_non_local_host_rejected(self):
        with self.assertRaises(ValueError):
            classify("查詢物流", host="https://example.com")

    def test_request_uses_schema_and_delivery_guidance(self):
        response = {"message": {"content": json.dumps({"category": "物流配送", "priority": "中", "summary": "包裹尚未送達", "suggested_reply": "請提供訂單編號以協助查詢。"})}}
        class MockResponse(BytesIO):
            def __enter__(self):
                return self
            def __exit__(self, *args):
                self.close()
        with patch("mail_triage.core.urlopen", return_value=MockResponse(json.dumps(response).encode())) as mocked:
            actual = classify("商品未收到，請查詢配送")
        self.assertEqual(actual["category"], "物流配送")
        request = mocked.call_args.args[0]
        payload = json.loads(request.data)
        self.assertEqual(payload["format"], SCHEMA)
        self.assertEqual(payload["options"]["temperature"], 0)
        self.assertIn("未收到貨", payload["messages"][0]["content"])

if __name__ == "__main__":
    unittest.main()
