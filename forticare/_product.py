# -*- coding: utf-8 -*-

"""_product.py: ."""

from ._helpers import *
import logging
import json
from datetime import datetime
from typing import List, Tuple

from .registration_unit import LicenseRegistrationUnit, ProductRegistrationUnit, ServiceRegistrationUnit
from .asset import Asset, Service
from .location import Location

__author__ = "Charles Prevot"
__copyright__ = "Copyright 2024"

LOG = logging.getLogger("forticare")


def get_products(
    self, expire_before: datetime, serial_number: str = "", product_model: str = "", status: str = "Registered"
) -> list[Asset]:
    """
    Returns product list based on product SN search pattern or support package expiration date.
    Both serialNumber and expireBefore cannot be empty at the same time.
    :param serial_number: Serial number or serial number search pattern
    :type serial_number: str
    :param expire_before: Date time in ISO 8601 format
    :type expire_before: datetime
    :param product_model: Product model name
    :type product_model: str
    :param status: Allowed values are Registered and Pending. Default value is Registered.
    :type status: str
    :return list: Return a list of assets
    """
    endpoint = "/products/list"
    body = {
        "status": str(status),
        "expireBefore": expire_before.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    if serial_number != "":
        body["serialNumber"] = str(serial_number)
    if product_model != "":
        body["productModel"] = str(product_model)

    LOG.info("> Retriving assets list...")
    results = {}
    try:
        results = self._post(endpoint, body)
    except Exception as exp:
        LOG.error(">>> Failed to retrive assets: %s", str(exp.args))
        raise exp

    if isinstance(results, dict) and "assets" in results:
        return [Asset(asset) for asset in results["assets"]]
    else:
        raise Exception("Inexpected response from API:/n%s", results)


def get_product_details(self, serial_number: str) -> Asset:
    """
    Returns product details based on product SN.
    :param serial_number: Serial number or serial number search pattern
    :type serial_number: str
    :return Asset: Return asset details
    """
    endpoint = "/products/details"
    body = {"serialNumber": str(serial_number)}

    LOG.info("> Retriving asset details...")
    results = {}
    try:
        results: dict = self._post(endpoint, body)
    except Exception as exp:
        LOG.error(">>> Failed to retrive asset details: %s", str(exp.args))
        raise exp

    return Asset(results["assetDetails"])


# {
#   "registrationUnits": [
#     {
#       "serialNumber": "FGT90D1234567890",
#       "contractNumber": "2121DJ8902",
#       "description": "Backup device",
#       "isGovernment": false,
#       "assetGroupIds": [],
#       "replacedSerialNumber": "FGT90D9876543210",
#       "additionalInfo": "",
#       "cloudKey": "80X4LSN3",
#       "location": {
#         // "ref": "#/locations/0"
#       }
#     }
#   ],
#   "locations": [
#     {
#       "company": "FortiTEST",
#       "address": "1234 Wall Street",
#       "city": "Sunnyvale",
#       "stateOrProvince": "CA",
#       "countryCode": "US",
#       "postalCode": "34510",
#       "email": "test@fortitest.com",
#       "phone": "3151231234",
#       "fax": "3151231235"
#     }
#   ]
# }
#
# Response:
# {
#   "token": "<string>",
#   "version": "<string>",
#   "status": "<integer>",
#   "message": "<string>",
#   "build": "<string>",
#   "error": "<string>",
#   "assets": [
#     {
#       "serialNumber": "<string>",
#       "folderId": "<number>",
#       "folderPath": "<string>",
#       "registrationDate": "<dateTime>",
#       "description": "<string>",
#       "isDecommissioned": "<boolean>",
#       "status": "<string>",
#       "productModel": "<string>",
#       "productModelEoR": "<string>",
#       "productModelEoS": "<string>",
#       "entitlements": [
#         {
#           "level": "<integer>",
#           "levelDesc": "<string>",
#           "type": "<integer>",
#           "typeDesc": "<string>",
#           "startDate": "<string>",
#           "endDate": "<string>"
#         },
#         {
#           "level": "<integer>",
#           "levelDesc": "<string>",
#           "type": "<integer>",
#           "typeDesc": "<string>",
#           "startDate": "<string>",
#           "endDate": "<string>"
#         }
#       ],
#       "assetGroups": [
#         {
#           "assetGroupId": "<integer>",
#           "assetGroup": "<string>"
#         },
#         {
#           "assetGroupId": "<integer>",
#           "assetGroup": "<string>"
#         }
#       ],
#       "warrantySupports": [
#         {
#           "level": "<integer>",
#           "levelDesc": "<string>",
#           "type": "<integer>",
#           "typeDesc": "<string>",
#           "startDate": "<string>",
#           "endDate": "<string>"
#         },
#         {
#           "level": "<integer>",
#           "levelDesc": "<string>",
#           "type": "<integer>",
#           "typeDesc": "<string>",
#           "startDate": "<string>",
#           "endDate": "<string>"
#         }
#       ],
#       "trialTypes": "<string>"
#     },
#     ...
#   ]
# }
def register_product(self, units: list[ProductRegistrationUnit], locations: list[Tuple[str, Location]] = []) -> bool:
    """
    Register products.
    :param units: Registration units
    :type units: list[ProductRegistrationUnit]
    :param locations: Locations
    :type locations: list[Tuple[serial_number: <string>, location: <Location>]]
    :return list[Asset]: Return a list of register assets
    """
    endpoint = "/products/register"
    _units_list = [ProductRegistrationUnit.to_json(unit) for unit in units]
    for unit in _units_list:
        for index, location in enumerate(locations):
            if unit["serialNumber"] == location[0]:
                unit["location"] = {"ref": "#/locations/" + str(index)}
    body = {
        "registrationUnits": _units_list,
    }
    if len(locations) > 0:
        body["locations"] = [location[1].to_json() for location in locations]

    print(json.dumps(body, indent=4))
    LOG.info("> Registering new product...")
    results = {}
    try:
        results: dict = self._post(endpoint, body)
    except Exception as exp:
        LOG.error(">>> Failed to register product: %s", str(exp.args))
        raise exp

    asset_list = []
    if isinstance(results, dict) and "assets" in results:
        asset_list = [Asset(asset) for asset in results["assets"]]
    else:
        raise Exception("Inexpected response from API:/n%s", results)
    for asset in asset_list:
        if asset.status == "Registered":
            for unit in units:
                if asset.serialNumber == unit.serialNumber:
                    break
                return False
    return True
