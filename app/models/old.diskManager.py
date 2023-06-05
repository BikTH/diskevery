from disk import Diske 
#import shutil
import os
import psutil
import subprocess
#import pySMART

class DiskManager:

    def __init__(self):
        self.liste_disk = []
        self.disque_actif = None

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

    

    def format_disk(self):

        #verifie si un disk est actif
        if self.disque_actif == None:
            print("veuillez selectionner un disque ")
            return 
        
        # Verifie si on est root
        if os.geteuid() != 0:
            print(" Vous devez etre Root !")
            exit(1)

        # Instructions de Formatage du disk

        # Démonte toutes les partitions du disques 
        os.system(f'umount {self.disque_actif}*')

        # Cré une nouvelle table de parition
        os.system(f'echo -e "o\nn\np\n1\n\n\nw" | fdisk {self.disque_actif}')

        # Formater le disque entier avec un système de fichiers
        os.system(f'mkfs.ext4 {self.disque_actif}1')

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
        

    def etendre_partition(self, device, size):
        partition_trouvee = False

        # Recherche de la partition à étendre dans la liste des disques
        for disk in self.liste_disk:
            for partition in disk.get_liste_partition():
                if partition.get_device() == device:
                    # Vérification si la partition est montée
                    if partition.is_mounted():
                        print("La partition {} est montée. Veuillez la démonter avant de l'étendre.".format(device))
                    else:
                        # Étendre la partition
                        partition.extend(size)
                        print("La partition {} a été étendue avec succès de {}.".format(device, size))
                    partition_trouvee = True
                    break

            if partition_trouvee:
                break

        # Vérification si la partition a été trouvée
        if not partition_trouvee:
            print("La partition {} n'a pas été trouvée.".format(device))

    def reduire_partition(self, device, size):
        partition_trouvee = False

        # Recherche de la partition à réduire dans la liste des disques
        for disk in self.liste_disk:
            for partition in disk.get_liste_partition():
                if partition.get_device() == device:
                    # Vérification si la partition est montée
                    if partition.is_mounted():
                        print("La partition {} est montée. Veuillez la démonter avant de la réduire.".format(device))
                    else:
                        # Réduire la partition
                        partition.reduce(size)
                        print("La partition {} a été réduite avec succès de {}.".format(device, size))
                    partition_trouvee = True
                    break

            if partition_trouvee:
                break

        # Vérification si la partition a été trouvée
        if not partition_trouvee:
            print("La partition {} n'a pas été trouvée.".format(device))

    def supprimer_partition(self, device):
        partition_trouvee = False

        # Recherche de la partition à supprimer dans la liste des disques
        for disk in self.liste_disk:
            for partition in disk.get_liste_partition():
                if partition.get_device() == device:
                    # Vérification si la partition est montée
                    if partition.is_mounted():
                        print("La partition {} est montée. Veuillez la démonter avant de la supprimer.".format(device))
                    else:
                        # Exécution de la commande fdisk pour supprimer la partition
                        command = "echo 'd\nw\n' | fdisk {}".format(device)
                        os.system(command)
                        print("La partition {} a été supprimée avec succès.".format(device))
                    partition_trouvee = True
                    break

            if partition_trouvee:
                break

        # Vérification si la partition a été trouvée
        if not partition_trouvee:
            print("La partition {} n'a pas été trouvée.".format(device))

     

    def create_partition(self,device, partition_size):

        #verifie si un disk est actif
        if self.disque_actif == None:
            print("veuillez selectionner un disque ")
            return 
        
        # Verifie s'il ya assez d'espace
        if partition_size > self.disque_actif.get_size_free():
            print("Impossible de créer ! Espace insuffisant ")
            return 
         # Créer la nouvelle partition
        subprocess.run(f'sudo parted {device} mkpart primary ext4 0% {partition_size}')
        print("La partition a été créée avec succès sur le disque {}.".format(device))

                

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