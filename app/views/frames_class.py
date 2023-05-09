import tkinter as tk
from customtkinter import CTkFrame as Frame
from customtkinter import *
from PIL import Image, ImageTk
from general_information import *


class Main_frame(Frame):
    """_summary_ 
    cette classe nous servira de base pour toute nos frames
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(corner_radius=0)
        self.parent = parent


#____________________________________________________________________________
class MenuFrame(tk.Menu):
    """Cette classe va nous permettre de créer un objet menu qui nous permettra 
    d'ajouter une barre de menu à notre fenêtre
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        self.config(**menu_bar_style) #on définit les configurations de style de notre barre de menu
        
        #On crée les menus de notre barre de menu
        
        #Diskevery
        self.app_menu = tk.Menu(self, tearoff = 0) 
        self.app_menu.config(**menu_style) #on définit les configurations de style pour ce menu
        self.app_menu.add_command(label='Agrandir') 
        self.app_menu.add_command(label='Rétrécir')
        #Vue
        self.view_menu = tk.Menu(self, tearoff= 0)
        self.view_menu.config(**menu_style) #on définit les configurations de style pour ce menu
        self.view_menu.add_command(label='Theme') 
        self.view_menu.add_command(label='Langue') 
        #Aide
        self.help_menu = tk.Menu(self, tearoff= 0)
        self.help_menu.config(**menu_style) #on définit les configurations de style pour ce menu
        self.help_menu.add_command(label='Aide') 
        self.help_menu.add_command(label='A propos') 
    
    
    def add_menu_bar(self):
        """Cette méthode va permettre d'ajouter notre barre de menu à notre fenêtre
        """
        self.parent.config(menu = self)
        self.add_cascade(label=app_name, menu=self.app_menu)
        self.add_cascade(label='Vue', menu=self.view_menu)
        self.add_cascade(label='Aide', menu=self.help_menu)


#____________________________________________________________________________
class Disque_liste(Main_frame):
    """Cette classe nous permetrra de lister les différents disque 
    """
    def __init__(self, parent):
        super().__init__(parent)


#____________________________________________________________________________
class DisqueFrame(Main_frame):
    """Cette classe nous permetrra de lister les différents disque 
    """
    def __init__(self, parent):
        super().__init__(parent)
        
        titre =  CTkLabel(self.parent, text="CTkLabel", )


#____________________________________________________________________________
class OutilsFrame(Main_frame):
    def __init__(self, parent):
        super().__init__(parent)


#____________________________________________________________________________
class DefaultContenuFrame(Main_frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="transparent")


#____________________________________________________________________________
class ContenuFrame(Main_frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="transparent")


#____________________________________________________________________________
class TachesFrame(Main_frame):
    def __init__(self, parent):
        super().__init__(parent)