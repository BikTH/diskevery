import tkinter as tk
from customtkinter import CTkFrame as CTkFrame
from customtkinter import *
from general_information import *
from bind_function import *


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
        
        self.config(**menu_bar_style,tearoff = 0) #on définit les configurations de style de notre barre de menu
        
        #On crée les menus de notre barre de menu
        
        #Diskevery
        self.app_menu = tk.Menu(self, tearoff = 0,) 
        self.app_menu.config(**menu_style) #on définit les configurations de style pour ce menu
        self.app_menu.add_command(label='Agrandir',) 
        self.app_menu.add_command(label='Réduire')
        self.app_menu.add_separator
        self.app_menu.add_command(label='Fermer application', command=self.parent.destroy)
        #Vue
        self.view_menu = tk.Menu(self, tearoff= 0)
        self.view_menu.config(**menu_style) #on définit les configurations de style pour ce menu
        self.view_menu.add_command(label='Theme',state=['disabled']) 
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
            self.image = return_ctk_image(cd_ico_dark, 50, 50, cd_ico_light)
        elif self.type == 'usb':
            self.image = return_ctk_image(usb_ico_dark, 50, 50, usb_ico_light)
        else:
            self.image = return_ctk_image(disk_ico_dark, 50, 50, disk_ico_light)
        
        super().__init__(self.parent, text=self.text, image= self.image, **disque_label_style) 
        #on définit le style de notre classe et on lui passe en paramètre le pareent, le nom, l'image
        
        def on_enter(event):
            self.configure(fg_color='#242424')
        def on_leave(event):
            self.configure(fg_color='transparent') 
        
        self.bind('<Enter>', on_enter)
        self.bind('<Leave>', on_leave)
    
    
    def run_disk_label(self):
        """permet d'afficher le label
        """
        self.parent.grid(row=self.position, column=0, padx=(10,10), pady=(10,0), sticky="new")
    
    
    def update_label_position(self,new_position: int):
        """Permet de changer la position du label
        Args:
            new_position (int): nouvelle position
        """
        self.parent.grid_forget()
        self.parent.grid(row=new_position, column=0, padx=(10,10), pady=(10,0), sticky="new")
    
    
    def update_label_text(self,new_name: str =NONE, new_free_space: int=NONE):
        """Permet de metre à jour le texte du label
        Args:
            nom (str): le nouveau nom. par défaut NONE
            new_free_space (int): le nouvel espace libre. par défaut NONE
        """
        self.name=new_name if new_name != NONE else self.name
        self.free_space=new_free_space if new_free_space != NONE else self.free_space
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
        
        self.titre =  CTkLabel(self, text="Disques",width=60, font=(app_font, 20), fg_color='transparent', padx=5, pady=15,)
        self.titre.grid(row=0, column=0, padx=(10,10), pady=(10,15), sticky="nsew")
        
        self.disk1 = Disque_label(self,position=1,name="Rupasan_drive",free_space='15',total_space='30')
        self.disk1.grid(row=1, **disque_grid_style)
        
        self.disk2 = Disque_label(self,position=2,name="Rupasan",free_space='10',total_space='16',type="usb")
        self.disk2.grid(row=2, **disque_grid_style)
        
        self.disk3 = Disque_label(self,position=3,name="cd - lecteur",type="cd")
        self.disk3.grid(row=3, **disque_grid_style)


#____________________________________________________________________________
class Outil_label(CTkLabel):
    """Cette classe va nous permettre de charger les labels relatifs aux divers outils
    """
    
    def __init__(self, parent, position: int, titre: str, image_dark: str, image_light:str):
        """Le construceur de notre classe nous permettrra de définir les attributs de notre label
        Args:
            parent (any): parent du label
            position (int): position d'apparition de l'outil
            titre (str): Titre de l'outil
            image_dark (str): chemin vers l'image theme sombre à partir du dossier assets/images/
            image_light (str): chemin vers l'image theme clair à partir du dossier assets/images/
        """
        
        self.parent = parent
        self.position = position
        self.titre = titre
        self.image = return_ctk_image(image_dark,60,60,image_light)
        
        super().__init__(self.parent, text=self.titre, image= self.image, **outils_label_style)
        
        
        
        self.bind("<Enter>", lambda event, on=self : hover_on(event, on))
        self.bind("<Leave>", lambda event, on=self : hover_off(event, on))


#____________________________________________________________________________
class OutilsFrame(Main_frame):
    """Cette classe va nous permettre d'afficher les éléments de la barre d'outils
    """
    def __init__(self, parent):
        super().__init__(parent)
        
        self.grid_columnconfigure((0,1,2,3,4), weight=1, )
        self.grid_columnconfigure(5, weight=2, )
        
        self.format = Outil_label(self, titre= 'Formater', position=0, image_dark=formater_ico[1], image_light=formater_ico[2])
        self.mount = Outil_label(self, titre= 'Monter Disque', position=1, image_dark=mount_ico[1], image_light=mount_ico[2])
        self.resize = Outil_label(self, titre= 'Etendre/Réduire partition', position=2, image_dark=resize_ico[1], image_light=resize_ico[2])
        self.create_partition = Outil_label(self, titre= 'Créer une partition', position=3, image_dark=create_partition_ico[1], image_light=create_partition_ico[2])
        self.delete_partition = Outil_label(self, titre= 'Supprimer partition', position=4, image_dark=delete_partition_ico[1], image_light=delete_partition_ico[2])
        self.recovery = Outil_label(self, titre= 'Restaurer Disque', position=5, image_dark=recovery_ico[1], image_light=recovery_ico[2])
        
        self.format.grid(row=0, column=0, padx=(5,5), pady=(10,10), sticky="nsew")
        self.mount.grid(row=0, column=1, padx=(5,5), pady=(10,10),  sticky="nsew")
        self.resize.grid(row=0, column=2, padx=(5,5), pady=(10,10), sticky="nsew")
        self.create_partition.grid(row=0, column=3, padx=(5,5), pady=(10,10), sticky="nsew")
        self.delete_partition.grid(row=0, column=4, padx=(5,5), pady=(10,10), sticky="nsew")
        self.recovery.grid(row=0, column=5, padx=(10,10), pady=(10,10), sticky="nsew")


#____________________________________________________________________________
class DefaultContenuFrame(Main_frame):
    """Cette classe va contenir le contenu par défaut de notre fenêtre
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="transparent")
        
        self.text = "Aucun périphérique sélectionné pour l'instant"
        self.text2 = "Sélectionner un périphérique à gérer"
        self.image = return_ctk_image(default_ico,100,100)
        
        self.grid_columnconfigure(0, weight=1) 
        
        self.grid_rowconfigure(0, weight=1, uniform='default')
        self.grid_rowconfigure(1, weight=1, uniform='default')
        
        content = CTkLabel(self,
                         text=self.text,
                         corner_radius=8,
                         font=(app_font, 30),
                         anchor="center",
                         compound="top",
                         justify="center",
                         padx=10,
                         pady=10,
                         image= self.image
                         )
        content.grid(row=0, column=0, columnspan=2, padx=(10,10), pady=(10,10), sticky="nsew")
        
        content2 = CTkLabel(self, text=self.text2, font=(app_font, 20))
        content2.grid(row=1, column=0, columnspan=2, padx=(10,10), pady=(10,10), sticky="new")


#____________________________________________________________________________
class ContenuFrame(Main_frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="transparent")


#____________________________________________________________________________
class TachesFrame(Main_frame):
    def __init__(self, parent):
        super().__init__(parent)