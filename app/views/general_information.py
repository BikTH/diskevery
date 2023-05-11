from PIL import Image, ImageTk
from customtkinter import  *

# _________main_view.py_________
#Variables utilisé dans le fichier frames_class.py

app_name = 'Diskevery'
app_ico = 'assets/diskevery.ico'
default_theme = 'black'



# _________frames_class.py_________
#Variables utilisé dans le fichier frames_class.py

#Menu_Frame
menu_bar_style = { #on définit le style de notre menu ici
    "bg": "black", # couleur de fond
    "fg": "white", # couleur de texte
    "activebackground": "grey", # couleur de fond quand le menu est actif
    "activeforeground": "white", # couleur de texte quand le menu est actif
}

#Disque_Frame
disk_ico = "disk_frame_ico/disk.ico"
usb_ico = "disk_frame_ico/usb.ico"
cd_ico = "disk_frame_ico/cd.ico"


menu_style = {
    "bg": "black", # couleur de fond
    "fg": "white", # couleur de texte
    "activebackground": "grey", # couleur de fond quand la commande est active
    "activeforeground": "white", # couleur de texte quand la commande est active
}


# _________Helpers_________
# Fonctions servant à faire diverses tâches

def assets_images(path_to_file: str):
    """Cette fonction retourne le chemin vers le fichier contenu assets/images
    Args:
        path_to_file (str): le chemin vers le fichier en partant du dossier assets/images
                            exemple: "image_outils/outil.png" 
    Returns:
        str: chemin vers le fichier
    """
    return "assets/images/"+path_to_file 

def return_ctk_image(image: str, width: int, height: int ):
    """Cette fonction retourne un élément image compatible avec tkinter et Ctkinter
    Args:
        image (str): le chemin vers l'image partant du répertoire assets/images/
        width (int): la largeur qu'on veut attribuer à l'image en px
        height (int): la hauteur qu'on veut associer à l'image en px
    Returns:
        objet CTkImage: l'image en un format compréhensible par tkinter et ctkinter
    """
    return CTkImage(Image.open(assets_images(image)), size=(width, height))