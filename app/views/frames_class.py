import tkinter as tk
from customtkinter import CTkFrame as CTkFrame
from customtkinter import *
from general_information import *


class Main_frame(CTkFrame):
    """_summary_ 
    cette classe nous servira de base pour toute nos frames
    """
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        super().__init__(self.parent)
        self.configure(corner_radius=0)


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
class Disque_label(CTkLabel):
    """Cette classe nous permetrra de lister les différents disque 
    """
    def __init__(self, parent, position: int, name: str, free_space: str = '---', total_space: str = '---', type: str = "disk"):
        """Constructeur de notre classe
        Args:
            parent (any): Le parent de cette classe
            position (int): la position du label
            name (str): Nom du disque
            free_space (int): espace libre sur le disque. par défaut "---"
            total_space (int): espace toal du disque. par défaut "---"
            type (str, optional): Type de disque: disk, cd, usb. par défaut "disk".
        """
        self.parent = parent
        self.position = position
        self.name = name
        self.type = type
        self.free_space = free_space+' Go' if free_space != '---' else free_space 
        self.total_space = total_space+' Go' if total_space != '---' else total_space 
        self.text = f'{self.name} \n {self.free_space} / {self.total_space}'
        
        if self.type == 'cd':
            self.image = return_ctk_image(cd_ico, 50, 50)
        elif self.type == 'usb':
            self.image = return_ctk_image(usb_ico, 50, 50)
        else:
            self.image = return_ctk_image(disk_ico, 50, 50)
        
        super().__init__(self.parent,
                         text=self.text,
                         corner_radius=8,
                         text_color=("black", "white"),
                         #font=()
                         anchor="center",
                         compound="left",
                         justify="left",
                         padx=5,
                         pady=5,
                         image= self.image
                         )
    
    def run_disk_label(self):
        self.parent.grid(row=self.position, column=0, padx=(10,10), pady=(10,0), sticky="new")
    
    def update_label_position(self,new_position: int):
        self.parent.grid_forget()
        self.parent.grid(row=new_position, column=0, padx=(10,10), pady=(10,0), sticky="new")
    
    def update_label_text(self,new_name: str, new_free_space: int):
        """Permet de metre à jour le texte du label
        Args:
            nom (str): le nouveau nom
            new_free_space (int): le nouvel espace libre
        """
        self.name =new_name
        self.free_space =new_free_space
        self.configure(text=f'{self.name} \n {self.free_space} / {self.total_space}')
    
    def delete_label(self):
        """permet de supprimer le label
        """
        self.destroy()


#____________________________________________________________________________
class DisqueFrame(Main_frame):
    """Cette classe nous permetrra de lister les différents disque 
    """
    
    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent, bg_color='black')
        
        self.titre =  CTkLabel(self, text="Disques",width=60, font=( 'none', 16), fg_color='transparent', padx=5, pady=15,)
        self.titre.grid(row=0, column=0, padx=(10,10), pady=(10,10), sticky="nsew")
        
        self.disk1 = Disque_label(self,position=1,name="Rupasan_drive",free_space='15',total_space='30',type="usb")
        self.disk1.grid(row=1, column=0, padx=(10,10), pady=(10,0), sticky="new")
        
        self.disk2 = Disque_label(self,position=2,name="Rupasan",free_space='10',total_space='16',type="usb")
        self.disk2.grid(row=2, column=0, padx=(10,10), pady=(10,0), sticky="new")
    


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