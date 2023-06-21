import requests
from pprint import pprint as print
import os
import pandas as pd

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from dotenv import load_dotenv
from grafana_api.base import AcceptableCodes


class GrafanaDatasourceMigrator6to9:
    def __init__(
        self, base: requests.Session, base_api_url: str, new: requests.Session, new_api_url: str
    ):
        """__init__

        Parameters
        ----------
        base : requests.Session
            Configuration request session of the base Grafana 6
            Need to be admin
        base_api_url : str
            Base of the api url for the base Grafana 6
            Need to be admin
        new : requests.Session
            Configuration request session of the Grafana 9
            Need to be admin
        new_api_url : str
            Base of the api url for the Grafana 9
            Need to be admin
        """
        self.base = base
        self.new = new
        self.base_api_url = base_api_url
        self.new_api_url = new_api_url
        self.base_datasources = self.base.get(f"{self.base_api_url}/datasources/").json()

    def migrate(self):
        for base_datasource in self.base_datasources:
            base_datasource_response = self.base.get(
                f"{self.base_api_url}/datasources/{base_datasource['id']}"
            ).json()
            self.new.post(f"{self.new_api_url}/datasources/", json=base_datasource_response).json()


class GrafanaDashboardMigrator6to9:
    def __init__(
        self, base: requests.Session, base_api_url: str, new: requests.Session, new_api_url: str
    ):
        """__init__

        Parameters
        ----------
        base : requests.Session
            Configuration request session of the base Grafana 6
            Need to be admin
        base_api_url : str
            Base of the api url for the base Grafana 6
            Need to be admin
        new : requests.Session
            Configuration request session of the Grafana 9
            Need to be admin
        new_api_url : str
            Base of the api url for the Grafana 9
            Need to be admin
        """
        self.base = base
        self.new = new
        self.base_api_url = base_api_url
        self.new_api_url = new_api_url
        print("Hello")
        self.base_folders = self.base.get(f"{self.base_api_url}/folders/").json()

    def migrate(self):

        for folder in self.base_folders:
            payload = {"title": folder["title"], "uid": folder["uid"]}
            folder_response_base = self.new.post(f"{self.new_api_url}/folders/", json=payload)
            if folder_response_base.status_code not in [200, 409, 412]:
                raise requests.RequestException(
                    f"{folder_response_base.status_code} : {folder_response_base.content}"
                )

            dashboards = self.base.get(
                f"{self.base_api_url}/search",
                params={"type": "dash-db", "folderIds": folder["id"]},
            ).json()

            for dashboard in dashboards:
                dashboard_response_base = self.base.get(
                    f"{self.base_api_url}/dashboards/uid/{dashboard['uid']}"
                ).json()

                dashboard_payload = dashboard_response_base["dashboard"]
                # Create a new dashboard
                dashboard_payload["id"] = None
                self.new.post(
                    f"{self.new_api_url}/dashboards/db",
                    json={"dashboard": dashboard_payload, "folderUid": folder["uid"]},
                )


class GrafanaContactMigrator6to9:
    def __init__(
        self, base: requests.Session, base_api_url: str, new: requests.Session, new_api_url: str
    ):
        """__init__

        Parameters
        ----------
        base : requests.Session
            Configuration request session of the base Grafana 6
            Need to be admin
        base_api_url : str
            Base of the api url for the base Grafana 6
            Need to be admin
        new : requests.Session
            Configuration request session of the Grafana 9
            Need to be admin
        new_api_url : str
            Base of the api url for the Grafana 9
            Need to be admin
        """
        self.base = base
        self.new = new
        self.base_api_url = base_api_url
        self.new_api_url = new_api_url
        self.base_contacts = self.base.get(f"{self.base_api_url}/alert-notifications/").json()

    def migrate(self):
        # We need to transform notification channel to contact when switching from 6 to 9.
        # General info on alerts notifications like alerts and so on.

        for base_contact in self.base_contacts:
            payload = {
                "uid": base_contact["uid"],
                "name": base_contact["name"],
                "type": base_contact["type"],
                "settings": base_contact["settings"],
                "provenance": "false",
            }
            self.new.post(f"{self.new_api_url}/v1/provisioning/contact-points", json=payload).json()


