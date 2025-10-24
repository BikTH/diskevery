"""Application entry point."""
from __future__ import annotations

from app.presentation.cli import render_disk_report
from app.services.disk_service import DiskService


def main() -> None:
    service = DiskService()
    disks = service.list_disks()
    report = render_disk_report(disks)
    print(report)


if __name__ == "__main__":  # pragma: no cover - manual execution guard
    main()
