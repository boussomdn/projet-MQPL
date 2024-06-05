"""
Module de gestion de projet avec classes pour membres, tâches, équipes, jalons,
risques, changements et projets.
"""

from datetime import date
from typing import List, Optional
from notification_strategy import (
    NotificationStrategy,
    EmailNotificationStrategy,
    NotificationContext,
)


class Membre:
    """Classe représentant un membre de l'équipe."""

    def __init__(self, nom: str, role: str):
        self.nom = nom
        self.role = role

    def __repr__(self):
        return f"Membre(nom={self.nom}, role={self.role})"


class Tache:
    """Classe représentant une tâche dans le projet."""

    def __init__(
        self,
        nom: str,
        description: str,
        date_debut: date,
        date_fin: date,
        responsable: Membre,
        statut: str,
        dependances: Optional[List["Tache"]] = None,
    ):
        self.nom = nom
        self.description = description
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.responsable = responsable
        self.statut = statut
        self.dependances = dependances if dependances else []

    def __repr__(self):
        return (
            f"Tache(nom={self.nom}, statut={self.statut}, "
            f"date_debut={self.date_debut}, date_fin={self.date_fin})"
        )


class Equipe:
    """Classe représentant une équipe de projet."""

    def __init__(self):
        self.membres = []

    def ajouter_membre(self, membre: Membre):
        """Ajoute un membre à l'équipe."""
        self.membres.append(membre)

    def __repr__(self):
        return f"Equipe(membres={self.membres})"


class Jalon:
    """Classe représentant un jalon dans le projet."""

    def __init__(self, nom: str, date_jalon: date):
        self.nom = nom
        self.date_jalon = date_jalon

    def __repr__(self):
        return f"Jalon(nom={self.nom}, date_jalon={self.date_jalon})"


class Risque:
    """Classe représentant un risque dans le projet."""

    def __init__(self, description: str, probabilite: float, impact: str):
        self.description = description
        self.probabilite = probabilite
        self.impact = impact

    def __repr__(self):
        return (
            f"Risque(description={self.description}, "
            f"probabilite={self.probabilite}, impact={self.impact})"
        )


class Changement:
    """Classe représentant un changement dans le projet."""

    def __init__(self, description: str, version: str, date_changement: date):
        self.description = description
        self.version = version
        self.date_changement = date_changement

    def __repr__(self):
        return (
            f"Changement(description={self.description}, "
            f"version={self.version}, date_changement={self.date_changement})"
        )


