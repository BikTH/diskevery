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
        super().__init__(self.parent, *args, **kwargs)
        self.configure(corner_radius=0)
        self.configure()

class Main_label(CTkLabel):
    """on définira dans cette classe les différentes réaction qu'aura un label 
    en fonction des trigers .bind qui lui serons passé
    """
    def __init__(self, parent, main_window, *args, **kwargs):
        super().__init__(parent,*args,**kwargs)
        
        self.main = main_window


#____________________________________________________________________________MENU
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




#____________________________________________________________________________DISQUES
class Disque_label(CTkLabel):                                   
    """Cette classe nous permetrra de lister les différents disque 
    """
    def __init__(self, parent, main_window, position: int, name: str, free_space: str = '---', total_space: str = '---', type: str = "disk"):
        """Constructeur de notre classe
        Args:
            parent (any): Le parent de cette classe
            main_windows (any): La fenêtre principale
            position (int): la position du label
            name (str): Nom du disque
            free_space (int): espace libre sur le disque. par défaut "---"
            total_space (int): espace toal du disque. par défaut "---"
            type (str, optional): Type de disque: disk, cd, usb. par défaut "disk".
        """
        
        self.parent = parent
        self.main = main_window
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
        #on définit le style de notre classe et on lui passe en paramètre le parent, le main_window, le nom, l'image
        
        # HOVER TRIGERS : les trigers bind en rapport avec le hover
        #
        self.bind("<Enter>", lambda event, on=self : hover_on(event, on)) #change le bg au survol
        self.bind("<Leave>", lambda event, on=self : hover_off(event, on)) #restaure le bg aprés
        
        # CLICK TRIGER : le trigers bind en rapport avec la sélection
        #
        self.bind("<Button-1>", lambda event, on=self, main=self.main, parent=self.parent: select_disk_label(event, on, main, parent))
    
    
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


class DisqueFrame(Main_frame):
    """Cette classe nous permetrra de lister les différents disque 
    """
    
    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent, bg_color='black')
        
        self.titre =  CTkLabel(self, text="Disques",width=60, font=(app_font, 20), fg_color='transparent', padx=5, pady=15,)
        self.titre.grid(row=0, column=0, padx=(10,10), pady=(10,15), sticky="nsew")
        
        self.active_disk = None
        
        
        #TEST : à retirer présent pour raison de test actuellement
        #
        self.disk1 = Disque_label(self, self.parent, position=1,name="Rupasan_drive",free_space='15',total_space='30')
        self.disk1.grid(row=1, **disque_grid_style)
        
        self.disk2 = Disque_label(self, self.parent, position=2,name="Rupasan",free_space='10',total_space='16',type="usb")
        self.disk2.grid(row=2, **disque_grid_style)
        
        self.disk3 = Disque_label(self, self.parent, position=3,name="cd - lecteur",type="cd")
        self.disk3.grid(row=3, **disque_grid_style)




#____________________________________________________________________________OUTILS
class Outil_label(CTkLabel):
    """Cette classe va nous permettre de charger les labels relatifs aux divers outils
    """
    
    def __init__(self, parent, main_window, position: int, titre: str, image_dark: str, image_light:str):
        """Le construceur de notre classe nous permettrra de définir les attributs de notre label
        Args:
            parent (any): parent du label
            main_windows (any): La fenêtre principale
            position (int): position d'apparition de l'outil
            titre (str): Titre de l'outil
            image_dark (str): chemin vers l'image theme sombre à partir du dossier assets/images/
            image_light (str): chemin vers l'image theme clair à partir du dossier assets/images/
        """
        
        self.parent = parent
        self.main = main_window
        self.position = position
        self.titre = titre
        self.image = return_ctk_image(image_dark,60,60,image_light)
        
        super().__init__(self.parent, text=self.titre, image= self.image, **outils_label_style)
        
        self._bind_function = [select_formater_dialog, select_mont_dialog, select_resize_dialog, select_creation_dialog, select_delete_dialog, select_recovery_dialog]
        
        # self.bind_function = self._bind_function[self.position]
        
        # HOVER TRIGERS : les trigers bind en rapport avec le hover
        #
        self.bind("<Enter>", lambda event, on=self : hover_on(event, on)) #change le bg au survol
        self.bind("<Leave>", lambda event, on=self : hover_off(event, on)) #restaure le bg aprés
        
        # CLICK TRIGER : le trigers en rapport avec la sélection
        #
        self.bind("<Button-1>", lambda event, on=self : self._bind_function[self.position](event, on))
    
    def open_formater_dialog(event):
        dialog = Format_Dialog()
        text = dialog.get_input()
        print(text)
    
    def open_resize_dialog(event):
        dialog = Resize_Dialog()
    
    def open_mont_dialog(event):
        dialog = Mont_Dialog()
    
    def open_creation_dialog(event):
        dialog = Creation_Dialog()
    
    def open_delete_dialog(event):
        dialog = Delete_Dialog()
    
    def open_recovery_dialog(event):
        dialog = Recovery_Dialog()


