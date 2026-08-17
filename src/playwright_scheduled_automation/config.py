from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def load_dotenv(path: Path | None = None) -> None:
    env_path = path or PROJECT_ROOT / ".env"
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def read_bool(name: str, default: bool) -> bool:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default
    return raw_value.strip().lower() in {"1", "true", "yes", "y", "on"}


def read_int(name: str, default: int) -> int:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default
    try:
        value = int(raw_value)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer.") from exc
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero.")
    return value


@dataclass(frozen=True)
class Settings:
    app_host: str = "127.0.0.1"
    app_port: int = 8000
    app_base_url: str = "http://127.0.0.1:8000"
    username: str = "demo_user"
    password: str = "demo_password"
    run_interval_seconds: int = 10
    headless: bool = True
    browser_channel: str | None = None
    log_file: Path = PROJECT_ROOT / "logs" / "automation.log"
    error_screenshot_dir: Path = PROJECT_ROOT / "screenshots" / "errors"


def get_settings(env_path: Path | None = None) -> Settings:
    load_dotenv(env_path)
    app_host = os.getenv("APP_HOST", "127.0.0.1")
    app_port = read_int("APP_PORT", 8000)
    app_base_url = os.getenv("APP_BASE_URL", f"http://{app_host}:{app_port}")
    browser_channel = os.getenv("BROWSER_CHANNEL", "").strip() or None

    return Settings(
        app_host=app_host,
        app_port=app_port,
        app_base_url=app_base_url.rstrip("/"),
        username=os.getenv("APP_USERNAME", "demo_user"),
        password=os.getenv("APP_PASSWORD", "demo_password"),
        run_interval_seconds=read_int("RUN_INTERVAL_SECONDS", 10),
        headless=read_bool("HEADLESS", True),
        browser_channel=browser_channel,
    )
