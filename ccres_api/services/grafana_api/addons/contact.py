from dataclasses import dataclass, field
import os
import requests
from dotenv import load_dotenv
from enum import Enum
from typing import Dict, List, Any, Optional, Union
from abc import ABC, abstractmethod
from .base import GrafanaValidator
from .utils import clean_none


class ContactPoint(ABC):
    @abstractmethod
    def to_json_data(self):
        pass


@dataclass
class ContactPointEmailSettings(GrafanaValidator):
    """Contact point setting for Email

    Parameters
    ----------

    addresses: List[str]
        Email addresses
    singleEmail: bool, by default False
        Whether it is a single email or not
    message: Optional[str]
        Message template, by default None
    subject: Optional[str]
        Subject template, by default None
    """

    addresses: List[str]
    singleEmail: bool = False
    message: Optional[str] = None
    subject: Optional[str] = None

    def to_json_data(self):
        json_data = {
            "addresses": ";".join(self.addresses),
            "singleEmail": self.singleEmail,
            "message": self.message,
            "subject": self.subject,
        }
        return clean_none(json_data)


@dataclass
class ContactPointEmail(GrafanaValidator, ContactPoint):
    """Model for building a Mail contact point

    https://grafana.com/docs/grafana/latest/developers/http_api/alerting_provisioning/#span-idembedded-contact-pointspan-embeddedcontactpoint

    Parameters
    ----------
    name: str
        Name of the contact
    settings: ContactPointSlackSettings
        Settings of the email contact
    disableResolveMessage: bool = False
        Whether to disable message or not, by default False
    provenance: Optional[str]
        If this comes from API or UI. Left if blank. by default None
    """

    name: str
    settings: ContactPointEmailSettings
    disableResolveMessage: bool = False
    provenance: Optional[str] = None

    def to_json_data(self):
        json_data = {
            "name": self.name,
            "settings": self.settings.to_json_data(),
            "disableResolveMessage": self.disableResolveMessage,
            "provenance": self.provenance,
            "type": "email",
        }
        return clean_none(json_data)


@dataclass
class ContactPointSlackSettings(GrafanaValidator):
    """Contact point setting for Email

    Parameters
    ----------

    recipient: str
        Who to send to
    token: Optional[str]
        Token of the slack channel, by default None
    url: Optional[str]
        URL of the slack channel, by default None
    endpointUrl: Optional[str]
        Endpoint of the slack channel, by default None
    icon_emoji: Optional[str]
        Icon for the bot, by default None
    icon_url: Optional[str]
        Icon URL for the bot, by default None
    mentionChannel: Optional[str]
        Channel of mention, by default None
    mentionGroups: Optional[str]
        , by default None
    mentionUsers: Optional[str]
        , by default None
    text: Optional[str]
        Text template, by default None
    title: Optional[str]
        Title template, by default None
    username: Optional[str]
        Name of the bot, by default None
    """

    recipient: str
    token: Optional[str] = None
    url: Optional[str] = None
    endpointUrl: Optional[str] = None
    icon_emoji: Optional[str] = None
    icon_url: Optional[str] = None
    mentionChannel: Optional[str] = None
    mentionGroups: Optional[str] = None
    mentionUsers: Optional[str] = None
    text: Optional[str] = None
    title: Optional[str] = None
    username: Optional[str] = None

    def validate(self):
        if not self.token and not self.url:
            raise ValueError(
                "token and url can't be both empty. At least one field must be filled."
            )

    def to_json_data(self):
        json_data = {
            "recipient": self.recipient,
            "token": self.token,
            "url": self.url,
            "endpointUrl": self.endpointUrl,
            "icon_emoji": self.icon_emoji,
            "icon_url": self.icon_url,
            "mentionChannel": self.mentionChannel,
            "mentionGroups": self.mentionGroups,
            "mentionUsers": self.mentionUsers,
            "text": self.text,
            "title": self.title,
            "username": self.username,
        }
        return clean_none(json_data)


@dataclass
class ContactPointSlack(GrafanaValidator, ContactPoint):
    """Model for building a Slack contact point

    Parameters
    ----------
    name: str
        Name of the contact
    settings: ContactPointSlackSettings
        Settings of the slack contact
    disableResolveMessage: bool = False
        Whether to disable message or not, by default False
    provenance: Optional[str]
        If this comes from API or UI. Left if blank. by default None
    """

    name: str
    settings: ContactPointSlackSettings
    disableResolveMessage: bool = False
    provenance: Optional[str] = None

    def to_json_data(self):
        json_data = {
            "name": self.name,
            "settings": self.settings.to_json_data(),
            "disableResolveMessage": self.disableResolveMessage,
            "provenance": self.provenance,
            "type": "slack",
        }
        return clean_none(json_data)
