"""
Signals that are run when a object is saved or updated in the db
"""
from typing import Any, Dict, List, Optional, Type

from config.settings.base import GRAFANA_API_URL
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from hkd.models import AlertContact, AlertContactGroup
from hkd.sessions import get_grafana_session
from services.grafana_api.addons.contact import ContactPointEmail, ContactPointEmailSettings
from services.grafana_api.notification_manager import NotificationManager


@receiver(m2m_changed, sender=AlertContact.groups.through)
def create_grafana_contact(sender: Type[AlertContact], instance: AlertContact, **kwargs):
    action = kwargs.pop("action", None)
    if action and action != "post_add":
        return None

    session = get_grafana_session()
    groups = instance.groups.all()
    for group in groups:
        contacts = AlertContact.objects.filter(
            groups=group.id,
        )

        emails = [contact.email for contact in contacts]

        contact_point = ContactPointEmail(
            name=group.name,
            settings=ContactPointEmailSettings(addresses=emails),
        )

        notification_manager = NotificationManager(GRAFANA_API_URL, session)
        notification_manager.add_contact_point(contact_point)
        notification_manager.push()
