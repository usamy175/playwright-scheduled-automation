from __future__ import annotations

import os
from pathlib import Path

import pytest

from playwright_scheduled_automation.config import get_settings, read_bool, read_int


def test_read_bool_accepts_common_true_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HEADLESS", "yes")
    assert read_bool("HEADLESS", False) is True


def test_read_int_rejects_non_positive_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RUN_INTERVAL_SECONDS", "0")
    with pytest.raises(ValueError, match="greater than zero"):
        read_int("RUN_INTERVAL_SECONDS", 10)


def test_get_settings_loads_env_file_without_overwriting_existing_env(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            [
                "APP_HOST=127.0.0.1",
                "APP_PORT=9001",
                "APP_USERNAME=file_user",
                "APP_PASSWORD=file_password",
                "RUN_INTERVAL_SECONDS=15",
                "HEADLESS=false",
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.setenv("APP_USERNAME", "env_user")
    for key in ["APP_PORT", "APP_PASSWORD", "RUN_INTERVAL_SECONDS", "HEADLESS", "APP_BASE_URL", "BROWSER_CHANNEL"]:
        monkeypatch.delenv(key, raising=False)

    settings = get_settings(env_file)

    assert settings.app_port == 9001
    assert settings.username == "env_user"
    assert settings.password == "file_password"
    assert settings.run_interval_seconds == 15
    assert settings.headless is False

    os.environ.pop("APP_HOST", None)
