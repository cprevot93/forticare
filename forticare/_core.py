# -*- coding: utf-8 -*-

"""_core.py: ."""

import requests
import logging
import json
from typing import Union

__author__ = "Charles Prevot"
__copyright__ = "Copyright 2023"


FC_OAUTH = "https://customerapiauth.fortinet.com/api/v1/oauth/token/"  # used for login only
LOG = logging.getLogger()


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
        "client_id": "flexvm",
        "grant_type": "password",
    }
    LOG.info("> Retrieving API Token on FortiCare")
    results = requests.post(FC_OAUTH, json=body)
    if results.ok:
        j_data = json.loads(results.content)
        self.token = j_data["access_token"]
    elif results.status_code == 401:
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
            f">>> Error: {error_description}\nREQUEST:\nHeaders:\n{results.request.headers}\nBody:\n{results.request.body}\nRESPONSE:\n{results.content}\n",
        )
        results.raise_for_status()  # unknown error. Raise an exception
        return False

    return True


def get_entitlements_list(self, program_sn: str, config_id: int = 0, account_id: int = 0) -> list[Entitlement]:
    """
    Get list of existing entitlements for a Configuration.
    Configuration ID and Account ID are mutually exclusive i-e at least one of them must be provided.
    :param program_sn: Program Serial Number
    :type program_sn: str
    :param config_ID: entitlement configuration ID
    :type config_ID: int
    :param account_id: Account ID
    :type account_id: int
    :return list: return a list of entitlements
    {
        "entitlements": [
            {
                "configId": 144,
                "description": "Lab home",
                "endDate": "2023-03-31T00:00:00",
                "serialNumber": "FGVMELTM21000XXX",
                "startDate": "2021-12-21T10:41:26.153",
                "status": "EXPIRED",
                "token": "9BE4322EB1524F769FC7",
                "tokenStatus": "USED",
                "accountId": 899695
            },
            ...
        ],
        "error": null,
        "message": "Request processed successfully.",
        "status": 0
    }
    """
    results = None
    endpoint = "/entitlements/list"
    if config_id == 0 and account_id == 0:
        LOG.error(">>> Account ID or Configuration ID must be provided")
        raise ValueError("Account ID or Configuration ID must be provided")
    body: dict[str, Union[str, int]] = {
        "programSerialNumber": str(program_sn),
    }
    if config_id != 0:
        body["configId"] = int(config_id)
    if account_id != 0:
        body["accountId"] = int(account_id)
    LOG.info("> Fetching entitlements list with accountID %d and configID %d...", account_id, config_id)
    try:
        results = self._post(endpoint, body)
    except Exception as exp:
        LOG.error(">>> Failed to get entitlements list: %s", exp.args[1])
        raise exp

    return [Entitlement(entitlement) for entitlement in results["entitlements"]]
