# -*- coding: utf-8 -*-

import json
import logging
import os
import platform
import requests
from ._constants import *
from logging.handlers import RotatingFileHandler

__author__ = "Charles Prevot"
__copyright__ = "Copyright 2023"

LOG = logging.getLogger("forticare")


def check_python_version():
    """
    Ensure the correct version of Python is being used.
    """
    minimum_version = ("3", "7")
    if platform.python_version_tuple() < minimum_version:
        message = "Only Python %s.%s and above is supported." % minimum_version
        raise Exception(message)


def init_logging(logger, log_level_console=logging.INFO):
    """
    Init logging module. A log file is created. Message will also be display in the console.
    :param logger: logger to init
    :type logger: logger
    :param log_level: visibility
    :type pwd: string
    :return: True if login success, False if login failed
    """
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    os.makedirs("logs", exist_ok=True)
    log_path = os.path.join("logs", "debug.log")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s", "%H:%M:%S")

    file_handler = RotatingFileHandler(log_path, "a", 1000000, 1)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    # second handle for console output
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level_console)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


# Error message example:
# HTTP 400 Bad Request
# Body:
# {
#     "build": "1.0.0",
#     "error": {
#         "errorCode": 101,
#         "message": "Both serialNumber and expireBefore cannot be empty at the same time."
#     },
#     "message": "Invalid incoming request.",
#     "status": -1,
#     "token": "7u7L4jqtZglv0toJjKvTJ415hkluBx",
#     "version": "3.0",
#     "assets": null,
#     "pageNumber": 0,
#     "totalPages": 0
# }

# Example 2:
# HTTP 400 Bad Request
# {
#     "build": "1.0.0",
#     "error": {
#         "errorCode": 301,
#         "message": "The license download function for given product category is not supported."
#     },
#     "message": "The license download function for given product category is not supported.",
#     "status": -2,
#     "token": "rZn5irgDwNxDK6snDol3ZYsptn0kAF",
#     "version": "3.0",
#     "licenseFile": "",
#     "serialNumber": "FSACLPTM21000303"
# }


# Example 3: Not logged in
# {
#     "build": "1.0.0",
#     "error": {
#         "errorCode": 201,
#         "message": "Invalid security token."
#     },
#     "message": "Invalid incoming request.",
#     "status": -1,
#     "token": "rZn5irgDwNxDK6snDol3ZYsptn0kAF",
#     "version": "3.0",
#     "assetDetails": null
# }
def _post(self, endpoint: str, body: dict = {}) -> dict:
    url = FORTICARE_URL + endpoint

    if self.token is None or self.token == "":
        if self._auto_login:
            self.login()
        else:
            raise ValueError("Token is missing. Please login first.")
    j_data = None
    if self.debug:
        LOG.debug(">>> POST %s\n%s", url, json.dumps(body, indent=4))
    results = requests.post(url, headers={"Authorization": f"Bearer {self.token}"}, json=body, timeout=self.timeout)
    print(results)
    j_data = results.json()
    if results.ok:
        return j_data
    # refresh token
    elif (
        (results.status_code == 400 or results.status_code == 401 or results.status_code == 403)
        and j_data
        and "error" in j_data
        and j_data["error"]
        and "message" in j_data["error"]
        and (
            j_data["error"]["message"] == "Invalid security token."
            or j_data["error"]["message"] == "Access denied. No permission to access the requested action or resource."
            or j_data["error"]["message"] == "Please provide token in request."
        )
    ):
        if self._auto_login:
            if self.login():
                return self._post(endpoint, body)
        else:
            raise requests.exceptions.HTTPError(results.status_code, f"POST {endpoint} {j_data['error']['message']}")
    else:
        if self.debug:
            LOG.debug(
                ">>> Error:\nREQUEST:\n%s\n%s\nRESPONSE:\n%s\n",
                str(results.request.headers),
                str(results.request.body),
                str(results.content),
            )
        if j_data and "error" in j_data and "message" in j_data["error"]:
            raise requests.exceptions.HTTPError(results.status_code, f"POST {endpoint} {j_data['error']['message']}")
        elif j_data and "message" in j_data:
            raise requests.exceptions.HTTPError(results.status_code, f"POST {endpoint} {j_data['message']}")
        else:
            results.raise_for_status()  # unknown error. Raise an exception
    return j_data
