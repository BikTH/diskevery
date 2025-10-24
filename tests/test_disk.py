import pathlib
import sys
import types
from collections import namedtuple
from unittest.mock import patch


PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


psutil_stub = types.ModuleType("psutil")
psutil_stub.disk_partitions = lambda: []
sys.modules.setdefault("psutil", psutil_stub)

pyudev_stub = types.ModuleType("pyudev")


class _DummyContext:  # pragma: no cover - helper for import compatibility
    pass


class _DummyDevices:  # pragma: no cover - helper for import compatibility
    @staticmethod
    def from_device_file(context, device):
        raise NotImplementedError


pyudev_stub.Context = _DummyContext
pyudev_stub.Devices = _DummyDevices
sys.modules.setdefault("pyudev", pyudev_stub)

from app.models.disk import Diske  # noqa: E402  pylint: disable=wrong-import-position
import psutil  # noqa: E402  pylint: disable=wrong-import-position


Partition = namedtuple("Partition", ["device", "mountpoint", "fstype"])


def test_get_name_returns_mountpoint_for_matching_device():
    disk = Diske("/dev/sda1")
    partitions = [
        Partition(device="/dev/sda0", mountpoint="/mnt/other", fstype="ext4"),
        Partition(device="/dev/sda1", mountpoint="/mnt/data", fstype="ext4"),
    ]

    with patch.object(psutil, "disk_partitions", return_value=partitions):
        assert disk.get_name() == "/mnt/data"


def test_get_name_returns_none_when_no_partition_matches():
    disk = Diske("/dev/sdb1")
    partitions = [
        Partition(device="/dev/sda0", mountpoint="/mnt/other", fstype="ext4"),
        Partition(device="/dev/sda1", mountpoint="/mnt/data", fstype="ext4"),
    ]

    with patch.object(psutil, "disk_partitions", return_value=partitions):
        assert disk.get_name() is None
