"""Low level utilities used to inspect disks present on the system."""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence

try:  # pragma: no cover - optional dependency
    import psutil  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    psutil = None  # type: ignore

try:  # pragma: no cover - optional dependency
    import pyudev  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    pyudev = None  # type: ignore


@dataclass(slots=True)
class RawPartition:
    """Container for raw partition data returned by :command:`lsblk`."""

    name: str
    mountpoint: Optional[str]
    filesystem: Optional[str]


@dataclass(slots=True)
class RawDisk:
    """Container for raw disk data returned by :command:`lsblk`."""

    name: str
    size: Optional[int]
    model: Optional[str]
    serial: Optional[str]
    partitions: List[RawPartition]

    @property
    def device_path(self) -> str:
        return f"/dev/{self.name}"


class SystemDiskInspector:
    """Collect information about the disks available on the host machine."""

    def __init__(
        self,
        lsblk_command: Optional[Sequence[str]] = None,
    ) -> None:
        self._lsblk_command = list(lsblk_command or [
            "lsblk",
            "-J",
            "-b",
            "-o",
            "NAME,TYPE,SIZE,MODEL,SERIAL,MOUNTPOINT,FSTYPE",
        ])

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def list_disks(self) -> List[RawDisk]:
        """Return a list of :class:`RawDisk` detected on the system."""

        blockdevices = self._run_lsblk()
        if blockdevices:
            return [self._build_disk(entry) for entry in blockdevices if entry.get("type") == "disk"]

        # Fall back to a limited view based on psutil when lsblk is unavailable
        return self._fallback_using_psutil()

    def partition_usage(self, mountpoint: Optional[str]) -> Dict[str, Optional[int]]:
        """Return usage metrics for a partition."""

        if not mountpoint:
            return {"total": None, "used": None, "free": None}

        if psutil is not None:
            try:
                usage = psutil.disk_usage(mountpoint)
                return {
                    "total": int(usage.total),
                    "used": int(usage.used),
                    "free": int(usage.free),
                }
            except (FileNotFoundError, PermissionError, OSError):
                pass

        try:
            total, used, free = shutil.disk_usage(mountpoint)
            return {"total": int(total), "used": int(used), "free": int(free)}
        except (FileNotFoundError, PermissionError, OSError):
            return {"total": None, "used": None, "free": None}

    def serial_number(self, device: str, fallback: Optional[str] = None) -> Optional[str]:
        """Retrieve the serial number for the given device using *pyudev* if available."""

        if pyudev is None:
            return fallback

        try:  # pragma: no cover - hardware specific branch
            context = pyudev.Context()
            dev = pyudev.Devices.from_device_file(context, device)
            serial = dev.get("ID_SERIAL_SHORT") or dev.get("ID_SERIAL")
            return serial or fallback
        except Exception:
            return fallback

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _run_lsblk(self) -> List[Dict[str, Any]]:
        try:
            completed = subprocess.run(
                self._lsblk_command,
                check=True,
                capture_output=True,
                text=True,
            )
        except (FileNotFoundError, subprocess.CalledProcessError):
            return []

        try:
            data = json.loads(completed.stdout)
        except json.JSONDecodeError:
            return []

        devices = data.get("blockdevices")
        if isinstance(devices, list):
            return devices
        return []

    def _build_disk(self, entry: Dict[str, Any]) -> RawDisk:
        partitions = []
        for child in entry.get("children", []):
            if child.get("type") != "part":
                continue
            name = child.get("name")
            if not name:
                continue
            partitions.append(
                RawPartition(
                    name=name,
                    mountpoint=self._normalise_mountpoint(child.get("mountpoint")),
                    filesystem=child.get("fstype"),
                )
            )
        size_value = self._to_int(entry.get("size"))
        return RawDisk(
            name=entry.get("name", ""),
            size=size_value,
            model=entry.get("model"),
            serial=entry.get("serial"),
            partitions=partitions,
        )

    def _fallback_using_psutil(self) -> List[RawDisk]:
        if psutil is None:
            return []

        devices: Dict[str, RawDisk] = {}
        for partition in psutil.disk_partitions(all=True):
            disk_name = self._extract_disk_name(partition.device)
            disk = devices.setdefault(
                disk_name,
                RawDisk(
                    name=disk_name.replace("/dev/", ""),
                    size=None,
                    model=None,
                    serial=None,
                    partitions=[],
                ),
            )
            disk.partitions.append(
                RawPartition(
                    name=partition.device.replace("/dev/", ""),
                    mountpoint=self._normalise_mountpoint(partition.mountpoint),
                    filesystem=partition.fstype,
                )
            )
        return list(devices.values())

    @staticmethod
    def _normalise_mountpoint(mountpoint: Optional[str]) -> Optional[str]:
        if not mountpoint:
            return None
        mountpoint = str(mountpoint).strip()
        return mountpoint or None

    @staticmethod
    def _to_int(value: Any) -> Optional[int]:
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    @classmethod
    def _extract_disk_name(cls, device: str) -> str:
        if not device.startswith("/dev/"):
            return device
        return re.sub(r"(p?\d+)$", "", device)
