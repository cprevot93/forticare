# -*- coding: utf-8 -*-

"""asset.py: Objects used in FortiCare API"""

from datetime import datetime
from typing import Union

__author__ = "Charles Prevot"
__copyright__ = "Copyright 2023"


class Entitlement(object):
    """FortiCare Entitlement object"""

    def __init__(self, json: dict):
        self._start_date = datetime.strptime(str(json.get("startDate")), "%Y-%m-%dT%H:%M:%S")
        self._end_date = datetime.strptime(str(json.get("endDate")), "%Y-%m-%dT%H:%M:%S")
        self._level = json.get("level")
        self._level_desc = json.get("levelDesc")
        self._type = json.get("type")
        self._type_desc = json.get("typeDesc")

    @property
    def start_date(self) -> datetime:
        """Get entitlement start date"""
        return self._start_date

    @property
    def end_date(self) -> datetime:
        """Get entitlement end date"""
        return self._end_date

    @property
    def level(self) -> int:
        """Get entitlement level"""
        return self._level

    @property
    def level_desc(self) -> str:
        """Get entitlement level description"""
        return self._level_desc

    @property
    def type(self) -> int:
        """Get entitlement type"""
        return self._type

    @property
    def type_desc(self) -> str:
        """Get entitlement type description"""
        return self._type_desc

    def __str__(self) -> str:
        return f"Entitlement: {self.type_desc}"

    def __eq__(self, other) -> bool:
        if self.type == other.type and self.level == other.level and self.end_date == other.end_date:
            return True
        return False


class Asset(object):
    """FortiCare Asset object"""

    def __init__(self, json: dict):
        self._description = json.get("description", "")
        self._is_decommissioned = json.get("isDecommissioned", "")
        self._product_model = json.get("productModel", "")
        self._registration_date = None
        if json.get("registrationDate"):
            self._registration_date = datetime.strptime(str(json.get("registrationDate")), "%Y-%m-%dT%H:%M:%S")
        self._serial_number = json.get("serialNumber", "")
        self._entitlements = []
        for entitlement in json.get("entitlements"):
            self._entitlements.append(Entitlement(entitlement))
        self._warranty_supports = json.get("warrantySupports", "")
        self._asset_groups = json.get("assetGroups", "")
        self._contracts = json.get("contracts", "")
        self._product_model_eor = json.get("productModelEoR", "")
        self._product_model_eos = json.get("productModelEoS", "")
        self._license = json.get("license", "")
        self._location = json.get("location", "")
        self._partner = json.get("partner", "")
        self._folder_id = json.get("folderId", "")
        self._folder_path = json.get("folderPath", "")

    @property
    def description(self) -> str:
        """Get asset description"""
        return self._description

    @property
    def is_decommissioned(self) -> bool:
        """Get asset decommissioned status"""
        return self._is_decommissioned

    @property
    def product_model(self) -> str:
        """Get asset product model"""
        return self._product_model

    @property
    def registration_date(self) -> Union[datetime, None]:
        """Get asset registration date"""
        return self._registration_date

    @property
    def serial_number(self) -> str:
        """Get asset serial number"""
        return self._serial_number

    @property
    def entitlements(self) -> list[Entitlement]:
        """Get asset entitlements"""
        return self._entitlements

    @property
    def warranty_supports(self) -> str:
        """Get asset warranty supports"""
        return self._warranty_supports

    @property
    def asset_groups(self) -> str:
        """Get asset asset groups"""
        return self._asset_groups

    @property
    def contracts(self) -> str:
        """Get asset contracts"""
        return self._contracts

    @property
    def product_model_eor(self) -> str:
        """Get asset product model EOR"""
        return self._product_model_eor

    @property
    def product_model_eos(self) -> str:
        """Get asset product model EOS"""
        return self._product_model_eos

    @property
    def license(self) -> str:
        """Get asset license"""
        return self._license

    @property
    def location(self) -> str:
        """Get asset location"""
        return self._location

    @property
    def partner(self) -> str:
        """Get asset partner"""
        return self._partner

    @property
    def folder_id(self) -> int:
        """Get asset folder ID"""
        return self._folder_id

    @property
    def folder_path(self) -> str:
        """Get asset folder path"""
        return self._folder_path

    def __str__(self) -> str:
        return f"Asset: {self.product_model} - {self.serial_number}"

    def __eq__(self, other) -> bool:
        if self.serial_number == other.serial_number:
            return True
        return False
