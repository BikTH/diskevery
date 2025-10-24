"""High level service assembling disk information for the application."""
from __future__ import annotations

from typing import Iterable, List, Optional

from app.core.models import DiskInfo, PartitionInfo
from app.infrastructure.system_inspector import RawDisk, RawPartition, SystemDiskInspector


class DiskService:
    """Entry point used by the presentation layer to query disks."""

    def __init__(self, inspector: Optional[SystemDiskInspector] = None) -> None:
        self._inspector = inspector or SystemDiskInspector()

    def list_disks(self) -> List[DiskInfo]:
        raw_disks = self._inspector.list_disks()
        return [self._build_disk(raw) for raw in raw_disks]

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------
    def _build_disk(self, raw_disk: RawDisk) -> DiskInfo:
        partitions = [self._build_partition(part) for part in raw_disk.partitions]
        health = self._compute_health(partitions, raw_disk.size)
        serial = self._inspector.serial_number(raw_disk.device_path, raw_disk.serial)
        disk = DiskInfo(
            device=raw_disk.device_path,
            model=self._normalise_string(raw_disk.model),
            serial_number=self._normalise_string(serial),
            size_bytes=raw_disk.size,
            health=health,
            partitions=[],
        )
        for partition in partitions:
            disk.add_partition(partition)
        return disk

    def _build_partition(self, raw_partition: RawPartition) -> PartitionInfo:
        metrics = self._inspector.partition_usage(raw_partition.mountpoint)
        return PartitionInfo(
            device=f"/dev/{raw_partition.name}",
            mountpoint=raw_partition.mountpoint,
            filesystem=self._normalise_string(raw_partition.filesystem),
            total_bytes=metrics.get("total"),
            used_bytes=metrics.get("used"),
            free_bytes=metrics.get("free"),
        )

    def _compute_health(
        self,
        partitions: Iterable[PartitionInfo],
        disk_size: Optional[int],
    ) -> Optional[str]:
        totals = []
        used = []
        for partition in partitions:
            if partition.total_bytes is not None:
                totals.append(partition.total_bytes)
            if partition.used_bytes is not None:
                used.append(partition.used_bytes)

        total_capacity = sum(totals) if totals else disk_size
        used_capacity = sum(used) if used else None

        if total_capacity in (None, 0) or used_capacity is None:
            return None

        usage_ratio = used_capacity / float(total_capacity)
        if usage_ratio >= 0.9:
            return "critical"
        if usage_ratio >= 0.75:
            return "warning"
        return "healthy"

    @staticmethod
    def _normalise_string(value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        stripped = value.strip()
        return stripped or None
