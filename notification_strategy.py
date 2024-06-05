from abc import ABC, abstractmethod


class NotificationStrategy(ABC):
    @abstractmethod
    def envoyer(self, message: str, destinataire: str):
        pass


class EmailNotificationStrategy(NotificationStrategy):
    def envoyer(self, message: str, destinataire: str):
        print(f"Notification envoyée à {destinataire}: par email: {message}")


class SMSNotificationStrategy(NotificationStrategy):
    def envoyer(self, message: str, destinataire: str):
        print(f"Notification envoyée à {destinataire} par SMS: {message}")


class NotificationContext:
    def __init__(self, strategy: NotificationStrategy):
        self.strategy = strategy

    def envoyer_notification(self, message: str, destinataire: str):
        self.strategy.envoyer(message, destinataire)