class GrafanaAlertMigrator6to9:
    def __init__(
        self, base: requests.Session, base_api_url: str, new: requests.Session, new_api_url: str
    ):
        """__init__

        Parameters
        ----------
        base : requests.Session
            Configuration request session of the base Grafana 6
            Need to be admin
        base_api_url : str
            Base of the api url for the base Grafana 6
            Need to be admin
        new : requests.Session
            Configuration request session of the Grafana 9
            Need to be admin
        new_api_url : str
            Base of the api url for the Grafana 9
            Need to be admin
        """
        self.base = base
        self.new = new
        self.base_api_url = base_api_url
        self.new_api_url = new_api_url
        self.base_alerts = self.base.get(f"{self.base_api_url}/alerts/").json()
        self.base_org = self.base.get(f"{self.base_api_url}/org/").json()

    def _get_folder_uid(self, alert):
        folder_uid = self.new.get(
            f"{self.new_api_url}/dashboards/uid/{alert['dashboardUid']}"
        ).json()["meta"]["folderUid"]
        return folder_uid

    def _get_datasource_uid_from_id(self, datasource_id: int):
        """_get_datasource_uid_from_id

        We need to get the datasource uid AFTER the migration of the datasource because this field
        does not exist in the previous
        """

        datasource_name = self.base.get(f"{self.base_api_url}/datasources/{datasource_id}").json()[
            "name"
        ]
        datasource_uid = self.new.get(
            f"{self.new_api_url}/datasources/name/{datasource_name}"
        ).json()["uid"]
        return datasource_uid

    def _string_to_time(self, date: str) -> int:
        date = date.replace("now", "0")
        return pd.Timedelta(date).seconds

    def _get_alert_rule_payload(self, alert_details, alert):
        """_get_alert_rule_payload

        Here comes the tricky part..
        https://grafana.com/docs/grafana/latest/developers/http_api/alerting_provisioning/#span-idalert-queryspan-alertquery
        We need to convert grafana 6 alert json to  grafana  alert json. We need to hardcoded
        some values and extract the query into new ones.
        In the old Grafana the query are nested inside the conditions, we need to denest
        them to make it more atomic and respect the new json.
        We also need to add informations about the datasources like the uid.

        Parameters
        ----------
        alert_details : dict
            Detailed information of the alert
        alert : dict
            General information of the alert

        """

        payload = {}
        # In annotations we need string type for all
        # This annotations section make the link between dashboard
        # and alert.
        payload["Annotations"] = {
            "__dashboardUid__": str(alert["dashboardUid"]),
            "__panelId__": str(alert["panelId"]),
        }

        # Needed by Grafana API.
        # https://grafana.com/docs/grafana/latest/developers/http_api/alerting_provisioning/#span-idalert-queryspan-alertquery
        payload["FolderUID"] = self._get_folder_uid(alert)
        payload["Title"] = alert_details["Name"]
        payload["for"] = alert_details["Settings"]["for"]
        payload["OrgID"] = alert_details["OrgId"]

        # To be defined because not present in Grafana 6
        payload["ExecErrState"] = "Error"
        payload["NoDataState"] = "NoData"
        payload["Labels"] = {"default": "default"}
        payload["RuleGroup"] = "SIRTA"

        # We need to loop over the condition and un-nest them.
        # The model was previously stored **inside** the classic condition.
        # We need to get them outside this condition i.e. create as many as model
        # as there was in conditions.
        payload["Data"] = []
        for condition_nb, condition in enumerate(alert_details["Settings"]["conditions"]):
            base_datasource_uid = self._get_datasource_uid_from_id(
                condition["query"]["datasourceId"]
            )

            _data = {}
            _data["DatasourceUID"] = base_datasource_uid
            _data["Model"] = condition["query"]["model"]
            _data["QueryType"] = ""
            _data["RefId"] = condition["query"]["model"]["refId"]

            # "To" == 0 is now
            # "From" is "To" - value
            from_time = self._string_to_time(condition["query"]["params"][1])
            to_time = self._string_to_time(condition["query"]["params"][2])
            _data["relativeTimeRange"] = {"from": from_time, "to": to_time}
            payload["Data"].append(_data)

        # Classic condition
        # In order to reproduce the classic condition we need to
        # replace the model.query by the coresponding refID created before
        # Increment one letter of alphabet to take the last panel
        # of alert
        last_ref_id = chr(ord(payload["Data"][-1]["RefId"]) + 1)

        _data = {}
        # Does not depend on any datasource but only on previous query
        _data["DatasourceUid"] = "-100"
        _data["Model"] = {}
        _data["Model"]["conditions"] = alert_details["Settings"]["conditions"]
        for condition_nb, condition in enumerate(alert_details["Settings"]["conditions"]):
            _data["Model"]["conditions"][condition_nb]["query"] = {
                "params": [condition["query"]["model"]["refId"]]
            }
        # Copy paste, don't know if it is useful
        _data["Model"]["datasource"] = {"name": "Expression", "type": "__expr__", "uid": "__expr__"}
        # Compatibility for old version
        _data["Model"]["type"] = "classic_conditions"
        _data["Model"]["refId"] = last_ref_id
        _data["RefId"] = last_ref_id
        # Set dummy value cause i don't know if it is
        # required (not written in doc)
        _data["relativeTimeRange"] = {"from": 600, "to": 0}

        payload["interval"] = alert_details["Settings"]["frequency"]
        payload["Data"].append(_data)
        payload["Condition"] = last_ref_id
        return payload

    def migrate(self):
        # We need to transform notification channel to contact when switching from 6 to 9.
        # General info on alerts notifications like alerts and so on.
        # General info on alerts. Can get more speficic by /alerts/:id
        for alert in self.base_alerts:
            alert_details = self.base.get(f"{self.base_api_url}/alerts/{alert['id']}").json()
            payload = self._get_alert_rule_payload(alert_details, alert)
            res = self.new.post(f"{self.new_api_url}/v1/provisioning/alert-rules/", json=payload)


