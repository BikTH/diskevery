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


class MenuFrame(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        self.config(**menu_bar_style) #on définit les configurations de style de notre barre de menu
        
        #On crée les menus de notre barre de menu
        self.app_menu = tk.Menu(self, tearoff = 0) #le menu de l'application
        self.app_menu.config(**menu_style) #on définit les configurations de style pour ce menu
        self.app_menu.add_command(label='Agrandir') 
        self.app_menu.add_command(label='Rétrécir') 
        
        self.help_menu = tk.Menu(self, tearoff= 0)
        self.help_menu.add_command(label='Aide') 
        self.help_menu.add_command(label='A propos') 
        
        self.parent.config(menu = self)
        
    def run(self):
        self.add_cascade(label=app_name, menu=self.app_menu)
        self.add_cascade(label='Aide', menu=self.help_menu)
        