from typing import Any, Dict, Union

import requests
from .addons.contact import ContactPoint
from .addons.notification_policies import Notification
from .base import AcceptableCodes, get_encodable_dict
from grafanalib.core import Dashboard
from typing import Optional, List
import datetime as dt


class DashboardManager:
    """Class that handle the creation of dahsboard

    We can add multiple dashboards and then push
    to the grafana
    """

    def __init__(self, url: str, session: requests.Response):
        self.url = url
        self.session = session
        self.endpoint = f"{self.url}/dashboards/db/"
        self.fetched_json: Dict[Any, Any] = self.fetch()
        self._dashboards = []

    def get_fetched_json(self) -> Any:
        return self.fetched_json

    def fetch(self) -> Dict[Any, Any]:
        res = self.session.get(f"{self.url}/search/?query=%")
        if res.status_code not in AcceptableCodes.list():
            msg = "Unable to get the current configuration\n"
            msg += f"[{res.status_code}] : {res.content}"
            raise requests.HTTPError(msg)
        self.fetched_json = res.json()
        return self.fetched_json

    def add_dashboard(
        self, dashboard: Union[Dashboard, Dict[Any, Any]], folder_uid: Optional[str] = None
    ) -> "DashboardManager":
        if isinstance(dashboard, Dashboard):
            dashboard_dict = dashboard.to_json_data()
        else:
            dashboard_dict = dashboard
        if folder_uid is None:
            folder_uid = ""
        self._dashboards.append((folder_uid, dashboard_dict))

        return self

    def push(self) -> List[requests.Response]:
        responses = []
        for folder_uid, dashboard in self._dashboards:
            json_d = {
                "dashboard": dashboard,
                "overwrite": True,
                "folderUid": folder_uid,
                "message": f"Updated from API at {dt.datetime.now().isoformat()}",
            }

            json_d = get_encodable_dict(json_d)

            res: requests.Response = self.session.post(self.endpoint, json=json_d)
            if res.status_code not in AcceptableCodes.list():
                msg = f"[{res.status_code}] : {res.content}"
                raise requests.HTTPError(msg)
            responses.append(res)
        return responses
