#  Système de Gestion de Bibliothèque

### Nom et prenom : khmaich Abdellah
### Année : 2024/2025  
### Filière : ENSAO GI3  
### Module : Programmation Avancée en Python
---------------------------------------------------------------------------------------------------

##  Guide d'installation

###  Prérequis
- Python 3.x installé sur votre machine
- Les modules suivants :
  - `ttkbootstrap`
  - `matplotlib`

### 📦 Installation des dépendances
Ouvrez un terminal dans le dossier du projet et exécutez :

```bash
pip install ttkbootstrap matplotlib
---------------------------------------------------------------------------------------------------
## Exemples d'utilisation

📖 **Ajouter un livre**  
Aller dans l’onglet Livres  
Remplir le formulaire (ISBN, Titre, Auteur, Année, Genre)  
Cliquer sur **Ajouter / Mettre à jour Livre**

📕 **Supprimer un livre**  
Sélectionner un livre dans la liste  
Cliquer sur **Supprimer Livre Sélectionné**

👤 **Ajouter un membre**  
Aller dans l’onglet Membres, section Ajouter un Membre  
Entrer l’ID et le nom du membre  
Cliquer sur **Ajouter Membre**

📗 **Emprunter un livre**  
Aller dans l’onglet Membres, section Emprunter un Livre  
Entrer l’ID du membre et l’ISBN du livre  
Cliquer sur **Emprunter Livre**

📘 **Retourner un livre**  
Aller dans l’onglet Membres, section Retourner un Livre  
Entrer l’ID du membre et l’ISBN du livre  
Cliquer sur **Retourner Livre**

📊 **Statistiques**  
Aller dans l’onglet Statistiques  
Visualiser la répartition des genres (camembert), le top 10 des auteurs (barres), et l’activité des emprunts (courbe)  
Utiliser les boutons pour changer de graphique

---------------------------------------------------------------------------------------------------

## Structure du projet

- `App.py'Interface graphique avec Tkinter et ttkbootstrap  
- `classes/` : Contient les classes `Livre.py`, `Membre.py`, `Bibliotheque.py` et les exceptions  
- `data/` : Contient les fichiers JSON de sauvegarde (`livres.json`, `membres.json`) et le fichier CSV d’historique  
- `visualisation.py` : Fonctions pour générer les graphiques statistiques

---------------------------------------------------------------------------------------------------

## Remarques

- La limite d’emprunt est de 3 livres par membre  
- Lors de la suppression d’un livre, il est aussi retiré des emprunts des membres  
- Lors de la suppression d’un membre, ses livres empruntés sont automatiquement rendus disponibles