class OutilsFrame(Main_frame):
    """Cette classe va nous permettre d'afficher les éléments de la barre d'outils
    """
    def __init__(self, parent):
        super().__init__(parent)
        
        self.grid_columnconfigure((0,1,2,3,4), weight=1, )
        self.grid_columnconfigure(5, weight=2, )
        
        self.format = Outil_label(self, self.parent, titre= 'Formater', position=0, image_dark=formater_ico[1], image_light=formater_ico[2])
        self.mount = Outil_label(self, self.parent, titre= 'Monter Disque', position=1, image_dark=mount_ico[1], image_light=mount_ico[2])
        self.resize = Outil_label(self, self.parent, titre= 'Etendre/Réduire partition', position=2, image_dark=resize_ico[1], image_light=resize_ico[2])
        self.create_partition = Outil_label(self, self.parent, titre= 'Créer une partition', position=3, image_dark=create_partition_ico[1], image_light=create_partition_ico[2])
        self.delete_partition = Outil_label(self, self.parent, titre= 'Supprimer partition', position=4, image_dark=delete_partition_ico[1], image_light=delete_partition_ico[2])
        self.recovery = Outil_label(self, self.parent, titre= 'Restaurer Disque', position=5, image_dark=recovery_ico[1], image_light=recovery_ico[2])
        
        self.format.grid(row=0, column=0, padx=(5,5), pady=(10,10), sticky="nsew")
        self.mount.grid(row=0, column=1, padx=(5,5), pady=(10,10),  sticky="nsew")
        self.resize.grid(row=0, column=2, padx=(5,5), pady=(10,10), sticky="nsew")
        self.create_partition.grid(row=0, column=3, padx=(5,5), pady=(10,10), sticky="nsew")
        self.delete_partition.grid(row=0, column=4, padx=(5,5), pady=(10,10), sticky="nsew")
        self.recovery.grid(row=0, column=5, padx=(10,10), pady=(10,10), sticky="nsew")




#____________________________________________________________________________CONTENU
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
        
        content = CTkLabel(self, text=self.text, image= self.image, **Default_contenu_style)
        
        content.grid(row=0, column=0, columnspan=2, padx=(10,10), pady=(10,10), sticky="nsew")
        
        content2 = CTkLabel(self, text=self.text2, font=(app_font, 20))
        content2.grid(row=1, column=0, columnspan=2, padx=(10,10), pady=(10,10), sticky="new")


class ContenuFrame(Main_frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="transparent")
        
        #Test
        content = CTkLabel(self, text="Hello World", font=(app_font, 20))
        content.grid(row=0, column=0, padx=(10,10), pady=(10,10), sticky="nsew")




#____________________________________________________________________________TACHES
class TachesFrame(Main_frame):
    def __init__(self, parent):
        super().__init__(parent)




