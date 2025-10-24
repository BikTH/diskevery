import tkinter as btk
import customtkinter as bctk

#____________________________________________________________________HOVER (<Enter> & <Leave>)
def hover_on(event, on):
    """Cette fonction change le bg d'un label lorsqu'il est survolé
    Args:
        event (_type_): <Enter> l'événement de survol du label
        on (CtkLabel Object): le label qu'on survole
    """
    on.configure(fg_color='#242424')

def hover_off(event, on):
    """Cette fonction restaure le bg d'un label une fois qu'on la quitté
    Args:
        event (): <leave> l'événement d'arret du survol du label
        on (CtkLabel Object): le label qu'on quitte
    """
    on.configure(fg_color='transparent')

def hover_disable(event, on):
    """Cette fonction va nous permettre de stoper le hover sur l'objet on
    Args:
        event (_type_): <leave> l'événement d'arret du survol du label
        on (CTkLabel Object): le label qu'on quitte
    """
    on.configure(fg_color='#242424')


#____________________________________________________________________CLIQUE GAUCHE (<Button-1>)
def select_disk_label(event, on, main, parent):
    """Cette fonction affiche le contenu relatif au disque sélectionné
    Args:
        event (): l'événement, ici un clique sur le label du disque
        on (CTkLabel Object): le label qu'on sélectionne 
        main (Main_windows object): l'objet représentant la fenêtre principale de notre application
        parent (CTkFrame object): la frame qui contient notre disque
    """
    main.grid_contenu() #on affiche le contenu du disque sélectionné
    if parent.active_disk != None : #s'il y a un disque actif
        parent.active_disk.configure(fg_color='transparent') #on fait passer son BG sur transparent (BG des disk_label inactifs)
        parent.active_disk.bind("<Leave>", lambda event, on=parent.active_disk : hover_off(event, on)) #on lui réattribue un bind hover normal
    parent.active_disk = on #on déclare le disk_label sélectionné comme étant celui actif
    parent.active_disk.bind("<Leave>",lambda event, self=on : hover_disable(event, self)) #on déactive son bind hover 

#ces fonctions gére l'ouverture des fenêtres associées aux outils de la frame outils
def select_formater_dialog(event, on):
    on.open_formater_dialog()

def select_resize_dialog(event, on):
    on.open_formater_dialog()

def select_mont_dialog(event, on):
    on.open_mont_dialog()

def select_creation_dialog(event, on):
    on.open_creation_dialog()

def select_delete_dialog(event, on):
    on.open_delete_dialog()

def select_recovery_dialog(event, on):
    on.open_recovery_dialog(event)
