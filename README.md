# 🧪 Calculateur du score des hydres

Ce projet permet de calculer automatiquement des scores à partir d'un fichier Excel (.xlsx) contenant des données biologiques liées à l'évolution de l'Hydre.

## 📦 Fonctionnalités

- Interface graphique simple via Tkinter

- Chargement d'un fichier Excel (.xlsx)

- Saisie du nombre total de lignes à traiter

- Calcul des scores selon les règles définies (T/E/I/M)

- Génération possible d'un .exe pour usage sans Python

## 🛠️ Installation

Installer les dépendances :

```pip install -r requirements.txt```

## ▶️ Utilisation

```python main.py```

- Cliquez sur "Parcourir" pour sélectionner le fichier Excel

- Entrez le nombre total de lignes à traiter

- Cliquez sur "Lancer le traitement"

## Export en .EXE (optionnel)

Pour convertir le programme en exécutable :

```pip install pyinstaller```

```pyinstaller --onefile --noconsole main.py```

L'exécutable sera généré dans le dossier dist/.