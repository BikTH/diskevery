import os
import psutil
import subprocess

from disk import Diske

class Partition(Diske):
        def __init__(self, device):
            
            super().__init__(device)

       
        def get_mountpoint(device):
            partitions = psutil.disk_partitions()
            for partition in partitions:
                if partition.device == device:
                    return partition.mountpoint
            return None




        def get_status(disk):
            partitions = os.statvfs(disk)
            flags = partitions.f_flag

            if flags & os.ST_RDONLY:
                return "Read-Only"
            else:
                return "Read/Write"
                    
        disk = "/dev/sda4"  # Remplacez par le nom du disque souhaité
        mountpoint = get_mountpoint(disk)
        if mountpoint:
            print(f"Point de montage de la partition {disk}: {mountpoint}")
        else:
            print("Impossible de trouver le point de montage.")

        status = get_status(disk)
        if status:
            print(f"Statut de la partition {disk}: {status}")
        else:
            print("Impossible de récupérer le statut de la partition.")
