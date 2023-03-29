from dataclasses import dataclass, field
import os
import requests
from dotenv import load_dotenv
from enum import Enum
from typing import Dict, List, Any, Optional, Union
from abc import ABC, abstractmethod
from base import GrafanaSerializer, AcceptableCodes


@dataclass
class ModelGrafanaContactPointEmailSettings(GrafanaSerializer):
    addresses: List[str]
    singleEmail: bool = False
    message: Optional[str] = None
    subject: Optional[str] = None

    def convert_addresses(self) -> str:
        return ";".join(self.addresses)


@dataclass
class ModelGrafanaContactPointEmail(GrafanaSerializer):
    """Model for building a Mail contact point

    https://grafana.com/docs/grafana/latest/developers/http_api/alerting_provisioning/#span-idembedded-contact-pointspan-embeddedcontactpoint

    Parameters
    ----------
        name: str
            Name of the contact
        settings: ModelGrafanaContactPointSlackSettings
            Settings of the email contact
        disableResolveMessage: bool = False
            Whether to disable message or not, by default False
        provenance: Optional[str]
            If this comes from API or UI. Left if blank. by default None
        type: str
            Type of the contact. Left it blank, by default "email"
    """
    name: str
    settings: ModelGrafanaContactPointEmailSettings
    disableResolveMessage: bool = False
    provenance: Optional[str] = None
    type: str = "email"


@dataclass
class ModelGrafanaContactPointSlackSettings(GrafanaSerializer):
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


@dataclass
class ModelGrafanaContactPointSlack(GrafanaSerializer):
    """Model for building a Slack contact point

    https://grafana.com/docs/grafana/latest/developers/http_api/alerting_provisioning/#span-idembedded-contact-pointspan-embeddedcontactpoint

    Parameters
    ----------

        name: str
            Name of the contact
        settings: ModelGrafanaContactPointSlackSettings
            Settings of the slack contact
        disableResolveMessage: bool = False
            Whether to disable message or not, by default False
        provenance: Optional[str]
            If this comes from API or UI. Left if blank. by default None
        type: str
            Type of the contact. Left it blank, by default "slack"
    """
    name: str
    settings: ModelGrafanaContactPointSlackSettings
    disableResolveMessage: bool = False
    provenance: Optional[str] = None
    type: str = "slack"
