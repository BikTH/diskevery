from PIL import Image, ImageTk

# _________main_view.py_________
#Variables utilisé dans le fichier frames_class.py

app_name = 'Diskevery'
default_theme = 'black'




# _________frames_class.py_________
#Variables utilisé dans le fichier frames_class.py

#Menu_Frame
menu_bar_style = { #on définit le style de notre menu ici
    "bg": "black", # couleur de fond
    "fg": "white", # couleur de texte
    "activebackground": "grey", # couleur de fond quand le menu est actif
    "activeforeground": "white", # couleur de texte quand le menu est actif
}

menu_style = {
    "bg": "black", # couleur de fond
    "fg": "white", # couleur de texte
    "activebackground": "grey", # couleur de fond quand la commande est active
    "activeforeground": "white", # couleur de texte quand la commande est active
}