def main():
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
    BASE_GRAFANA_SIRTA = os.environ.get("SIRTA_GRAFANA_URL")
    TOKEN_GRAFANA_SIRTA = os.environ.get("SIRTA_GRAFANA_TOKEN")
    AUTH_HEADER_GRAFANA_SIRTA = {"Authorization": f"Bearer {TOKEN_GRAFANA_SIRTA}"}

    PROXIES_SIRTA = {
        "http": "socks5://localhost:1080",
        "https": "socks5://localhost:1080",
    }

    BASE_GRAFANA_DOCKER = os.environ.get("DOCKER_GRAFANA_URL")
    AUTH_GRAFANA_DOCKER = requests.auth.HTTPBasicAuth(
        os.environ.get("DOCKER_GRAFANA_USERNAME"), os.environ.get("DOCKER_GRAFANA_PASSWORD")
    )
    session_from = requests.Session()
    session_from.headers.update(AUTH_HEADER_GRAFANA_SIRTA)
    session_from.proxies = PROXIES_SIRTA

    session_to = requests.Session()
    session_to.auth = AUTH_GRAFANA_DOCKER
    session_to.headers.update({"x-disable-provenance": "true"})
    dashboard_migrator = GrafanaDashboardMigrator6to9(
        session_from, BASE_GRAFANA_SIRTA, session_to, BASE_GRAFANA_DOCKER
    )
    dashboard_migrator.migrate()


if __name__ == "__main__":
    main()