#____________________________________________________________________________DIALOGUES
class Main_Dialog(CTkToplevel):
    """Cette classe va servir de classe de référence pour nos boîtes de dialogue
    """
    def __init__(self, title: str, fg_color= None):
        super().__init__(fg_color=fg_color)
        
        self._user_input = [] #cette variable contiendra les inputs de l'utilisateur sur le dialogue
        self._warning_image = return_ctk_image(warning_ico[1],100,100,warning_ico[2])
        self._ok_image = return_ctk_image(ok_ico[1],100,100,ok_ico[2])
        
        self.title(title) #on définit le titre de la fenêtre
        self.lift() #pour metre notre fenêtre au premier plan
        self.attributes("-topmost", True) #pour garder notre fenêtre au premier plan
        self.protocol("WM_DELETE_WINDOW", self._on_closing) #pour fermer notre fenêtre lorsque le fenêtre principal se ferme
        self.resizable(False, False) #pour éviter que les boîte de dialogue soit redimensionné
        self.grab_set() #pour rendre les autres fenêtre non cliquable lorsque la boîte de dialogue est ouverte
        
        
        
        #On définit le style de notre fenêtre 
        self._fg_color = ThemeManager.theme["CTkToplevel"]["fg_color"] 
        self._text_color = ThemeManager.theme["CTkLabel"]["text_color"] 
        self._button_fg_color = ThemeManager.theme["CTkButton"]["fg_color"] 
        self._button_hover_color = ThemeManager.theme["CTkButton"]["hover_color"] 
        self._button_text_color = ThemeManager.theme["CTkButton"]["text_color"] 
        self._entry_fg_color = ThemeManager.theme["CTkEntry"]["fg_color"] 
        self._entry_border_color = ThemeManager.theme["CTkEntry"]["border_color"] 
        self._entry_text_color = ThemeManager.theme["CTkEntry"]["text_color"] 
    
    def _on_closing(self):
        """Cette méthode nous permet de détruire la fenêtre
        """
        self._user_input.clear()
        self.grab_release()
        self.destroy()
    
    def _cancel_event(self):
        """Cette méthode nous permet d'anuler les actions dans la fenêtre et de la fermer
        """
        self._user_input.clear()
        self.grab_release()
        self.destroy()
    
    def get_input(self):
        """Cette méthode nous permet de récupérer les données de la fenêtre
        Returns:
            tableau: la tableau contenant les différentes informations de la fenêtre
        """
        self.master.wait_window(self)
        return self._user_input


