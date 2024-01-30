# -*- coding: utf-8 -*-

"""_product.py: ."""

from ._helpers import *
import uuid
import logging
from datetime import datetime

from .asset import Asset, Service, License
from .registration_unit import LicenseRegistrationUnit

__author__ = "Charles Prevot"
__copyright__ = "Copyright 2024"

LOG = logging.getLogger("forticare")


# {
#   "status": "Registered"
#   "licenseNumber": "FMCLD4713562246",
#   "licenseSKU": "FMG-VM-CLOUD",
# }
def get_licenses(self, status: str = "", license_number: str = "", license_sku: str = "") -> list[License]:
    """
    Get license information.
    :param status: License status. Registered, Pending, Expired, or Decommissioned
    :type status: str
    :param license_number: License number
    :type license_number: str
    :param license_sku: License SKU
    :type license_sku: str
    :return list: Return a list of assets
    """
    endpoint = "/licenses/list"
    body = {}
    if status != "":
        body["status"] = str(status)
    if license_number != "":
        body["licenseNumber"] = str(license_number)
    if license_sku != "":
        body["licenseSKU"] = str(license_sku)

    LOG.info("> Getting license information...")
    results = {}
    try:
        results: dict = self._post(endpoint, body)
    except Exception as exp:
        LOG.error(">>> Failed to get license information: %s", str(exp.args))
        raise exp

    if isinstance(results, dict) and "licenses" in results:
        return [License(_l) for _l in results["licenses"]]
    raise Exception("Inexpected response from API:/n%s", results)


# Request body example:
# {
#   "licenseRegistrationCode": "K06V2-U795H-9PKR7-2TXNM-V8GL6B",
#   "description": "Backup device",
#   "additionalInfo": "",
#   "isGovernment": false
# }
def register_licenses(self, license: LicenseRegistrationUnit) -> Asset:
    """
    Register a subscription contract (e.g. VM-S) to generate serial number.
    :param license: License registration unit
    :type license: LicenseRegistrationUnit
    :return Asset: Details for registered asset
    """
    endpoint = "/licenses/register"
    body = license.to_json()

    LOG.info("> Registering new service...")
    results = {}
    try:
        results: dict = self._post(endpoint, body)
    except Exception as exp:
        LOG.error(">>> Failed to register service: %s", str(exp.args))
        raise exp

    if isinstance(results, dict) and "assetDetails" in results:
        return Asset(results["assetDetails"])
    raise Exception("Inexpected response from API:/n%s", results)


def download_licenses(self, serial_number: str) -> str:
    """
    Download key license file.
    :param serial_number: Serial number
    :type serial_number: str
    :return str: Return a license file
    """
    endpoint = "/licenses/download"
    body = {"serialNumber": str(serial_number)}

    LOG.info("> Downloading license file...")
    results = {}
    try:
        results: dict = self._post(endpoint, body)
    except Exception as exp:
        LOG.error(">>> Failed to download license file: %s", str(exp.args))
        raise exp

    if isinstance(results, dict) and "licenseFile" in results:
        return results["licenseFile"]
    raise Exception("Inexpected response from API:/n%s", results)
