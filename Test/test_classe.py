"""
Ce module contient des tests unitaires pour la classe Projet.
"""

import unittest
from datetime import date
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import Membre, Tache, Projet, EmailNotificationStrategy


class TestProjet(unittest.TestCase):
    """
    Classe de test pour la classe Projet.
    
    Cette classe contient des tests unitaires pour vérifier les fonctionnalités
    de la classe Projet, y compris
    l'ajout de membres d'équipe, l'ajout de tâches,
    le calcul du chemin critique et la génération de rapports.
    """

    def setUp(self):
        """
        Configuration initiale pour chaque test.
        """
        self.membre1 = Membre(nom="Alice", role="Chef de projet")
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
        """
        Teste l'ajout d'un membre à l'équipe du projet.
        """
        self.projet.ajouter_membre_equipe(self.membre1)
        self.assertIn(self.membre1, self.projet.equipe.membres)

    def test_ajouter_tache(self):
        """
        Teste l'ajout d'une tâche au projet.
        """
        self.projet.ajouter_tache(self.tache1)
        self.assertIn(self.tache1, self.projet.taches)

    def test_calculer_chemin_critique(self):
        """
        Teste le calcul du chemin critique du projet.
        """
        self.projet.ajouter_tache(self.tache1)
        self.assertEqual(self.projet.calculer_chemin_critique(), self.tache1)

    def test_generer_rapport(self):
        """
        Teste la génération du rapport du projet.
        """
        self.projet.ajouter_membre_equipe(self.membre1)
        self.projet.ajouter_tache(self.tache1)
        rapport = self.projet.generer_rapport()
        self.assertIn("Projet Alpha", rapport)
        self.assertIn("Alice", rapport)
        self.assertIn("Analyse des besoins", rapport)


if __name__ == "__main__":
    unittest.main()