class Format_Dialog(Main_Dialog):
    
    def __init__(self):
        
        self.titre = "Formater "
        super().__init__(self.titre)
        
        self.after(10, self._create_format_widgets)
        #on crée le contenu de notre boîte de dialogue
    
    def _create_format_widgets(self):
        """Cette fonction génére le contenu de notre fenêtre et ses différents champs
        """
        #ce label est responsable de titré l'entrée qui recupérera le nom de la partition
        #l'entry nous permettra de récupérer ce nom
        #et en dessous on a un label pour décrire les champs plus hauts
        self._name_label = CTkLabel(master=self, fg_color="transparent", text_color=self._text_color, anchor="e", font=(app_font,12),
                               text="Nom du volume")
        self._name_entry = CTkEntry(master=self, width=230, fg_color=self._entry_fg_color, border_color=self._entry_border_color, font=(app_font,12), text_color=self._entry_text_color)
        self._name_desc = CTkLabel(master=self, fg_color="transparent", text_color='grey', anchor="w", font=(app_font,12), 
                                   text="Nom de la partition aprés formatage")
        #on les ajoute à la fenêtre
        self._name_label.grid(row=0, column=0, columnspan=1, padx=(20,5), pady=(20, 0), sticky="ew")
        self._name_entry.grid(row=0, column=1, columnspan=2, padx=(5,20), pady=(20, 0), sticky="ew")
        self._name_desc.grid(row=1, column=1, columnspan=2, padx=(5,20), pady=(5, 0), sticky="ew")
        
        #ce label est responsable de titré le checkbox responsable de l'ajout de l'option pour effacer
        #ensuite on a le checkbox responsable de l'action de suppression et sa valeur par défaut qui est off
        #et en dessous on a un label pour décrire les champs de l'option supprimer
        self._delete_label = CTkLabel(master=self, fg_color="transparent", text_color=self._text_color, anchor="e", font=(app_font,12),
                               text="Effacer")
        self._delete_default_var = StringVar(value="off")
        self._delete = CTkCheckBox(master=self, variable=self._delete_default_var, onvalue="on", offvalue="off")
        self._delete_desc = CTkLabel(master=self, fg_color="transparent", text_color='grey', anchor="w", font=(app_font,12), text="Ecrase les données existantes, allonge la durée du formatage")
        #on les ajoute à notre fenêtre
        self._delete.grid(row=2, column=1, columnspan=2, padx=(5,20), pady=(20, 0), sticky="ew")
        self._delete_label.grid(row=2, column=0, columnspan=1, padx=(20,5), pady=(20, 0), sticky="ew")
        self._delete_desc.grid(row=3, column=1, columnspan=2, padx=(5,20), pady=(5, 0), sticky="ew")
        
        #ce label est responsable de titré l'option du choix du système de fichier
        #ensuite on a les différents radio en rapport avec les systèmes de fichier : NTFS, EXT4 et FAT
        self._sf_label = CTkLabel(master=self, fg_color="transparent", text_color=self._text_color, anchor="e", font=(app_font,12),
                               text="Système de fichier",)
        self._radio_var = StringVar(value="NTFS")
        self._NTFS_radio = CTkRadioButton(master=self, text="NTFS (Compatible avec Windows)", font=(app_font,12), variable= self._radio_var, value="NTFS")
        self._EXT4_radio = CTkRadioButton(master=self, text="EXT4 (Compatible avec les systèmes Linux)", font=(app_font,12), variable= self._radio_var, value="EXT4")
        self._FAT_radio = CTkRadioButton(master=self, text="FAT (Compatible avec tous les systèmes)", font=(app_font,12), variable= self._radio_var, value="FAT")
        #on les ajoute à notre fenêtre
        self._sf_label.grid(row=4, column=0, columnspan=1, padx=(20,5), pady=(20, 0), sticky="ew")
        self._NTFS_radio.grid(row=4, column=1, columnspan=2, padx=(5,20), pady=(20, 0), sticky="ew")
        self._EXT4_radio.grid(row=5, column=1, columnspan=2, padx=(5,20), pady=(20, 0), sticky="ew")
        self._FAT_radio.grid(row=6, column=1, columnspan=2, padx=(5,20), pady=(20, 0), sticky="ew")
        
        #on a ici les boutons annuler et confirmer
        self._cancel_button = CTkButton(master=self, width=100,
                                    border_width=0,
                                    fg_color=self._button_fg_color,
                                    hover_color=self._button_hover_color,
                                    text_color=self._button_text_color,
                                    text='Annuler',
                                    font=(app_font,12),
                                    command=self._cancel_event)
        self._next_button = CTkButton(master=self,
                                    width=100,
                                    border_width=0,
                                    fg_color='#ed4539',
                                    hover_color='#eb1d0e',
                                    text_color=self._button_text_color,
                                    text='Confirmer',
                                    font=(app_font,12),
                                    command=self._next_event)
        #on les ajoute à la fenêtre
        self._cancel_button.grid(row=7, column=1, columnspan=1, padx=(5, 10), pady=(20, 20), sticky="ew")
        self._next_button.grid(row=7, column=2, columnspan=1, padx=(5, 10), pady=(20, 20), sticky="ew")
    
    def _create_confirm_format_widgets(self):
        
        #on enlève les éléments de la fenêtre
        self._name_label.grid_remove()
        self._name_entry.grid_remove()
        self._name_desc.grid_remove()
        self._delete_label.grid_remove()
        self._delete.grid_remove()
        self._delete_desc.grid_remove()
        self._sf_label.grid_remove()
        self._NTFS_radio.grid_remove()
        self._EXT4_radio.grid_remove()
        self._FAT_radio.grid_remove()
        self._cancel_button.grid_remove()
        self._next_button.grid_remove()
        
        #on crée les nouveaux
        self._warning_label = CTkLabel(master=self, fg_color="transparent", text_color=self._text_color, anchor="center", font=(app_font, 24), compound="top", image= self._warning_image,
                               text="Attention: Toutes les données de la partition seront perdues",)
        self._warning_label.grid(row=0, column=0, columnspan=3, padx=(20,20), pady=(20, 0), sticky="ew")
        
        self._warning_desc_label = CTkLabel(master=self, fg_color="transparent", text_color=self._text_color, anchor="center", font=(app_font, 16),
                               text="Confirmer les détails de la partition avant de poursuivre",)
        self._warning_desc_label.grid(row=1, column=0, columnspan=3, padx=(20,20), pady=(20, 20), sticky="ew")
        
        self._peripherique_label = CTkLabel(master=self, fg_color="transparent", text_color=self._text_color, anchor="e", font=(app_font, 12),
                               text="Périphérique ",)
        self._peripherique_label.grid(row=2, column=0, columnspan=1, padx=(20,5), pady=(20, 10), sticky="ew")
        
        self._peripherique_content_label = CTkLabel(master=self, fg_color="transparent", text_color=self._text_color, anchor="w", font=(app_font, 13),
                               text="Test Tes Test ",)
        self._peripherique_content_label.grid(row=2, column=1, columnspan=2, padx=(20,5), pady=(20, 10), sticky="ew")
        
        self._volume_label = CTkLabel(master=self, fg_color="transparent", text_color=self._text_color, anchor="e", font=(app_font, 12),
                               text="Volume ",)
        self._volume_label.grid(row=3, column=0, columnspan=1, padx=(20,5), pady=(10, 10), sticky="ew")
        
        self._volume_content_label = CTkLabel(master=self, fg_color="transparent", text_color=self._text_color, anchor="w", font=(app_font, 13),
                               text="Test Test Test 2",)
        self._volume_content_label.grid(row=3, column=1, columnspan=2, padx=(20,5), pady=(10, 10), sticky="ew")
        
        self._use_label = CTkLabel(master=self, fg_color="transparent", text_color=self._text_color, anchor="e", font=(app_font, 12),
                               text="utilisé ",)
        self._use_label.grid(row=4, column=0, columnspan=1, padx=(20,5), pady=(10, 10), sticky="ew")
        
        self._use_content_label = CTkLabel(master=self, fg_color="transparent", text_color=self._text_color, anchor="w", font=(app_font, 13),
                               text="Test Test Test 3",)
        self._use_content_label.grid(row=4, column=1, columnspan=2, padx=(20,5), pady=(10, 10), sticky="ew")
        
        self._divice_label = CTkLabel(master=self, fg_color="transparent", text_color=self._text_color, anchor="e", font=(app_font, 12),
                               text="emplacement ",)
        self._divice_label.grid(row=5, column=0, columnspan=1, padx=(20,5), pady=(10, 0), sticky="ew")
        
        self._divice_content_label = CTkLabel(master=self, fg_color="transparent", text_color=self._text_color, anchor="w", font=(app_font, 13),
                               text="Test Test Test 4",)
        self._divice_content_label.grid(row=5, column=1, columnspan=2, padx=(20,5), pady=(10, 0), sticky="ew")
        
        #on a ici les boutons annuler et confirmer
        self._cancel_button = CTkButton(master=self, width=100,
                                    border_width=0,
                                    fg_color=self._button_fg_color,
                                    hover_color=self._button_hover_color,
                                    text_color=self._button_text_color,
                                    text='Annuler',
                                    font=(app_font,12),
                                    command=self._cancel_event)
        self._format_button = CTkButton(master=self,
                                    width=100,
                                    border_width=0,
                                    fg_color='#ed4539',
                                    hover_color='#eb1d0e',
                                    text_color=self._button_text_color,
                                    text='Formater',
                                    font=(app_font,12),
                                    command=self._format_event)
        #on les ajoute à la fenêtre
        self._cancel_button.grid(row=6, column=1, columnspan=1, padx=(5, 10), pady=(20, 20), sticky="ew")
        self._format_button.grid(row=6, column=2, columnspan=1, padx=(5, 10), pady=(20, 20), sticky="ew")
    
    def _next_event(self, event=None):
        self._create_confirm_format_widgets()
    
    def _format_event(self, event=None):
        self._user_input.extend([self._name_entry.get(), self._delete.get(), self._radio_var.get() ])
        self.grab_release()
        self.destroy()

