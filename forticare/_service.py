# -*- coding: utf-8 -*-

"""_product.py: ."""

from ._helpers import *
import uuid
import logging
from datetime import datetime

from .asset import Asset, Service

__author__ = "Charles Prevot"
__copyright__ = "Copyright 2023"

LOG = logging.getLogger()


# Request body example:
# {
#   "licenseRegistrationCode": "K06V2-U795H-9PKR7-2TXNM-V8GL6B",
#   "description": "Backup device",
#   "additionalInfo": "",
#   "isGovernment": false
# }
def register_services(
    self, registration_code: str, description: str = "", additional_info: str = "", is_government: bool = False
) -> Asset:
    """
    Register a subscription contract (e.g. VM-S) to generate serial number.
    :param registration_code: Registration code
    :type registration_code: str
    :param description: Description
    :type description: str
    :param additional_info: Additional information
    :type additional_info: str
    :param is_government: Is government
    :type is_government: bool
    :return list: Return a list of assets
    """
    endpoint = "/services/register"
    body = {
        "contractNumber": str(registration_code),
        "isGovernment": is_government,
    }
    if description != "":
        body["description"] = str(description)
    if additional_info != "":
        body["additionalInfo"] = str(additional_info)

    LOG.info("> Registering new service...")
    results = None
    try:
        results = self._post(endpoint, body)
    except Exception as exp:
        LOG.error(">>> Failed to register service: %s", str(exp.args))
        raise exp

    return Asset(results["assetDetails"])
