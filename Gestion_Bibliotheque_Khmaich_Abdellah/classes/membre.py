class Membre:
    def __init__(self, id_membre, nom):
        self.id_membre = id_membre
        self.nom = nom
        self.livres_empruntes = []

    def __str__(self):
        return f"Membre {self.nom} (ID: {self.id_membre})"
