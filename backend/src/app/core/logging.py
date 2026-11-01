"""Logging setup."""

from __future__ import annotations

import logging
import sys


def configure_logging(level: str = "INFO") -> None:
    """Configure root logging once, to stdout, in a single structured line format."""
    if logging.getLogger().handlers:
        logging.getLogger().setLevel(level.upper())
        return
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s", "%Y-%m-%dT%H:%M:%S%z"))
    root = logging.getLogger()
    root.setLevel(level.upper())
    root.addHandler(handler)
