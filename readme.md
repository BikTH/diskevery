# Diskevery

Application graphique destinée aux environnements Linux pour la gestion et la récupération de disques.

## Aperçu

Diskevery est une application de bureau construite avec [Tkinter](https://docs.python.org/3/library/tkinter.html) et [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter). Elle propose une interface plein écran qui centralise l'exploration des périphériques de stockage, la consultation de leurs informations et l'accès à des outils de maintenance courants.

Même si certaines fonctionnalités sont encore en phase de prototypage, l'interface expose déjà les composants clés de l'expérience utilisateur finale : navigation par panneaux, dialogues contextuels et prise en charge des thèmes clair/sombre.

## Fonctionnalités

- **Vue d'ensemble des disques** : liste interactive des disques internes, supports amovibles (USB) et lecteurs optiques, avec affichage des capacités et de l'espace libre.
- **Barre d'outils dédiée** : accès rapide aux opérations de gestion classiques (formatage, montage, redimensionnement, création et suppression de partitions, récupération de données).
- **Panneau de contenu dynamique** : zone centrale destinée à afficher les détails et actions spécifiques au disque sélectionné.
- **Barre de menu native** : commandes pour le dimensionnement de la fenêtre, le changement de thème et l'aide intégrée.
- **Compatibilité thèmes clair/sombre** : les icônes et palettes de couleurs s'adaptent automatiquement au thème choisi grâce aux ressources situées dans `assets/images`.

## Structure du projet

```
.
├── app
│   ├── controller      # Contrôleurs et logique métier (points d'extension)
│   ├── models          # (Placeholder) Structures de données métier
│   └── views           # Interfaces Tkinter/CustomTkinter et widgets
├── assets              # Icônes, images et autres ressources graphiques
├── LICENSE             # Licence GPLv3
└── readme.md
```

Les éléments d'interface principaux se trouvent dans `app/views/main_view.py`, `frames_class.py` et `bind_function.py`. Les styles globaux et utilitaires sont centralisés dans `app/views/general_information.py`.

## Prérequis

- Python 3.10 ou supérieur
- Environnement Linux avec gestionnaire de fenêtres compatible Tk

### Dépendances Python

Installez les dépendances nécessaires :

```bash
pip install customtkinter pillow
```

> **Remarque :** Tkinter est généralement fourni avec Python sur Linux. Vérifiez que le paquet `python3-tk` (ou équivalent) est installé sur votre distribution.

## Lancer l'application

Depuis la racine du projet :

```bash
python -m app.views.main_view
```

L'application se lance en plein écran. Utilisez la barre de menus pour ajuster la fenêtre ou quitter, sélectionnez un disque dans la colonne de gauche pour afficher ses options et explorez la barre d'outils pour accéder aux opérations de maintenance.

## Développement

- Les nouvelles vues doivent idéalement étendre les classes présentes dans `app/views/widgets_class.py` pour conserver la cohérence visuelle.
- Les icônes doivent être ajoutées dans `assets/images` et référencées via les utilitaires `assets_images` et `return_ctk_image` définis dans `general_information.py`.
- Préférez l'encodage UTF-8 et la nomenclature anglaise pour les noms de fichiers Python.

## Tests

Aucun test automatisé n'est fourni pour le moment. Pour valider une modification, lancez l'application manuellement (`python -m app.views.main_view`) et vérifiez les interactions impactées.

## Feuille de route

- Récupération des informations systèmes réelles sur les disques.
- Implémentation des opérations de formatage et de partitionnement.
- Localisation complète de l'interface.
- Ajout d'une suite de tests automatisés pour la logique de contrôle.

## Auteurs

- [@Bikoko Thierry](https://www.github.com/BikTH)
- [@Sinda Jordan](https://www.github.com/sinda-678)

## Licence

Sous licence [GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/).

## Crédit

- [Icons8](https://icones8.fr) : icônes de l'application.
