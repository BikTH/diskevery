import tkinter as tk
from customtkinter import CTk as ctk
from general_information import *
from frames_class import *

class Main_window(ctk):
    """_summary_ Classe principale de la vue, elle permet de construire 
    la fenêtre principale de notre application et ses composants 

    Args:
        ctk (_type_): _description_ classe parent 
    """   
    current_disk = " "
    
    def __init__(self): 
        """_summary_ Constructeur de notre classe
        """
        super().__init__() #on appelle le constructeur de la classe parent ctk
        
        # _________INFOS SUR LA FENETRE_________
        # On définit les information générale relative à notre fenêtre
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}") #on définit la taille par défaut de la fenêtre : plein écran ici
        self.title(f"{app_name}") #on définit le titre de la fenêtre
        self._set_appearance_mode(default_theme) #on définit le thème par défaut de l'application: dark, system ou light
        self.minsize(600, 400) #on définit la taille minimal que pourra avoir notre fenêtre
        
        # _________COLONNES & LIGNE DE LA FENETRE_________
        # On définit les proportions des compartiments de notre fenêtre afin qu'il soit le plus resposif possible
        # ||||||||||||||||| Colonnes |||||||||||||||||
        self.grid_columnconfigure(0,weight=0)
        self.grid_columnconfigure(1, weight=4)
        
        # ||||||||||||||||| Lignes |||||||||||||||||
        self.grid_rowconfigure(0,weight=1, uniform='group1')
        self.grid_rowconfigure(1,weight=2, uniform='group1')
        self.grid_rowconfigure(2,weight=10, uniform='group1')
        self.grid_rowconfigure(3,weight=1, uniform='group1')
        
        # _________FRAMES DE LA FENETRE_________
        # On charge les différentes frames qui constituerons notre fenêtre, 
        # ici nous en avons 5 : le menu, les disques, les outils, le contenu et l'état
        self.menu = MenuFrame(self)  #on créer le frame qui contiendra les éléments de la barre de menu 
        self.menu.run()


view = Main_window()
view.mainloop()