class LivreIndisponibleError(Exception):
    def __init__(self, message="Le livre est indisponible."):
        self.message = message
        super().__init__(self.message)
class QuotaEmpruntDepasseError(Exception):
    def __init__(self, message="Le quota d'emprunt a été dépassé."):
        self.message = message
        super().__init__(self.message)
class MembreInexistantError(Exception):
    def __init__(self, message="Le membre n'existe pas."):
        self.message = message
        super().__init__(self.message)
class LivreInexistantError(Exception):
    def __init__(self, message="Le livre n'existe pas."):
        self.message = message
        super().__init__(self.message)
    