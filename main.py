from datetime import date
from typing import List, Optional
from notification_strategy import (
    NotificationStrategy,
    EmailNotificationStrategy,
    SMSNotificationStrategy,
    NotificationContext,
)


class Membre:
    def __init__(self, nom: str, role: str):
        self.nom = nom
        self.role = role


class Tache:
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


class Equipe:
    def __init__(self):
        self.membres = []

    def ajouter_membre(self, membre: Membre):
        self.membres.append(membre)


class Jalon:
    def __init__(self, nom: str, date: date):
        self.nom = nom
        self.date = date


class Risque:
    def __init__(self, description: str, probabilite: float, impact: str):
        self.description = description
        self.probabilite = probabilite
        self.impact = impact


class Changement:
    def __init__(self, description: str, version: str, date: date):
        self.description = description
        self.version = version
        self.date = date


class Projet:
    def __init__(
        self,
        nom: str,
        description: str,
        date_debut: date,
        date_fin: date,
        budget: float,
    ):
        self.nom = nom
        self.description = description
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.budget = budget
        self.taches = []
        self.equipe = Equipe()
        self.risques = []
        self.jalons = []
        self.versions = []
        self.changements = []
        self.notification_context = None

    def definir_notification_strategy(self, strategy: NotificationStrategy):
        self.notification_context = NotificationContext(strategy)

    def notifier_membres(self, message: str):
        if self.notification_context:
            for membre in self.equipe.membres:
                self.notification_context.envoyer_notification(message, membre.nom)

    def ajouter_tache(self, tache: Tache):
        self.taches.append(tache)
        self.notifier_membres(f"Nouvelle tâche ajoutée: {tache.nom}")

    def ajouter_membre_equipe(self, membre: Membre):
        self.equipe.ajouter_membre(membre)
        self.notifier_membres(f"{membre.nom}  a été ajouté à l'équipe")

    def ajouter_risque(self, risque: Risque):
        self.risques.append(risque)
        self.notifier_membres(f"Nouveau risque ajouté: {risque.description}")

    def ajouter_jalon(self, jalon: Jalon):
        self.jalons.append(jalon)
        self.notifier_membres(f"Nouveau jalon ajouté: {jalon.nom}")

    def ajouter_changement(self, changement: Changement):
        self.changements.append(changement)
        self.notifier_membres(
            f"Changement enregistré: {changement.description} (version {changement.version})"
        )

    def definir_budget(self, budget: float):
        self.budget = budget
        self.notifier_membres(
            f"Le budget du projet a été défini à {budget} Unité Monetaire"
        )

    def calculer_chemin_critique(self):
        return max(self.taches, key=lambda t: t.date_fin)

    def generer_rapport(self):
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
            rapport += f"  - {tache.nom}: {tache.statut} (de {tache.date_debut} à {tache.date_fin})\n"
        rapport += "Risques:\n"
        for risque in self.risques:
            rapport += f"  - {risque.description} (Probabilité: {risque.probabilite}, Impact: {risque.impact})\n"
        rapport += "Jalons:\n"
        for jalon in self.jalons:
            rapport += f"  - {jalon.nom} à la date {jalon.date}\n"
        rapport += "Changements:\n"
        for changement in self.changements:
            rapport += f"  - {changement.description} (Version: {changement.version} le {changement.date})\n"
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

    modou = Membre(nom="Modou", role="Développeur")
    christian = Membre(nom="Christian", role="Analyste")
    projet.ajouter_membre_equipe(modou)
    projet.ajouter_membre_equipe(christian)

    tache1 = Tache(
        nom="Analyse des besoins",
        description="Analyser les besoins du client",
        date_debut=date(2023, 2, 1),
        date_fin=date(2023, 2, 28),
        responsable=modou,
        statut="En cours",
    )
    projet.ajouter_tache(tache1)

    tache2 = Tache(
        nom="Développement",
        description="Développer les fonctionnalités",
        date_debut=date(2023, 3, 1),
        date_fin=date(2023, 6, 30),
        responsable=christian,
        statut="En attente",
    )
    projet.ajouter_tache(tache2)

    projet.definir_budget(50000)

    risque = Risque(description="Retard de livraison", probabilite=0.4, impact="Élevé")
    projet.ajouter_risque(risque)

    jalon = Jalon(nom="Phase 1 terminée", date=date(2023, 6, 30))
    projet.ajouter_jalon(jalon)

    changement = Changement(
        description="Changement de la portée du projet",
        version="2",
        date=date(2023, 5, 1),
    )
    projet.ajouter_changement(changement)

    print(projet.generer_rapport())
