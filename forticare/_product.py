# -*- coding: utf-8 -*-

"""_product.py: ."""

from ._helpers import *
import uuid
import logging
from datetime import datetime

from .asset import Asset, Entitlement

__author__ = "Charles Prevot"
__copyright__ = "Copyright 2023"

LOG = logging.getLogger()


def get_product_licenses(
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
    results = None
    try:
        results = self._post(endpoint, body)
    except Exception as exp:
        LOG.error(">>> Failed to retrive assets: %s", str(exp.args))
        raise exp

    return [Asset(asset) for asset in results["assets"]]


def get_product_details(self, serial_number: str) -> Asset:
    """
    Returns product details based on product SN.
    :param serial_number: Serial number or serial number search pattern
    :type serial_number: str
    :return Asset: Return an asset
    """
    endpoint = "/products/details"
    body = {"serialNumber": str(serial_number)}

    LOG.info("> Retriving asset details...")
    results = None
    try:
        results = self._post(endpoint, body)
    except Exception as exp:
        LOG.error(">>> Failed to retrive asset details: %s", str(exp.args))
        raise exp

    return Asset(results)
