# Diskevery

Outil en ligne de commande destiné aux environnements Linux pour la gestion et la récupération d'informations relatives aux disques.

## Démarrage rapide

```bash
python -m app.main
```

La commande inspecte les disques disponibles, calcule l'utilisation de leurs partitions et affiche un rapport synthétique dans le terminal.

## Architecture

L'application est organisée autour de trois couches afin de faciliter l'évolution du code :

- `app/core` contient les modèles métiers (`DiskInfo`, `PartitionInfo`).
- `app/infrastructure` encapsule la récupération des données système (`SystemDiskInspector`).
- `app/services` agrège les informations de bas niveau pour produire des objets métiers prêts à l'emploi (`DiskService`).
- `app/presentation` fournit la vue actuelle en mode CLI (`render_disk_report`).

Cette séparation claire remplace l'ancienne architecture vide MVC et permet de réutiliser facilement les services au sein d'une interface graphique ultérieure.


## Authors

- [@Bikoko Thierry](https://www.github.com/BikTH)
- [@Sinda Jordan](https://www.github.com/sinda-678)


## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)


## Crédit

[Icons8](https://icones8.fr) : Icônes de l'application


