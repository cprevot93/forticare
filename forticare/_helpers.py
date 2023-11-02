# -*- coding: utf-8 -*-

import logging
import requests
import os
import platform
from ._constants import *
from logging.handlers import RotatingFileHandler

__author__ = "Charles Prevot"
__copyright__ = "Copyright 2023"

LOG = logging.getLogger()


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
def _post(self, endpoint: str, body: dict = {}) -> dict:
    url = FORTICARE_URL + endpoint

    if self.token is None or self.token == "":
        if self._auto_login:
            self.login()
        else:
            raise ValueError("Token is missing. Please login first.")
    j_data = None
    results = requests.post(url, headers={"Authorization": f"Bearer {self.token}"}, json=body, timeout=self.timeout)
    j_data = results.json()
    if results.ok:
        return j_data
    # need to refresh token
    if (
        (results.status_code == 400 or results.status_code == 401)
        and j_data
        and "message" in j_data
        and j_data["message"] == "Invalid security token."
    ):
        if self._auto_login:
            if self.login():
                return self._post(endpoint, body)
        else:
            raise requests.exceptions.HTTPError(results.status_code, j_data["message"])
    else:
        LOG.error(
            ">>> Error:\nREQUEST:\n%s\n%s\nRESPONSE:\n%s\n",
            str(results.request.headers),
            str(results.request.body),
            str(results.content),
        )
        if j_data and "message" in j_data:
            raise requests.exceptions.HTTPError(results.status_code, j_data["message"])
        else:
            results.raise_for_status()  # unknown error. Raise an exception
    return j_data