class Resize_Dialog(Main_Dialog):
    
    def __init__(self):
        
        self.titre = "Formater "
        super().__init__(self.titre)
        
        self.after(10, self._create_format_widgets)
        #on crée le contenu de notre boîte de dialogue
    
    def _create_format_widgets(self):
        
        self.grid_columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)
        
        self._label = CTkLabel(master=self,
                               width=300,
                               wraplength=300,
                               fg_color="transparent",
                               text_color=self._text_color,
                               text="test2",)
        self._label.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        
        self._entry = CTkEntry(master=self,
                               width=230,
                               fg_color=self._entry_fg_color,
                               border_color=self._entry_border_color,
                               text_color=self._entry_text_color)
        self._entry.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")
        
        self._ok_button = CTkButton(master=self,
                                    width=100,
                                    border_width=0,
                                    fg_color=self._button_fg_color,
                                    hover_color=self._button_hover_color,
                                    text_color=self._button_text_color,
                                    text='Ok',
                                    command=self._ok_event)
        self._ok_button.grid(row=2, column=0, columnspan=1, padx=(20, 10), pady=(0, 20), sticky="ew")

class Mont_Dialog(Main_Dialog):
    pass

class Creation_Dialog(Main_Dialog):
    pass

class Delete_Dialog(Main_Dialog):
    pass

class Recovery_Dialog(Main_Dialog):
    pass
