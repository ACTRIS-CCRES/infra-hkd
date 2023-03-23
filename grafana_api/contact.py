from dataclasses import dataclass, field
import os
import requests
from dotenv import load_dotenv
from enum import Enum
from typing import Dict, List, Any, Optional, Union
from abc import ABC, abstractmethod
from base import GrafanaSerializer, AcceptableCodes


@dataclass
class GrafanaContactPointModelEmailSettings(GrafanaSerializer):
    addresses: List[str]
    singleEmail: bool = False
    message: Optional[str] = None
    subject: Optional[str] = None

    def convert_addresses(self) -> str:
        return ";".join(self.addresses)


@dataclass
class GrafanaContactPointModelEmail(GrafanaSerializer):
    # https://grafana.com/docs/grafana/latest/developers/http_api/alerting_provisioning/#span-idembedded-contact-pointspan-embeddedcontactpoint
    name: str
    settings: GrafanaContactPointModelEmailSettings
    disableResolveMessage: bool = False
    provenance: Optional[str] = None
    type: str = "email"


@dataclass
class GrafanaContactPointModelSlackSettings(GrafanaSerializer):
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
class GrafanaContactPointModelSlack(GrafanaSerializer):
    # https://grafana.com/docs/grafana/latest/developers/http_api/alerting_provisioning/#span-idembedded-contact-pointspan-embeddedcontactpoint
    name: str
    settings: GrafanaContactPointModelSlackSettings
    disableResolveMessage: bool = False
    provenance: Optional[str] = None
    type: str = "slack"
