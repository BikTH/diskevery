import psutil
import pyudev
import subprocess

class Diske:
    def __init__(self, device):
        self.device = device
        self.liste_partition = []
      
    def partition_is_mounted(self, device):
        # Verifie si une partition est montée (retourne True ou False)
        
        # Liste des partitions déjà montée
        mounted_partitions = psutil.disk_partitions(all=True)

        is_mounted = False

        for parition in mounted_partitions:
            if parition.device == device:
                is_mounted = True
 
                break
        return is_mounted
    
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


        #if serial_number:
        #        print(f"Numéro de série du disque {self.device}: {serial_number}")
        #else:
        #        print(f"Aucun numéro de série trouvé pour le disque {self.device}.")
        
        return serial_number
    

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
        
        try:
            disk_usage = psutil.disk_usage(f"/dev/{self.get_disk_name()}")
            size_free = disk_usage.free
            if size_free is not None:
                print(f"Taille libre du disque /dev/{self.get_disk_name()}: {size_free} octets")
            else:
                print(f"Impossible de trouver la taille du disque {self.get_disk_name()}")

            return size_free
        except (subprocess.CalledProcessError, IndexError, ValueError):
            return None
        
    def get_disk_name(self):
            context = pyudev.Context()
            device = pyudev.Devices.from_device_file(context, self.device)
            return device.sys_name


    def get_liste_partition(self):
        partitions = psutil.disk_partitions(all=False)
        for partition in partitions:
            if partition.device.startswith(self.device):
                self.liste_partition.append(f"Device: {partition.device}, Mountpoint: {partition.mountpoint}, Filesystem: {partition.fstype}")
        
        return self.liste_partition
   
    
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
    

'''disk = Diske('/dev/sda')
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
'''




    
    