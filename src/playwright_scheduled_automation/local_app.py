from __future__ import annotations

import html
import secrets
import threading
from http import HTTPStatus
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import parse_qs

from .config import Settings


SESSION_COOKIE_NAME = "demo_session"


LOGIN_PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Automation Demo Login</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 0; min-height: 100vh; display: grid; place-items: center; background: #f4f7fb; color: #172033; }
    main { width: min(92vw, 420px); background: white; padding: 32px; border: 1px solid #d9e2ef; border-radius: 8px; box-shadow: 0 16px 40px rgba(23, 32, 51, 0.08); }
    label { display: block; margin-top: 16px; font-weight: 700; }
    input { width: 100%; box-sizing: border-box; padding: 12px; margin-top: 6px; border: 1px solid #b7c3d5; border-radius: 6px; }
    button { width: 100%; margin-top: 22px; padding: 12px; border: 0; border-radius: 6px; background: #1f6feb; color: white; font-weight: 700; cursor: pointer; }
    .error { color: #a31515; margin-top: 16px; }
  </style>
</head>
<body>
  <main>
    <h1>Local Automation Demo</h1>
    <p>Use the demo credentials from your environment configuration.</p>
    __ERROR__
    <form method="post" action="/login">
      <label for="username">Username</label>
      <input id="username" name="username" data-testid="username" autocomplete="username" required>
      <label for="password">Password</label>
      <input id="password" name="password" data-testid="password" type="password" autocomplete="current-password" required>
      <button data-testid="login-button" type="submit">Sign in</button>
    </form>
  </main>
</body>
</html>
"""


def dashboard_page(action_count: int, confirmation: str = "") -> str:
    message = (
        f'<p data-testid="success-message" class="success">{html.escape(confirmation)}</p>'
        if confirmation
        else ""
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Automation Demo Dashboard</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 0; min-height: 100vh; background: #eef4f8; color: #172033; }}
    main {{ width: min(92vw, 760px); margin: 48px auto; background: white; padding: 32px; border: 1px solid #d9e2ef; border-radius: 8px; }}
    button {{ padding: 12px 18px; border: 0; border-radius: 6px; background: #147d64; color: white; font-weight: 700; cursor: pointer; }}
    .success {{ padding: 12px 14px; background: #e6f6ee; border: 1px solid #8fd0ad; border-radius: 6px; color: #14623d; }}
    .metric {{ display: inline-block; margin: 18px 0; padding: 10px 12px; background: #f5f7fb; border-radius: 6px; }}
  </style>
</head>
<body>
  <main>
    <h1>Authenticated Area</h1>
    <p>This local page simulates a private dashboard for a safe automation demo.</p>
    <span class="metric" data-testid="action-count">Actions completed: {action_count}</span>
    {message}
    <form method="post" action="/action">
      <button data-testid="run-action-button" type="submit">Run demo action</button>
    </form>
  </main>
</body>
</html>
"""


class DemoAutomationHandler(BaseHTTPRequestHandler):
    server: "DemoAutomationServer"

    def do_GET(self) -> None:
        if self.path in {"/", "/login"}:
            self.respond_html(LOGIN_PAGE.replace("__ERROR__", ""))
            return
        if self.path == "/dashboard":
            if not self.is_authenticated():
                self.redirect("/login")
                return
            self.respond_html(dashboard_page(self.server.action_count))
            return
        if self.path == "/health":
            self.respond_text('{"status":"ok"}', content_type="application/json")
            return
        self.send_error(HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length).decode("utf-8")
        form = parse_qs(body)

        if self.path == "/login":
            username = form.get("username", [""])[0]
            password = form.get("password", [""])[0]
            if username == self.server.settings.username and password == self.server.settings.password:
                token = secrets.token_urlsafe(24)
                with self.server.state_lock:
                    self.server.sessions.add(token)
                self.send_response(HTTPStatus.SEE_OTHER)
                self.send_header("Location", "/dashboard")
                self.send_header("Set-Cookie", f"{SESSION_COOKIE_NAME}={token}; HttpOnly; SameSite=Lax; Path=/")
                self.end_headers()
                return
            error = '<p class="error" data-testid="login-error">Invalid demo credentials.</p>'
            self.respond_html(LOGIN_PAGE.replace("__ERROR__", error), status=HTTPStatus.UNAUTHORIZED)
            return

        if self.path == "/action":
            if not self.is_authenticated():
                self.redirect("/login")
                return
            with self.server.state_lock:
                self.server.action_count += 1
                count = self.server.action_count
            self.respond_html(dashboard_page(count, "Demo action completed successfully."))
            return

        self.send_error(HTTPStatus.NOT_FOUND)

    def is_authenticated(self) -> bool:
        cookie_header = self.headers.get("Cookie", "")
        cookie = SimpleCookie(cookie_header)
        session = cookie.get(SESSION_COOKIE_NAME)
        if session is None:
            return False
        with self.server.state_lock:
            return session.value in self.server.sessions

    def redirect(self, location: str) -> None:
        self.send_response(HTTPStatus.SEE_OTHER)
        self.send_header("Location", location)
        self.end_headers()

    def respond_html(self, body: str, status: HTTPStatus = HTTPStatus.OK) -> None:
        self.respond_text(body, status=status, content_type="text/html; charset=utf-8")

    def respond_text(
        self,
        body: str,
        status: HTTPStatus = HTTPStatus.OK,
        content_type: str = "text/plain; charset=utf-8",
    ) -> None:
        encoded = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format: str, *args: Any) -> None:
        return


class DemoAutomationServer(ThreadingHTTPServer):
    def __init__(self, server_address: tuple[str, int], settings: Settings):
        super().__init__(server_address, DemoAutomationHandler)
        self.settings = settings
        self.sessions: set[str] = set()
        self.action_count = 0
        self.state_lock = threading.Lock()


def create_server(settings: Settings, port: int | None = None) -> DemoAutomationServer:
    return DemoAutomationServer((settings.app_host, port if port is not None else settings.app_port), settings)


def start_server_in_thread(settings: Settings, port: int | None = None) -> DemoAutomationServer:
    server = create_server(settings, port=port)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server
