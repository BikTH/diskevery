"""Command line presentation helpers."""
from __future__ import annotations

from typing import Iterable

from app.core.models import DiskInfo, PartitionInfo


def render_disk_report(disks: Iterable[DiskInfo]) -> str:
    """Generate a string representation of the disks list."""

    lines: list[str] = []
    for disk in disks:
        lines.extend(_render_single_disk(disk))

    if not lines:
        return "Aucun disque détecté."

    return "\n".join(lines)


def _render_single_disk(disk: DiskInfo) -> list[str]:
    lines = [f"Disque {disk.device}"]
    if disk.model:
        lines.append(f"  Modèle        : {disk.model}")
    if disk.serial_number:
        lines.append(f"  Numéro de série : {disk.serial_number}")
    if disk.size_bytes is not None:
        size_gb = disk.size_bytes / (1024 ** 3)
        lines.append(f"  Capacité totale : {size_gb:.2f} Gio")
    if disk.health:
        lines.append(f"  Santé          : {disk.health}")

    if not disk.partitions:
        lines.append("  Aucune partition détectée.")
        return lines

    lines.append("  Partitions :")
    for partition in disk.partitions:
        lines.extend(_render_partition(partition))

    return lines


def _render_partition(partition: PartitionInfo) -> list[str]:
    lines = [f"    - {partition.device}"]
    if partition.mountpoint:
        lines.append(f"        Point de montage : {partition.mountpoint}")
    if partition.filesystem:
        lines.append(f"        Système de fichiers : {partition.filesystem}")
    if partition.total_bytes is not None:
        total_gb = partition.total_bytes / (1024 ** 3)
        lines.append(f"        Taille : {total_gb:.2f} Gio")
    if partition.used_bytes is not None and partition.total_bytes:
        ratio = partition.usage_ratio()
        if ratio is not None:
            lines.append(f"        Utilisation : {ratio * 100:.1f}%")
    return lines
