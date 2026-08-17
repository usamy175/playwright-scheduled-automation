from __future__ import annotations

from http.cookiejar import CookieJar
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, Request, build_opener, urlopen

from playwright_scheduled_automation.config import Settings
from playwright_scheduled_automation.local_app import start_server_in_thread


def test_health_endpoint_returns_ok() -> None:
    settings = Settings(app_port=0)
    server = start_server_in_thread(settings, port=0)
    host, port = server.server_address

    try:
        with urlopen(f"http://{host}:{port}/health", timeout=2) as response:
            assert response.status == 200
            assert response.read().decode("utf-8") == '{"status":"ok"}'
    finally:
        server.shutdown()
        server.server_close()


def test_login_and_action_flow() -> None:
    settings = Settings(app_port=0, username="demo_user", password="demo_password")
    server = start_server_in_thread(settings, port=0)
    host, port = server.server_address
    base_url = f"http://{host}:{port}"
    opener = build_opener(HTTPCookieProcessor(CookieJar()))

    try:
        login_request = Request(
            f"{base_url}/login",
            data=urlencode({"username": "demo_user", "password": "demo_password"}).encode("utf-8"),
            method="POST",
        )
        opener.open(login_request, timeout=2)

        action_request = Request(f"{base_url}/action", data=b"", method="POST")
        with opener.open(action_request, timeout=2) as response:
            body = response.read().decode("utf-8")

        assert response.status == 200
        assert "Demo action completed successfully." in body
        assert "Actions completed: 1" in body
    finally:
        server.shutdown()
        server.server_close()
