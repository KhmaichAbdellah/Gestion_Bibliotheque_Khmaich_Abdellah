import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import Style
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from visualisation import *
from classes.bibliotheque import Bibliotheque
from classes.livre import Livre
from classes.membre import Membre
from classes.exceptions import *

# Creation de l'objet Bibliothèque et chargement des données (livres + membres)
biblio = Bibliotheque()
biblio.charger()

# Configuration du style et de la fenêtre principale avec ttkbootstrap
style = Style("darkly")  # Choix du thème (darkly, flatly, morph, ...)
root = style.master
root.title("Système de Gestion de Bibliothèque")
root.geometry("1000x700")  # Dimensions fenêtre
root.configure(bg="#1b697d")  # Couleur de fond

#  Création des onglets : Livres, Membres, Statistiques
onglets = ttk.Notebook(root, bootstyle="primary")
tab_livres = ttk.Frame(onglets)
tab_membres = ttk.Frame(onglets)
tab_stats = ttk.Frame(onglets)
onglets.add(tab_livres, text=' Livres')
onglets.add(tab_membres, text=' Membres')
onglets.add(tab_stats, text=' Statistiques')
onglets.pack(expand=1, fill='both', padx=10, pady=10)

# =======================
#  Onglet LIVRES
# =======================

def refresh_liste_livres():
    # Vide la liste affichée puis recharge tous les livres depuis biblio.livres
    for row in tree_livres.get_children():
        tree_livres.delete(row)
    for livre in biblio.livres.values():
        tree_livres.insert('', 'end', values=(livre.isbn, livre.titre, livre.auteur, livre.genre, livre.statut))

# Frame contenant la liste des livres
frame_livres = ttk.Frame(tab_livres, padding=10)
frame_livres.pack(fill='both', expand=True)

# Table (Treeview) affichant les livres avec colonnes ISBN, Titre, Auteur, Genre, Statut
tree_livres = ttk.Treeview(frame_livres, columns=('ISBN', 'Titre', 'Auteur', 'Genre', 'Statut'), show='headings', bootstyle="info")
for col in tree_livres["columns"]:
    tree_livres.heading(col, text=col)  # Nom des colonnes
tree_livres.pack(fill='both', expand=True, pady=10)

# Formulaire d'ajout ou mise à jour d'un livre
form_frame = ttk.Labelframe(tab_livres, text="Ajouter un Livre", padding=10, bootstyle="primary")
form_frame.pack(pady=10)

entries = {}       # Dictionnaire pour stocker les champs de saisie
labels = {}        # Dictionnaire des labels des champs
error_labels = {}  # Labels d'erreur affichés sous chaque champ (en rouge)
champs = ["ISBN", "Titre", "Auteur", "Année", "Genre"]

# Création dynamique des labels, champs d'entrée et labels d'erreur pour chaque champ
for i, label_text in enumerate(champs):
    lbl = ttk.Label(form_frame, text=label_text)
    lbl.grid(row=0, column=i, padx=5)
    labels[label_text] = lbl
    
    ent = ttk.Entry(form_frame, width=15, bootstyle="primary")
    ent.grid(row=1, column=i, padx=5)
    entries[label_text] = ent

    # Label vide initial pour afficher un message d'erreur sous chaque champ si besoin
    err_lbl = ttk.Label(form_frame, text="", foreground="red")
    err_lbl.grid(row=2, column=i)
    error_labels[label_text] = err_lbl

def valider_champs():
    # Valide que tous les champs sont remplis, sinon met en rouge les champs et labels concernés
    valid = True
    for champ in champs:
        value = entries[champ].get().strip()
        if not value:
            entries[champ].configure(bootstyle="danger")    # Champ rouge
            labels[champ].configure(foreground="red")       # Label rouge
            error_labels[champ].configure(text="Remplir ce champ")
            valid = False
        else:
            entries[champ].configure(bootstyle="success")   # Champ vert
            labels[champ].configure(foreground="white")     # Label blanc
            error_labels[champ].configure(text="")
    return valid

def vider_champs():
    # Vide tous les champs et remet leur style à normal (primaire)
    for champ in champs:
        entries[champ].delete(0, 'end')
        entries[champ].configure(bootstyle="primary")
        labels[champ].configure(foreground="white")
        error_labels[champ].configure(text="")

