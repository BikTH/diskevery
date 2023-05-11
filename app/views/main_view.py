import tkinter as tk
from customtkinter import CTk as ctk
from general_information import *
from frames_class import *

class Main_window(ctk):
    """ Classe principale de la vue, elle permet de construire 
    la fenêtre principale de notre application et ses composants 
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
        #self.grid_rowconfigure(0,weight=1, uniform='group1')
        self.grid_rowconfigure(0,weight=3, uniform='group1')
        self.grid_rowconfigure(1,weight=10, uniform='group1')
        self.grid_rowconfigure(2,weight=1, uniform='group1')
        
        # _________FRAMES DE LA FENETRE_________
        # On charge les différentes frames qui constituerons notre fenêtre, 
        # ici nous en avons 5 : le menu, les disques, les outils, le contenu et l'état
        self.menu = MenuFrame(self)  #on créer le frame qui contiendra les éléments de la barre de menu 
        self.menu.add_menu_bar()
        
        self.disques = DisqueFrame(self) #on créer le frame responsable d'afficher les disques et on l'initialise avec grid
        self.disques.grid(row=0, rowspan=2, column=0, padx=(0,3), pady=(3,3), sticky="nsew")
        
        self.outils = OutilsFrame(self) #on créer le frame qui contiendra les éléments de la barre d'outil et on l'initialise avec grid
        self.outils.grid(row=0, column=1, padx=(3,0), pady=(3,3), sticky ="ew")
        
        self.contenu = DefaultContenuFrame(self) #on créer le frame qui contiendra les éléments de la zone de contenu principale et on l'initialise avec grid
        self.contenu.grid(row=1, column=1, padx=(3,0), pady=(3,0), sticky="nsew")
        
        self.menu = TachesFrame(self)  #on créer le frame qui contiendra les éléments de la barre de tache et on l'initialise avec grid
        self.menu.grid(row=2, column=0, columnspan=2, padx=(0,0), pady=(0,0), sticky="sew")


view = Main_window()
view.mainloop()