# -*- coding: utf-8 -*-

"""_core.py: ."""

import requests
import logging
import json
from typing import Union

__author__ = "Charles Prevot"
__copyright__ = "Copyright 2024"


FC_OAUTH = "https://customerapiauth.fortinet.com/api/v1/oauth/token/"  # used for login only
LOG = logging.getLogger("forticare")


def login(self, api_user: str = "", api_key: str = "") -> bool:
    """
    Retrive a new token for authentication.
    See more: https://docs.fortinet.com/document/fortiauthenticator/6.1.2/rest-api-solution-guide/498666/oauth-server-token-oauth-token
    :param api_user: API user to authenticate
    :type api_user: str
    :param api_user: API password
    :type api_user: str
    :return str: Return a bearer token
    """
    if api_user == "" or api_user is None:
        api_user = self._api_user
    else:
        self._api_user = api_user
    if api_key == "" or api_key is None:
        api_key = self._api_key
    else:
        self._api_key = api_key
    if api_user == "" or api_key == "" or api_user is None or api_key is None:
        LOG.error(">>> API user or API key is missing")
        return False
    body = {
        "username": str(api_user),
        "password": str(api_key),
        "client_id": "assetmanagement",
        "grant_type": "password",
    }
    LOG.info("> Retrieving API Token on FortiCare")
    results = requests.post(FC_OAUTH, json=body)
    if results.ok:
        j_data = json.loads(results.content)
        self.token = j_data["access_token"]
    elif results.status_code == 400 or results.status_code == 401:
        LOG.error(">>> Invalid credentials, or user improperly configured")
        return False
    else:
        error_description = ""
        try:
            j_data = results.json()
            error_description = j_data["error_description"]
        except Exception:
            pass
        LOG.error(
            ">>> Error: %s\nREQUEST:\nHeaders:\n%s\nBody:\n%s\nRESPONSE:\n%s\n",
            error_description,
            results.request.headers,
            results.request.body,
            results.content,
        )
        results.raise_for_status()  # unknown error. Raise an exception
        return False

    return True