def ajouter_livre():
    # Fonction déclenchée lors de l'ajout ou mise à jour d'un livre via le formulaire
    if not valider_champs():
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
        return

    isbn = entries["ISBN"].get().strip()
    titre = entries["Titre"].get().strip()
    auteur = entries["Auteur"].get().strip()
    annee = entries["Année"].get().strip()
    genre = entries["Genre"].get().strip()

    try:
        if isbn in biblio.livres:
            # Mise à jour d'un livre existant
            livre = biblio.livres[isbn]
            livre.titre = titre
            livre.auteur = auteur
            livre.annee = annee
            livre.genre = genre
            message = "Livre mis à jour avec succès."
        else:
            # Ajout d'un nouveau livre
            livre = Livre(isbn, titre, auteur, annee, genre)
            biblio.ajouter_livre(livre)
            message = "Livre ajouté avec succès."

        biblio.sauvegarder()  # Sauvegarde des données dans fichier
        refresh_liste_livres()  # Rafraîchit l'affichage
        vider_champs()
        messagebox.showinfo("Succès", message)

    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def supprimer_livre_selectionne():
    # Supprime le livre sélectionné dans la table, après confirmation
    selected = tree_livres.selection()
    if not selected:
        messagebox.showwarning("Aucun livre sélectionné", "Veuillez sélectionner un livre à supprimer.")
        return

    try:
        item = tree_livres.item(selected[0])
        isbn = str(item["values"][0]).strip()

        if isbn not in biblio.livres:
            raise LivreInexistantError()

        confirmation = messagebox.askyesno("Confirmation", f"Voulez-vous vraiment supprimer le livre ISBN {isbn} ?")
        if not confirmation:
            return

        #  Supprimer le livre de la liste des livres empruntés par tous les membres
        for membre in biblio.membres.values():
            if isbn in membre.livres_empruntes:
                membre.livres_empruntes.remove(isbn)

        # Supprimer le livre de la bibliothèque
        biblio.supprimer_livre(isbn)
        biblio.sauvegarder()

        refresh_liste_livres()
        refresh_membres()  # Met à jour aussi la liste des membres (car leurs emprunts ont changé)

        messagebox.showinfo("Succès", f"Livre ISBN {isbn} supprimé avec succès.")

    except LivreInexistantError:
        messagebox.showerror("Erreur", "Le livre sélectionné n'existe pas.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la suppression : {str(e)}")

# Boutons pour ajouter/metre à jour et supprimer un livre
ttk.Button(form_frame, text="Ajouter / Mettre à jour Livre", command=ajouter_livre, bootstyle="success-outline rounded").grid(row=3, column=0, columnspan=len(champs), pady=10)
ttk.Button(
    form_frame,
    text=" Supprimer Livre Sélectionné",
    command=lambda: supprimer_livre_selectionne(),
    bootstyle="danger-outline"
).grid(row=4, column=0, columnspan=len(champs), pady=5)

refresh_liste_livres()  # Affiche la liste des livres au démarrage

# =======================
#  Onglet MEMBRES 
# =======================

def refresh_membres():
    # Vide et recharge la table des membres avec leurs emprunts affichés
    for row in tree_membres.get_children():
        tree_membres.delete(row)
    for m in biblio.membres.values():
        tree_membres.insert('', 'end', values=(m.id_membre, m.nom, ", ".join(m.livres_empruntes)))

frame_membres = ttk.Frame(tab_membres, padding=10)
frame_membres.pack(fill='both', expand=True)

# Table affichant les membres avec ID, Nom, et Livres empruntés
tree_membres = ttk.Treeview(frame_membres, columns=('ID', 'Nom', 'Livres Empruntés'), show='headings', bootstyle="info")
for col in tree_membres["columns"]:
    tree_membres.heading(col, text=col)
tree_membres.pack(fill='both', expand=True, pady=10)

# Conteneur pour les 3 sections dans Membres : Ajout, Emprunt, Retour
frame_sections = ttk.Frame(tab_membres)
frame_sections.pack(fill='x', pady=10, padx=10)

# ----- Section 1 : Ajouter un Membre -----
form_ajout = ttk.Labelframe(frame_sections, text="Ajouter un Membre", padding=10, bootstyle="primary")
form_ajout.grid(row=0, column=0, sticky='nsew', padx=5)

id_entry = ttk.Entry(form_ajout, width=15, bootstyle="primary")
nom_entry = ttk.Entry(form_ajout, width=15, bootstyle="primary")
ttk.Label(form_ajout, text="ID").grid(row=0, column=0, padx=5, pady=2)
id_entry.grid(row=1, column=0, padx=5, pady=2)
ttk.Label(form_ajout, text="Nom").grid(row=0, column=1, padx=5, pady=2)
nom_entry.grid(row=1, column=1, padx=5, pady=2)

def valider_ajout_membre():
    # Valide que l'ID et le nom sont remplis pour ajouter un membre
    valid = True
    if not id_entry.get().strip():
        id_entry.configure(bootstyle="danger")
        valid = False
    else:
        id_entry.configure(bootstyle="primary")
    if not nom_entry.get().strip():
        nom_entry.configure(bootstyle="danger")
        valid = False
    else:
        nom_entry.configure(bootstyle="primary")
    return valid

