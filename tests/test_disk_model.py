import sys
from collections import namedtuple
from types import SimpleNamespace
from unittest.mock import patch


if "psutil" not in sys.modules:
    sys.modules["psutil"] = SimpleNamespace(
        disk_partitions=lambda: [],
        disk_usage=lambda device: SimpleNamespace(percent=0),
    )

if "pyudev" not in sys.modules:
    sys.modules["pyudev"] = SimpleNamespace(
        Context=lambda: None,
        Devices=SimpleNamespace(
            from_device_file=lambda context, device: SimpleNamespace(
                get=lambda key: None,
                sys_name="",
            )
        ),
    )

from app.models.disk import Diske


Partition = namedtuple("Partition", "device mountpoint fstype opts")


def test_get_name_returns_mountpoint_for_matching_device():
    mock_partitions = [
        Partition(device="/dev/sda1", mountpoint="/", fstype="ext4", opts="rw"),
        Partition(device="/dev/sdb1", mountpoint="/mnt/data", fstype="ext4", opts="rw"),
    ]

    disk = Diske("/dev/sda1")

    with patch("app.models.disk.psutil.disk_partitions", return_value=mock_partitions):
        assert disk.get_name() == "/"


def test_update_liste_partition_replaces_matching_partition():
    mock_partitions = [
        Partition(device="/dev/sda1", mountpoint="/", fstype="ext4", opts="rw"),
        Partition(device="/dev/sdb1", mountpoint="/mnt/data", fstype="ext4", opts="rw"),
    ]

    disk = Diske("/dev/sda1")
    nouvelle_partition = Partition(
        device="/dev/sda1", mountpoint="/mnt/new", fstype="ext4", opts="rw"
    )

    with patch("app.models.disk.psutil.disk_partitions", return_value=mock_partitions):
        updated_partitions = disk.update_liste_partition(nouvelle_partition)

    assert updated_partitions == [nouvelle_partition, mock_partitions[1]]
