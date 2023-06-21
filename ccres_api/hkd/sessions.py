from config.settings.base import (
    GRAFANA_AUTH_PASSWORD,
    GRAFANA_AUTH_TOKEN,
    GRAFANA_AUTH_USERNAME,
)
import requests
import logging


def get_grafana_session():
    session = requests.Session()
    session.headers.update({"x-disable-provenance": "true"})

    is_auth = False
    __nb_set = sum(x is not None or x != "" for x in [GRAFANA_AUTH_PASSWORD, GRAFANA_AUTH_USERNAME])
    if __nb_set == 1:
        logging.warning(
            "You need to set both GRAFANA_AUTH_PASSWORD and GRAFANA_AUTH_USERNAME in order to use basic authentifaction."
        )
        if GRAFANA_AUTH_PASSWORD is None:
            logging.warning("GRAFANA_AUTH_PASSWORD unset.")
        if GRAFANA_AUTH_USERNAME is None:
            logging.warning("GRAFANA_AUTH_USERNAME unset.")

    if __nb_set == 2:
        auth = requests.auth.HTTPBasicAuth(GRAFANA_AUTH_USERNAME, GRAFANA_AUTH_PASSWORD)
        session.auth = auth
        is_auth = True

    if not is_auth and GRAFANA_AUTH_TOKEN:
        headers = {"Authorization": f"Bearer {GRAFANA_AUTH_TOKEN}"}
        session.headers.update(headers)

    return session
