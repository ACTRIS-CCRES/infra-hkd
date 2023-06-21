
from typing import Any, Dict, Union

import requests
from .addons.contact import ContactPoint
from .addons.notification_policies import Notification
from .base import AcceptableCodes, get_encodable_dict
from grafanalib.core import Dashboard

class DashboardManager:
    """Class that handle the creation of dahsboard

    We can add multiple dashboards and then push
    to the grafana
    """
    def __init__(self, url: str, session: requests.Response):
        self.url = url
        self.session = session
        self.endpoint = f"{self.url}/dashboards/db/"
        self.config:Dict[Any,Any] = {}

    def get(self) -> Any:
        return self.config

    def add_dashboard(
        self, dashboard: Union[Dashboard, Dict[Any,Any]]
    ) -> "DashboardManager":
        if isinstance(dashboard, Dashboard):
            dashboard_dict = dashboard.to_json_data()
        else:
            dashboard_dict = dashboard

        self.config = dashboard_dict
        return self
    
    def push(self) -> requests.Response:
        json_d ={ 
            "dashboard": self.config,
            "overwrite": False,
            "folderUid" :"",
            "message": "Updated from API"
        }

        json_d = get_encodable_dict(json_d)

        res: requests.Response = self.session.post(self.endpoint, json=json_d)
        if res.status_code not in AcceptableCodes.list():
            msg = f"[{res.status_code}] : {res.content}"
            raise requests.HTTPError(msg)
        return res