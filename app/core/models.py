"""Domain models describing disks and their partitions."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(slots=True)
class PartitionInfo:
    """Representation of a partition that belongs to a disk."""

    device: str
    mountpoint: Optional[str]
    filesystem: Optional[str]
    total_bytes: Optional[int] = None
    used_bytes: Optional[int] = None
    free_bytes: Optional[int] = None

    def usage_ratio(self) -> Optional[float]:
        """Return the usage ratio expressed between 0 and 1."""

        if self.total_bytes in (None, 0) or self.used_bytes is None:
            return None
        return self.used_bytes / float(self.total_bytes)


@dataclass(slots=True)
class DiskInfo:
    """Description of a physical disk present on the host machine."""

    device: str
    model: Optional[str]
    serial_number: Optional[str]
    size_bytes: Optional[int]
    health: Optional[str]
    partitions: List[PartitionInfo] = field(default_factory=list)

    def add_partition(self, partition: PartitionInfo) -> None:
        self.partitions.append(partition)

    def total_used_bytes(self) -> Optional[int]:
        usable = [p.used_bytes for p in self.partitions if p.used_bytes is not None]
        if not usable:
            return None
        return int(sum(usable))

    def total_bytes(self) -> Optional[int]:
        totals = [p.total_bytes for p in self.partitions if p.total_bytes is not None]
        if totals:
            return int(sum(totals))
        return self.size_bytes

    def usage_ratio(self) -> Optional[float]:
        total = self.total_bytes()
        used = self.total_used_bytes()
        if total in (None, 0) or used is None:
            return None
        return used / float(total)