def ajouter_membre():
    # Ajoute un membre à la bibliothèque si la validation passe
    if not valider_ajout_membre():
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
        return
    try:
        membre = Membre(id_entry.get().strip(), nom_entry.get().strip())
        biblio.enregistrer_membre(membre)
        biblio.sauvegarder()
        refresh_membres()
        messagebox.showinfo("Succès", "Membre ajouté.")
        id_entry.delete(0, 'end')
        nom_entry.delete(0, 'end')
        id_entry.configure(bootstyle="primary")
        nom_entry.configure(bootstyle="primary")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

ttk.Button(form_ajout, text="Ajouter Membre", command=ajouter_membre, bootstyle="success-outline").grid(row=2, column=0, columnspan=2, pady=10)

# ----- Section 2 : Emprunter un Livre -----
form_emprunt = ttk.Labelframe(frame_sections, text="Emprunter un Livre", padding=10, bootstyle="primary")
form_emprunt.grid(row=0, column=1, sticky='nsew', padx=5)

emprunt_id_entry = ttk.Entry(form_emprunt, width=15, bootstyle="primary")
emprunt_isbn_entry = ttk.Entry(form_emprunt, width=15, bootstyle="primary")
ttk.Label(form_emprunt, text="ID Membre").grid(row=0, column=0, padx=5, pady=2)
emprunt_id_entry.grid(row=1, column=0, padx=5, pady=2)
ttk.Label(form_emprunt, text="ISBN Livre").grid(row=0, column=1, padx=5, pady=2)
emprunt_isbn_entry.grid(row=1, column=1, padx=5, pady=2)

def valider_emprunt():
    # Valide que les champs ID Membre et ISBN sont remplis pour un emprunt
    valid = True
    if not emprunt_id_entry.get().strip():
        emprunt_id_entry.configure(bootstyle="danger")
        valid = False
    else:
        emprunt_id_entry.configure(bootstyle="primary")
    if not emprunt_isbn_entry.get().strip():
        emprunt_isbn_entry.configure(bootstyle="danger")
        valid = False
    else:
        emprunt_isbn_entry.configure(bootstyle="primary")
    return valid

def emprunter_livre():
    # Gère l'emprunt d'un livre par un membre
    if not valider_emprunt():
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
        return
    id_membre = emprunt_id_entry.get().strip()
    isbn = emprunt_isbn_entry.get().strip()
    try:
        biblio.emprunter_livre(isbn, id_membre)  # Méthode métier pour emprunter
        biblio.sauvegarder()
        refresh_membres()
        refresh_liste_livres()
        messagebox.showinfo("Succès", f"Livre {isbn} emprunté par le membre {id_membre}.")
        emprunt_id_entry.delete(0, 'end')
        emprunt_isbn_entry.delete(0, 'end')
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

ttk.Button(form_emprunt, text="Emprunter Livre", command=emprunter_livre, bootstyle="success-outline").grid(row=2, column=0, columnspan=2, pady=10)

# ----- Section 3 : Retourner un Livre -----
form_retour = ttk.Labelframe(frame_sections, text="Retourner un Livre", padding=10, bootstyle="primary")
form_retour.grid(row=0, column=2, sticky='nsew', padx=5)

retour_id_entry = ttk.Entry(form_retour, width=15, bootstyle="primary")
retour_isbn_entry = ttk.Entry(form_retour, width=15, bootstyle="primary")
ttk.Label(form_retour, text="ID Membre").grid(row=0, column=0, padx=5, pady=2)
retour_id_entry.grid(row=1, column=0, padx=5, pady=2)
ttk.Label(form_retour, text="ISBN Livre").grid(row=0, column=1, padx=5, pady=2)
retour_isbn_entry.grid(row=1, column=1, padx=5, pady=2)

def valider_retour():
    # Valide que les champs ID Membre et ISBN sont remplis pour retour livre
    valid = True
    if not retour_id_entry.get().strip():
        retour_id_entry.configure(bootstyle="danger")
        valid = False
    else:
        retour_id_entry.configure(bootstyle="primary")
    if not retour_isbn_entry.get().strip():
        retour_isbn_entry.configure(bootstyle="danger")
        valid = False
    else:
        retour_isbn_entry.configure(bootstyle="primary")
    return valid

def retourner_livre():
    # Gère le retour d'un livre par un membre
    if not valider_retour():
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
        return
    id_membre = retour_id_entry.get().strip()
    isbn = retour_isbn_entry.get().strip()
    try:
        biblio.retourner_livre(isbn, id_membre)
        biblio.sauvegarder()
        refresh_membres()
        refresh_liste_livres()
        messagebox.showinfo("Succès", f"Livre {isbn} retourné par le membre {id_membre}.")
        retour_id_entry.delete(0, 'end')
        retour_isbn_entry.delete(0, 'end')
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

