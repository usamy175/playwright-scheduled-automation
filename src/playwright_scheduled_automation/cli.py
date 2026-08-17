from __future__ import annotations

import argparse
import sys

from .automation import run_once
from .config import get_settings
from .local_app import create_server, start_server_in_thread
from .logging_config import configure_logging
from .scheduler import run_scheduler


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Safe local demo of scheduled Playwright automation.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("serve", help="Start the local demo web application.")
    subparsers.add_parser("run-once", help="Run the automation once against APP_BASE_URL.")

    schedule_parser = subparsers.add_parser("schedule", help="Run the automation repeatedly.")
    schedule_parser.add_argument("--max-runs", type=int, default=None, help="Stop after a fixed number of runs.")

    demo_parser = subparsers.add_parser("demo", help="Start the local app and run the automation once.")
    demo_parser.add_argument("--max-runs", type=int, default=1, help="Number of automation runs to execute.")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    settings = get_settings()
    logger = configure_logging(settings.log_file)

    if args.command == "serve":
        server = create_server(settings)
        logger.info("Local demo app running at http://%s:%s", settings.app_host, settings.app_port)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            logger.info("Local demo app stopped by user.")
        finally:
            server.server_close()
        return 0

    if args.command == "run-once":
        result = run_once(settings, logger)
        return 0 if result.success else 1

    if args.command == "schedule":
        run_scheduler(settings, logger, max_runs=args.max_runs)
        return 0

    if args.command == "demo":
        server = start_server_in_thread(settings)
        host, port = server.server_address
        logger.info("Local demo app running at http://%s:%s", host, port)
        try:
            results = run_scheduler(settings, logger, max_runs=args.max_runs)
            return 0 if all(result.success for result in results) else 1
        finally:
            server.shutdown()
            server.server_close()
            logger.info("Local demo app stopped.")

    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
