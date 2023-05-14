import tkinter as btk
import customtkinter as bctk


#____________________________________________________________________Hover sur les labels
def hover_on(event, on):
    """Cette fonction change le bg d'un label lorsqu'il est survolé
    Args:
        event (_type_): <Enter> l'événement de survol du label
        on (CtkLabel Object): le label qu'on survole
    """
    on.configure(fg_color='#242424')
    print(on.titre)

def hover_off(event, on):
    """Cette fonction restaure le bg d'un label une fois qu'on la quitté
    Args:
        event (_type_): <leave> l'événement d'arret du survol du label
        on (CtkLabel Object): le label qu'on quitte
    """
    on.configure(fg_color='transparent') 
    print(on.position)