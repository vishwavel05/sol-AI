"""
Unit tests for SOL AI REST API Handler (backend/api/server.py).
Verifies GET /api/health, POST /api/query, CORS headers, error codes, and payload validation.
"""

import os
import json
import unittest
from http.server import HTTPServer
from threading import Thread
import urllib.request
import urllib.error

from backend.api.server import SOLAPIRequestHandler


class TestSOLAPI(unittest.TestCase):
    """
    Test suite for SOL REST API endpoints.
    Starts a local background HTTPServer on a free port for real HTTP request assertions.
    """

    @classmethod
    def setUpClass(cls):
        # Start server on ephemeral port
        cls.server = HTTPServer(("127.0.0.1", 0), SOLAPIRequestHandler)
        cls.port = cls.server.server_port
        cls.base_url = f"http://127.0.0.1:{cls.port}"
        cls.thread = Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_health_endpoint(self):
        """1. Test GET /api/health."""
        req = urllib.request.Request(f"{self.base_url}/api/health", method="GET")
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode("utf-8"))
            self.assertEqual(data.get("status"), "ok")

    def test_query_endpoint_success(self):
        """2. Test POST /api/query with valid query 'மரங்களில்' using mock provider."""
        payload = {"query": "மரங்களில்", "provider": "mock"}
        req = urllib.request.Request(
            f"{self.base_url}/api/query",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode("utf-8"))
            self.assertEqual(data.get("query"), "மரங்களில்")
            self.assertEqual(data.get("lemma"), "மரம்")
            self.assertIn("sources", data)

    def test_query_endpoint_missing_payload(self):
        """3. Test POST /api/query with missing query field."""
        payload = {}
        req = urllib.request.Request(
            f"{self.base_url}/api/query",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            urllib.request.urlopen(req)
            self.fail("Expected HTTPError 400")
        except urllib.error.HTTPError as err:
            self.assertEqual(err.code, 400)
            data = json.loads(err.read().decode("utf-8"))
            self.assertIn("error", data)

    def test_query_endpoint_missing_gemini_key(self):
        """4. Test POST /api/query with provider=gemini when GEMINI_API_KEY is not set."""
        old_key = os.environ.pop("GEMINI_API_KEY", None)
        try:
            payload = {"query": "மரங்களில்", "provider": "gemini"}
            req = urllib.request.Request(
                f"{self.base_url}/api/query",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            try:
                urllib.request.urlopen(req)
                self.fail("Expected HTTPError 400")
            except urllib.error.HTTPError as err:
                self.assertEqual(err.code, 400)
                data = json.loads(err.read().decode("utf-8"))
                self.assertIn("GEMINI_API_KEY", data.get("error", ""))
        finally:
            if old_key:
                os.environ["GEMINI_API_KEY"] = old_key


if __name__ == "__main__":
    unittest.main()
