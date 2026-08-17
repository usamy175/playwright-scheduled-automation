from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Protocol

from .config import Settings


class LoggerLike(Protocol):
    def info(self, message: str, *args: object) -> None: ...
    def exception(self, message: str, *args: object) -> None: ...
    def error(self, message: str, *args: object) -> None: ...


@dataclass(frozen=True)
class AutomationResult:
    success: bool
    started_at: datetime
    finished_at: datetime
    message: str
    screenshot_path: Path | None = None


def build_error_screenshot_path(settings: Settings, started_at: datetime) -> Path:
    timestamp = started_at.strftime("%Y%m%d-%H%M%S")
    return settings.error_screenshot_dir / f"automation-error-{timestamp}.png"


def run_once(settings: Settings, logger: LoggerLike) -> AutomationResult:
    from playwright.sync_api import sync_playwright

    started_at = datetime.now()
    logger.info("Automation run started at %s.", started_at.isoformat(timespec="seconds"))

    browser = None
    page = None
    screenshot_path: Path | None = None

    with sync_playwright() as playwright:
        try:
            launch_options = {"headless": settings.headless}
            if settings.browser_channel:
                launch_options["channel"] = settings.browser_channel

            browser = playwright.chromium.launch(**launch_options)
            page = browser.new_page()

            page.goto(settings.app_base_url, wait_until="networkidle")
            page.get_by_test_id("username").fill(settings.username)
            page.get_by_test_id("password").fill(settings.password)
            page.get_by_test_id("login-button").click()
            page.wait_for_url(f"{settings.app_base_url}/dashboard", timeout=5_000)

            page.get_by_test_id("run-action-button").click()
            page.get_by_test_id("success-message").wait_for(timeout=5_000)

            finished_at = datetime.now()
            message = "Demo action completed successfully."
            logger.info(
                "Automation run finished at %s with result: success.",
                finished_at.isoformat(timespec="seconds"),
            )
            return AutomationResult(True, started_at, finished_at, message)

        except Exception as exc:
            finished_at = datetime.now()
            screenshot_path = build_error_screenshot_path(settings, started_at)
            settings.error_screenshot_dir.mkdir(parents=True, exist_ok=True)

            if page is not None:
                try:
                    page.screenshot(path=str(screenshot_path), full_page=True)
                    logger.error("Error screenshot saved at %s.", screenshot_path)
                except Exception as screenshot_error:
                    logger.error("Could not save error screenshot: %s.", screenshot_error)
                    screenshot_path = None

            logger.exception("Automation run failed: %s", exc)
            return AutomationResult(False, started_at, finished_at, str(exc), screenshot_path)

        finally:
            if browser is not None:
                browser.close()
                logger.info("Browser closed.")
