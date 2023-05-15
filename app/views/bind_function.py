import tkinter as btk
import customtkinter as bctk

#____________________________________________________________________Hover 
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
        event (_type_): <leave> l'événement d'arret du survol du label
        on (CtkLabel Object): le label qu'on quitte
    """
    on.configure(fg_color='transparent')


#____________________________________________________________________Clique
def select_disk_label(event, on):
    """Cette fonction affiche le contenu relatif au disque sélectionné
    Args:
        event (): l'événement, ici un clique sur le label du disque
        on (Main_windows object): l'objet représentant la fenêtre principale de notre application
    """
    on.grid_contenu()