ttk.Button(form_retour, text="Retourner Livre", command=retourner_livre, bootstyle="success-outline").grid(row=2, column=0, columnspan=2, pady=10)

# Bouton pour supprimer un membre sélectionné dans la table des membres
def supprimer_membre_selectionne():
    selection = tree_membres.selection()
    if not selection:
        messagebox.showwarning("Avertissement", "Aucun membre sélectionné.")
        return

    id_membre = tree_membres.item(selection[0], "values")[0]
    try:
        if id_membre not in biblio.membres:
            raise MembreInexistantError()

        membre = biblio.membres[id_membre]

        #  Rendre tous les livres empruntés par ce membre disponibles
        for isbn in membre.livres_empruntes:
            if isbn in biblio.livres:
                biblio.livres[isbn].statut = "disponible"

        #  Supprimer le membre de la bibliothèque
        del biblio.membres[id_membre]
        biblio.sauvegarder()

        refresh_membres()
        refresh_liste_livres()

        messagebox.showinfo("Succès", f"Membre {id_membre} supprimé et ses livres ont été rendus disponibles.")

    except Exception as e:
        messagebox.showerror("Erreur", str(e))

ttk.Button(tab_membres, text=" Supprimer Membre Sélectionné", command=supprimer_membre_selectionne, bootstyle="danger-outline").pack(pady=10)

# Ajustement des colonnes pour que les 3 sections soient équitablement réparties
frame_sections.columnconfigure(0, weight=1)
frame_sections.columnconfigure(1, weight=1)
frame_sections.columnconfigure(2, weight=1)

refresh_membres()  # Affiche la liste des membres au démarrage

# =======================
#  Onglet STATISTIQUES
# =======================

# Variables globales pour stocker l'état actuel du graphique affiché
canvas_stats = None
current_fig = None
graph_frame = None
button_frame = None
current_chart = "genres"

def afficher_graphique_stats(fig):
    # Affiche le graphique matplotlib passé en argument dans le frame dédié
    global canvas_stats, current_fig
    if canvas_stats:
        canvas_stats.get_tk_widget().destroy()  # Supprime ancien graphique
    if current_fig:
        plt.close(current_fig)  # Ferme l'ancienne figure matplotlib
    current_fig = fig
    canvas_stats = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas_stats.draw()
    canvas_stats.get_tk_widget().pack(fill='both', expand=True, pady=10)

def switch_graphique(type_chart):
    # Permet de changer de graphique selon le bouton sélectionné
    global current_chart
    current_chart = type_chart
    if type_chart == "genres":
        fig = genre_pie_chart_figure()
    elif type_chart == "auteurs":
        fig = top_auteurs_bar_figure()
    elif type_chart == "emprunts":
        fig = activite_emprunts_courbe_figure()
    else:
        fig = genre_pie_chart_figure()
    afficher_graphique_stats(fig)
    afficher_boutons()

def afficher_boutons():
    # Affiche les boutons permettant de changer de graphique
    for widget in button_frame.winfo_children():
        widget.destroy()

    autres = {
        "genres": [(" Top 10 Auteurs", "auteurs"), (" Emprunts Récents", "emprunts")],
        "auteurs": [("Répartition Genres", "genres"), (" Emprunts Récents", "emprunts")],
        "emprunts": [(" Répartition Genres", "genres"), (" Top 10 Auteurs", "auteurs")]
    }

    for texte, chart in autres.get(current_chart, []):
        ttk.Button(
            button_frame,
            text=texte,
            command=lambda c=chart: switch_graphique(c),
            bootstyle="light-outline",
            cursor="hand2",
            width=20,
            padding=10,
        ).pack(side="left", padx=5)

def afficher_statistiques():
    # Initialisation et affichage des widgets graphiques dans l'onglet Statistiques
    global graph_frame, button_frame
    for widget in tab_stats.winfo_children():
        widget.destroy()

    ttk.Label(tab_stats, text="Statistiques de la Bibliothèque", font=("Segoe UI", 18, "bold")).pack(pady=5)

    button_frame = ttk.Frame(tab_stats)
    button_frame.pack(pady=5)

    graph_frame = ttk.Frame(tab_stats)
    graph_frame.pack(fill='both', expand=True)

    switch_graphique("genres")  # Affiche par défaut la répartition des genres

#  Détecte le changement d'onglet et recharge les stats si on arrive sur l'onglet Statistiques
def on_tab_change(event):
    if onglets.index("current") == 2:  # Index 2 = onglet Statistiques
        afficher_statistiques()

onglets.bind("<<NotebookTabChanged>>", on_tab_change)
afficher_statistiques()

#  Lancement principal de la boucle Tkinter
root.mainloop()