class Projet:
    """Classe représentant un projet."""

    def __init__(
        self,
        nom: str,
        description: str,
        date_debut: date,
        date_fin: date,
        budget: float,
    ):
        self.nom: str = nom
        self.description: str = description
        self.date_debut: date = date_debut
        self.date_fin: date = date_fin
        self.budget: float = budget
        self.taches: List[Tache] = []
        self.equipe = Equipe()
        self.risques: List[Risque] = []
        self.jalons: List[Jalon] = []
        self.changements: List[Changement] = []
        self.notification_context: Optional[NotificationContext] = None

    def definir_notification_strategy(self, strategy: NotificationStrategy):
        """Définit la stratégie de notification."""
        self.notification_context = NotificationContext(strategy)

    def notifier_membres(self, message: str):
        """Envoie une notification aux membres de l'équipe."""
        if self.notification_context:
            for membre in self.equipe.membres:
                self.notification_context.envoyer_notification(message, membre.nom)

    def ajouter_tache(self, tache: Tache):
        """Ajoute une tâche au projet et notifie les membres."""
        self.taches.append(tache)
        self.notifier_membres(f"Nouvelle tâche ajoutée: {tache.nom}")

    def ajouter_membre_equipe(self, membre: Membre):
        """Ajoute un membre à l'équipe et notifie les membres."""
        self.equipe.ajouter_membre(membre)
        self.notifier_membres(f"{membre.nom} a été ajouté à l'équipe")

    def ajouter_risque(self, risque_projet: Risque):
        """Ajoute un risque au projet et notifie les membres."""
        self.risques.append(risque_projet)
        self.notifier_membres(f"Nouveau risque ajouté: {risque_projet.description}")

    def ajouter_jalon(self, jalon_projet: Jalon):
        """Ajoute un jalon au projet et notifie les membres."""
        self.jalons.append(jalon_projet)
        self.notifier_membres(f"Nouveau jalon ajouté: {jalon_projet.nom}")

    def ajouter_changement(self, changement_projet: Changement):
        """Ajoute un changement au projet et notifie les membres."""
        self.changements.append(changement_projet)
        self.notifier_membres(
            f"Changement enregistré: {changement_projet.description}"
            f"(version {changement_projet.version})"
        )

    def definir_budget(self, budget: float):
        """Définit le budget du projet et notifie les membres."""
        self.budget = budget
        self.notifier_membres(
            f"Le budget du projet a été défini à {budget} Unité Monétaire"
        )

    def generer_rapport(self):
        """Génère un rapport complet sur le projet."""
        rapport = f"Rapport du projet {self.nom}\n"
        rapport += f"Description: {self.description}\n"
        rapport += f"Date de début: {self.date_debut}\n"
        rapport += f"Date de fin: {self.date_fin}\n"
        rapport += f"Budget: {self.budget}\n"
        rapport += "Équipe:\n"
        for membre in self.equipe.membres:
            rapport += f"  - {membre.nom} ({membre.role})\n"
        rapport += "Tâches:\n"
        for tache in self.taches:
            rapport += f"  - {tache.nom}: {tache.statut}"
            f"(de {tache.date_debut} à {tache.date_fin})\n"
        rapport += "Risques:\n"
        for risk in self.risques:
            rapport += f"  - {risk.description} (Probabilité:"
            f"{risk.probabilite}, Impact: {risk.impact})\n"
        rapport += "Jalons:\n"
        for milestone in self.jalons:
            rapport += f"  - {milestone.nom} à la date"
            f"{milestone.date_jalon}\n"
        rapport += "Changements:\n"
        for change in self.changements:
            rapport += f"  - {change.description} (Version: "
            f"{change.version} le {change.date_changement})\n"
        return rapport


if __name__ == "__main__":
    projet = Projet(
        nom="Projet MQPL",
        description="Gestion de projet",
        date_debut=date(2023, 1, 1),
        date_fin=date(2023, 12, 31),
        budget=50000,
    )
    projet.definir_notification_strategy(EmailNotificationStrategy())
    Maty = Membre(nom="Maty", role="Développeur")
    Awa = Membre(nom="Awa", role="Analyste")
    projet.ajouter_membre_equipe(Maty)
    projet.ajouter_membre_equipe(Awa)
    tache1 = Tache(
        nom="Analyse des besoins",
        description="Analyser les besoins du client",
        date_debut=date(2023, 2, 1),
        date_fin=date(2023, 2, 28),
        responsable=Maty,
        statut="En cours",
    )
    projet.ajouter_tache(tache1)
    tache2 = Tache(
        nom="Développement",
        description="Développer les fonctionnalités",
        date_debut=date(2023, 3, 1),
        date_fin=date(2023, 6, 30),
        responsable=Awa,
        statut="En attente",
    )
    projet.ajouter_tache(tache2)
    projet.definir_budget(50000)
    risque_proj = Risque(
        description="Retard de livraison", probabilite=0.4, impact="Élevé"
    )
    projet.ajouter_risque(risque_proj)
    jalon_proj = Jalon(nom="Phase 1 terminée", date_jalon=date(2023, 6, 30))
    projet.ajouter_jalon(jalon_proj)
    changement_proj = Changement(
        description="Changement de la portée du projet",
        version="2",
        date_changement=date(2023, 5, 1),
    )
    projet.ajouter_changement(changement_proj)
    print(projet.generer_rapport())
