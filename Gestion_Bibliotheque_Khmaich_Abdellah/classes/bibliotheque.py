import json
import csv
from datetime import datetime
from classes.livre import Livre
from classes.membre import Membre
from classes.exceptions import *

class Bibliotheque:
    def __init__(self):
        self.livres = {}
        self.membres = {}

    def ajouter_livre(self, livre):
        self.livres[livre.isbn] = livre

    def supprimer_livre(self, isbn):
        if isbn in self.livres:
            del self.livres[isbn]
        else:
            raise LivreInexistantError()

    def enregistrer_membre(self, membre):
        self.membres[membre.id_membre] = membre

    def emprunter_livre(self, isbn, id_membre):
        if id_membre not in self.membres:
            raise MembreInexistantError()
        if isbn not in self.livres:
            raise LivreInexistantError()
        livre = self.livres[isbn]
        membre = self.membres[id_membre]
        if livre.statut != "disponible":
            raise LivreIndisponibleError()
        if len(membre.livres_empruntes) >= 3:
            raise QuotaEmpruntDepasseError()
        livre.statut = "emprunté"
        membre.livres_empruntes.append(isbn)
        self.enregistrer_historique(isbn, id_membre, "emprunt")

    def retourner_livre(self, isbn, id_membre):
        livre = self.livres.get(isbn)
        membre = self.membres.get(id_membre)
        if livre and isbn in membre.livres_empruntes:
            livre.statut = "disponible"
            membre.livres_empruntes.remove(isbn)
            self.enregistrer_historique(isbn, id_membre, "retour")
        else:
            raise LivreInexistantError("Le livre n'est pas emprunté par ce membre.")

    def sauvegarder(self):
        with open("data/livres.json", "w",encoding="utf-8") as f:
            json.dump({isbn: vars(livre) for isbn, livre in self.livres.items()}, f, indent=2)
        with open("data/membres.json", "w",encoding="utf-8") as f:
            json.dump({id_: {"nom": m.nom, "livres_empruntes": m.livres_empruntes} for id_, m in self.membres.items()}, f, indent=2)

    def charger(self):
        try:
            with open("data/livres.json", "r",encoding="utf-8") as f:
                data = json.load(f)
                self.livres = {isbn: Livre(**d) for isbn, d in data.items()}
        except FileNotFoundError:
            pass
        try:
            with open("data/membres.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.membres = {id_: Membre(id_, d["nom"]) for id_, d in data.items()}
                for id_, m in data.items():
                    self.membres[id_].livres_empruntes = m["livres_empruntes"]
        except FileNotFoundError:
            pass

    def enregistrer_historique(self, isbn, id_membre, action):
        with open("data/historique.csv", "a",encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().isoformat(), isbn, id_membre, action])
