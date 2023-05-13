from PIL import Image, ImageTk
from customtkinter import  *

# _________main_view.py_________
#Variables utilisé dans le fichier frames_class.py

app_name = 'Diskevery'
app_ico = 'assets/diskevery.ico'
default_theme = 'black'
app_font = 'ubuntu'



# _________frames_class.py_________
#Variables utilisé dans le fichier frames_class.py

#Menu_Frame
menu_bar_style = { #on définit le style de notre menu ici
    "bg": "#2b2b2b", # couleur de fond #242424
    "fg": "white", # couleur de texte
    "activebackground": "grey", # couleur de fond quand le menu est actif
    "activeforeground": "white", # couleur de texte quand le menu est actif
    "bd": 0, # épaisseur de la bordure du menu
    "cursor": 'hand2', # forme du curseur quand il survole le menu
    "font": (app_font, 12), # police et taille du texte du menu
    "relief": 'flat' # style de la bordure du menu (flat, groove, raised, ridge, solid, or sunken)
}

menu_style = {
    "bg": "#2b2b2b", # couleur de fond
    "fg": "white", # couleur de texte
    "activebackground": "grey", # couleur de fond quand la commande est active
    "activeforeground": "white", # couleur de texte quand la commande est active
    "bd": 0, # épaisseur de la bordure du menu
    "cursor": 'hand2', # forme du curseur quand il survole le menu
    "font": (app_font, 10), # police et taille du texte du menu
    "relief": 'flat', # style de la bordure du menu (flat, groove, raised, ridge, solid, or sunken)
    "borderwidth": 15 #largeur du menu
}

#Disque_Frame
disk_ico_light= "disk_frame_ico/disk_light.png" #icone pour un disque
disk_ico_dark = "disk_frame_ico/disk_dark2.png" #icone pour un disque
usb_ico_light = "disk_frame_ico/usb_light.png" #icone pour une clef usb
usb_ico_dark = "disk_frame_ico/usb_dark2.png" #icone pour une clef usb
cd_ico_light = "disk_frame_ico/cd_light.png" #icone pour un lecteur de cd
cd_ico_dark = "disk_frame_ico/cd_dark2.png" #icone pour une clef usb

disque_label_style = {
    "corner_radius": 8,
    "text_color": ("black", "white"),
    "font": (app_font, 10),
    "anchor": "e",
    "compound": "left",
    "justify": "left",
    "padx": 5,
    "pady": 5,
}

#Outils_Frame
formater_ico = ["outils/formater_dark.png", "outils/formater_dark2.png", "outils/formater_light.png"]
create_partition_ico = ["outils/create_partition_dark.png", "outils/create_partition_dark2.png", "outils/create_partition_light.png"]
delete_partition_ico = ["outils/delete_partition_dark.png", "outils/delete_partition_dark2.png", "outils/delete_partition_light.png"]
mount_ico = ["outils/mont_dark.png", "outils/mont_dark2.png", "outils/mont_light.png"]
recovery_ico = ["outils/recovery_dark.png", "outils/recovery_dark2.png", "outils/recovery_light.png"]
resize_ico = ["outils/resize_dark.png", "outils/resize_dark2.png", "outils/resize_light.png"]

#Default_Contenu_Frame
default_ico = "default.png" #image pour la page par défaut


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

def return_ctk_image(dark_image: str, width: int, height: int, light_image: str = None):
    """Cette fonction retourne un élément image compatible avec tkinter et Ctkinter
    Args:
        dark_image (str): le chemin vers l'image adapté au thème sombre partant du répertoire assets/images/
        light.png_image (str): le chemin vers l'image adapté au thème clair partant du répertoire assets/images/
        width (int): la largeur qu'on veut attribuer à l'image en px
        height (int): la hauteur qu'on veut associer à l'image en px
    Returns:
        objet CTkImage: l'image en un format compréhensible par tkinter et ctkinter
    """
    if light_image == None :
        return CTkImage(light_image=Image.open(assets_images(dark_image)), dark_image=Image.open(assets_images(dark_image)),size=(width, height))
    else: 
        return CTkImage(light_image=Image.open(assets_images(light_image)), dark_image=Image.open(assets_images(dark_image)),size=(width, height))
