from __future__ import annotations

import time

from .automation import AutomationResult, run_once
from .config import Settings
from .automation import LoggerLike


def run_scheduler(settings: Settings, logger: LoggerLike, max_runs: int | None = None) -> list[AutomationResult]:
    results: list[AutomationResult] = []
    run_number = 0

    while max_runs is None or run_number < max_runs:
        run_number += 1
        logger.info("Scheduled run %s started.", run_number)
        results.append(run_once(settings, logger))

        if max_runs is not None and run_number >= max_runs:
            break

        logger.info("Waiting %s seconds before the next run.", settings.run_interval_seconds)
        time.sleep(settings.run_interval_seconds)

    return results
