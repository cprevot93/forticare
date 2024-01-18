# -*- coding: utf-8 -*-

"""_product.py: ."""

from ._helpers import *
import uuid
import logging
from datetime import datetime

from .asset import Asset, Service
from .registration_unit import ServiceRegistrationUnit

__author__ = "Charles Prevot"
__copyright__ = "Copyright 2023"

LOG = logging.getLogger("forticare")


# Request body example:
# {
#   "licenseRegistrationCode": "K06V2-U795H-9PKR7-2TXNM-V8GL6B",
#   "description": "Backup device",
#   "additionalInfo": "",
#   "isGovernment": false
# }
def register_services(self, service: ServiceRegistrationUnit) -> Asset:
    """
    Register a subscription contract (e.g. VM-S) to generate serial number.
    :param service: Service registration unit
    :type service: ServiceRegistrationUnit
    :return Asset: An assets
    """
    endpoint = "/services/register"
    body = service.to_json()

    LOG.info("> Registering new service...")
    results = None
    try:
        results = self._post(endpoint, body)
    except Exception as exp:
        LOG.error(">>> Failed to register service: %s", str(exp.args))
        raise exp

    return Asset(results["assetDetails"])
