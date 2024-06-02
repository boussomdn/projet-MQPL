import unittest
from datetime import date
from main import Membre, Tache, Projet, EmailNotificationStrategy


class TestProjet(unittest.TestCase):
    def setUp(self):
        self.membre1 = Membre(nom="Alice", role="Chef de projet")
        self.membre2 = Membre(nom="Bob", role="Développeur")
        self.tache1 = Tache(
            nom="Analyse des besoins",
            description="Analyser les besoins du client",
            date_debut=date(2023, 5, 1),
            date_fin=date(2023, 5, 15),
            responsable=self.membre1,
            statut="En cours",
        )
        self.projet = Projet(
            nom="Projet Alpha",
            description="Développement d'une application web",
            date_debut=date(2023, 5, 1),
            date_fin=date(2023, 12, 31),
            budget=100000.0,
        )
        self.projet.definir_notification_strategy(EmailNotificationStrategy())

    def test_ajouter_membre_equipe(self):
        self.projet.ajouter_membre_equipe(self.membre1)
        self.assertIn(self.membre1, self.projet.equipe.membres)

    def test_ajouter_tache(self):
        self.projet.ajouter_tache(self.tache1)
        self.assertIn(self.tache1, self.projet.taches)

    def test_calculer_chemin_critique(self):
        self.projet.ajouter_tache(self.tache1)
        self.assertEqual(self.projet.calculer_chemin_critique(), self.tache1)

    def test_generer_rapport(self):
        self.projet.ajouter_membre_equipe(self.membre1)
        self.projet.ajouter_tache(self.tache1)
        rapport = self.projet.generer_rapport()
        self.assertIn("Projet Alpha", rapport)
        self.assertIn("Alice", rapport)
        self.assertIn("Analyse des besoins", rapport)


if __name__ == "__main__":
    unittest.main()
