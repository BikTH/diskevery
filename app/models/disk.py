import psutil
import pyudev
import subprocess

class Diske:
    def __init__(self, device):
        self.device = device
      
      

    def get_model(self):
        command = ["lsblk", "-o", "MODEL"]
        output = subprocess.check_output(command).decode("utf-8")

        models = output.splitlines()[1:]  # Ignorer la première ligne (en-têtes)
        for model in models:
            if model.strip():  # Ignorer les lignes vides
                return model.strip()
        return "Modèle non trouvé pour ce disque"
    
    def get_serial_number(self):
        context = pyudev.Context()
        device = pyudev.Devices.from_device_file(context, self.device)
        serial_number = device.get('ID_SERIAL_SHORT')


        if serial_number:
                print(f"Numéro de série du disque {self.device}: {serial_number}")
        else:
                print(f"Aucun numéro de série trouvé pour le disque {self.device}.")
        return serial_number
    
    def get_name(self):
        partitions = psutil.disk_partitions()
        for partition in partitions:
            if partition.device == self.name:
                return partition.mountpoint
        return None

    def get_total_size(self):
        try:
            command = f"lsblk -b -dn -o SIZE {self.device} | awk 'NR==1 {{print $1}}'"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            total_size = int(result.stdout.strip())
            if total_size:
             print(f"La taille totale du disque {self.device} est : {total_size} octets")

            return total_size
        except Exception as e:
            print(f"Erreur lors de l'obtention de la taille totale du disque : {e}")
            return None
    
    def get_used_size(self):
        try:
            command = f"df -B1 --output=used {self.device} | awk 'NR==2 {{print $1}}'"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            used_size = int(result.stdout.strip())
            if used_size:
             print(f"La taille utilisée du disque {self.device} est : {used_size} octets")

            return used_size
        except Exception as e:
            print(f"Erreur lors de l'obtention de la taille utilisée du disque : {e}")
            return None
        

    
    
    def get_size_free(self):
        command = ['df', '-B1', self.device]
        try:
            output = subprocess.check_output(command).decode().strip().split('\n')[1]
            size_free = int(output.split()[3])
            if size_free is not None:
                print(f"Taille libre du disque {self.device}: {size_free} octets")
            else:
                print(f"Impossible de trouver le disque {self.device}")

            return size_free
        except (subprocess.CalledProcessError, IndexError, ValueError):
            return None
        
    def get_disk_name(self):
            context = pyudev.Context()
            device = pyudev.Devices.from_device_file(context, self.device)
            return device.sys_name


    

    def get_liste_partition(self):
        partitions = psutil.disk_partitions()
        liste_partition = []
        for partition in partitions:
            if partition.device == self.device:
                liste_partition.append(f"Device: {partition.device}, Mountpoint: {partition.mountpoint}, Filesystem: {partition.fstype}")
        
        return liste_partition
   
    def update_liste_partition(disque, nouvelle_partition):
        partitions = psutil.disk_partitions()
        updated_partitions = []
        for partition in partitions:
            if partition.device == disque:
                updated_partitions.append(nouvelle_partition)
            else:
                updated_partitions.append(partition)
        return updated_partitions
    
    def get_health(self):
        try:
            disk_usage = psutil.disk_usage(self.device)
            if disk_usage.percent >= 90:
                return "Critique"
            elif disk_usage.percent >= 70:
                return "Élevé"
            elif disk_usage.percent >= 50:
                return "Moyen"
            else:
                return "Bon"
        except Exception as e:
            return str(e)
        

disk = Diske('/dev/sda6')
total_size = disk.get_total_size()
used_size = disk.get_used_size()
size_free = disk.get_size_free()

disk_name = disk.get_disk_name()
print("Nom du disque : ", disk_name)
health_state = disk.get_health()
serial = disk.get_serial_number()
disk_partitions = disk.get_liste_partition() 


disk_model = disk.get_model() 
print(f"le model du disque est :{disk_model}\n")

print(f" partitionné :{disk_partitions}\n")
print(f"État de santé du disque:  {health_state}\n")




    
    