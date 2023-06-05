from disk import Diske 
#import shutil
import os
import psutil
import subprocess
#import pySMARTl

class DiskManager:

    def __init__(self):
        self.liste_disk = []
        self.disque_actif = None

    def availableDisk(self):
        l=os.system("lsblk -o NAME,SIZE,TYPE,MOUNTPOINT | grep -E '^<device_name>\s|─'")
        print(l)

    def lister_disques(self):

        if len(self.liste_disk) == 0:
            print("Aucun disque géré par Disk Manager ! ")
        
        else:
            print("Liste des disques : ")
            for i, disk in enumerate(self.liste_disk):
                print(i+1," -- (", disk.get_disk_name(), ") Numéro de Série : ", disk.get_serial_number())

    def ajout_disk(self, disk):
        disk=Diske(disk)
        self.liste_disk.append(disk)

    def retirer_disk(self, serialNumber):
        for disk in self.liste_disk:
            if disk.get_serial_number() == serialNumber:
                self.liste_disk.remove(disk)
                break

    def set_active_disk(self, serialNumber):
        
        if len(self.liste_disk) == 0:
            print("Aucun disque géré par Disk Manager ! Ajoutez d'abord un disque !")
            return

        disque_trouve = False
        # Recherche du disque à définir comme actif dans la liste
        for disk in self.liste_disk:
            if disk.get_serial_number() == serialNumber:
                self.disque_actif = disk
                disque_trouve = True
                break

        # Vérification si le disque a été trouvé
        if disque_trouve:
            print("Le disque ({}) a été défini comme disque actif.".format(disk.get_disk_name()))
        else:
            print("Le disque ({}) n'a pas été trouvé.".format(disk.get_disk_name()))

    


    def format_disk(self,device, file_system):


        #verifie si un disk est actif
        if self.disque_actif == None:
            print("veuillez selectionner un disque ")
            return
        
        # Construct the format command
        command = f"mkfs.{file_system} {device}"

        # Execute the command
        try:
            subprocess.run(command, shell=True, check=True)
            print("Disk formatted successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error formatting disk: {e}")

        

    def monter_partition(self, device, mount_point):
        
        #verifie si un disk est actif
        if self.disque_actif == None:
            print("veuillez selectionner un disque ")
            return 
        
        # Monter la partiton (device)
        if self.disque_actif.partition_is_mounted(device): # Vérification si le disque est déjà monté
            print("La partition {} est déjà montée.".format(device))

        else:
            # Instruction pour monter une parition
            os.system(f'mkdir -p {mount_point}')
            os.system(f'mount -o rw {device} {mount_point}')
            print("Le disque {} a été monté avec succès au point de montage {}.".format(device, mount_point))
        

    def demonter_partition(self, device):
        
        #verifie si un disk est actif
        if self.disque_actif == None:
            print("veuillez selectionner un disque ")
            return 
        
        # Instructions pour démonter une parition
        os.system(f'umount {device}')
        print("La partition {} a été démontée avec succès.".format(device))
    

    def extend_partition(self,device, partition_number, end_point):
         #verifie si un disk est actif
         if self.disque_actif == None:
            print("veuillez selectionner un disque ")
            return 
            # Construct the parted command
         command = f"parted -s {device} resizepart {partition_number} {end_point}"
            
            # Execute the command
         try:
                subprocess.run(command, shell=True, check=True)
                print("Partition extended successfully.")
         except subprocess.CalledProcessError as e:
                print(f"Error extending partition: {e}")



    



    def reduce_partition(self,device, new_size):

        #verifie si un disk est actif
        if self.disque_actif == None:
             print("veuillez selectionner un disque ")
             return 


        try:
            # Recreate the file system on the partition
            mkfs_command = f"mkfs.ext4 {device}"
            subprocess.run(mkfs_command, shell=True, check=True)

            # Calculate the new size in blocks
            block_size_command = f"dumpe2fs -h {device} | grep 'Block size'"
            block_count_command = f"dumpe2fs -h {device} | grep 'Block count'"
            block_size = int(subprocess.check_output(block_size_command, shell=True).split()[2])
            block_count = int(subprocess.check_output(block_count_command, shell=True).split()[2])
            new_size_value = int(new_size.rstrip("MB"))  # Remove "MB" suffix and convert to integer
            new_size_blocks = new_size_value * 1024 * 1024 // block_size  # Convert size to blocks

            # Resize the file system within the partition
            resize2fs_command = f"resize2fs {device} {new_size_blocks}"
            subprocess.run(resize2fs_command, shell=True, check=True)

            print("Partition reduced successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error reducing partition: {e}")



    def delete_partition(self,device, partition_number):
        #verifie si un disk est actif
        if self.disque_actif == None:
             print("veuillez selectionner un disque ")
             return 
            
        # Construct the parted command
        command = f"parted -s {device} rm {partition_number}"
        
        # Execute the command
        try:
            subprocess.run(command, shell=True, check=True)
            print("Partition deleted successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error deleting partition: {e}")



    def create_partition(self,device, partition_type, file_system_type, start, end):

        #verifie si un disk est actif
            if self.disque_actif == None:
                print("veuillez selectionner un disque ")
                return 
            
        # Construct the parted command
            command = f"parted -s {device} mklabel gpt mkpart {partition_type} {file_system_type} {start} {end}"
            
            # Execute the command
            try:
                subprocess.run(command, shell=True, check=True)
                print("Partition created successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Error creating partition: {e}")

    

''' def data_recovery(self, device, destination_path):
        # Recherche du disque dans la liste des disques
        for disk in self.liste_disk:
            if disk.device == device:
                try:
                    # Récupération des partitions du disque
                    partitions = disk.liste_partition

                    # Récupération des données de chaque partition
                    for partition in partitions:
                        partition_path = partition.mountpoint
                        recovered_files_path = destination_path + '/' + partition.nom

                        # Copie des fichiers de la partition vers le chemin de destination
                        shutil.copytree(partition_path, recovered_files_path)

                    print("Récupération de données du disque {} terminée avec succès.".format(device))
                except Exception as e:
                    print("Une erreur s'est produite lors de la récupération des données du disque {}: {}".format(device, str(e)))

                break

        else:
            print("Le disque {} n'a pas été trouvé.".format(device))
'''