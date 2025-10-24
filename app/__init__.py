"""diskevery application package."""
from __future__ import annotations

from typing import Any

__all__ = ["main"]


def main(*args: Any, **kwargs: Any) -> Any:
    """Proxy to :func:`app.main.main` without importing it at module load time."""

    from .main import main as _entrypoint

    return _entrypoint(*args, **kwargs)
