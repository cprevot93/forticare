# -*- coding: utf-8 -*-

"""asset.py: Objects used in FortiCare API"""

from datetime import datetime
from typing import Union

__author__ = "Charles Prevot"
__copyright__ = "Copyright 2023"


# {
#     "licenseNumber": "FMCLD4713562246",
#     "licenseSKU": "FMG-VM-CLOUD",
#     "serialNumber": "FMGVCLTM20000051",
#     "status": "Registered"
# },
class License(object):
    """FortiCare License object"""

    def __init__(self, json: dict):
        self._license_number = json.get("licenseNumber", "")
        self._license_sku = json.get("licenseSKU", "")
        self._serial_number = json.get("serialNumber", "")
        self._status = json.get("status", "")

    @property
    def license_number(self) -> str:
        """Get license number"""
        return self._license_number

    @property
    def license_sku(self) -> str:
        """Get license SKU"""
        return self._license_sku

    @property
    def serial_number(self) -> str:
        """Get serial number"""
        return self._serial_number

    @property
    def status(self) -> str:
        """Get status"""
        return self._status

    def to_json(self) -> dict:
        """Get object as json"""
        return {
            "licenseNumber": self.license_number,
            "licenseSKU": self.license_sku,
            "serialNumber": self.serial_number,
            "status": self.status,
        }

    def __str__(self) -> str:
        return f"License: {self.license_sku} - {self.license_number}"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        if self.serial_number == other.serial_number:
            return True
        return False

    def __hash__(self) -> int:
        return hash(self.serial_number)


class Service(object):
    """FortiCare Entitlement or Warranty object"""

    def __init__(self, json: dict):
        self._start_date = datetime.strptime(str(json.get("startDate")), "%Y-%m-%dT%H:%M:%S")
        self._end_date = datetime.strptime(str(json.get("endDate")), "%Y-%m-%dT%H:%M:%S")
        self._level = json.get("level")
        self._level_desc = json.get("levelDesc")
        self._type = json.get("type")
        self._type_desc = json.get("typeDesc")

    @property
    def start_date(self) -> datetime:
        """Get service start date"""
        return self._start_date

    @property
    def end_date(self) -> datetime:
        """Get service end date"""
        return self._end_date

    @property
    def level(self) -> int:
        """Get service level"""
        return self._level

    @property
    def level_desc(self) -> str:
        """Get service level description"""
        return self._level_desc

    @property
    def type(self) -> int:
        """Get service type"""
        return self._type

    @property
    def type_desc(self) -> str:
        """Get service type description"""
        return self._type_desc

    def to_json(self) -> dict:
        """Get object as json"""
        return {
            "startDate": self.start_date,
            "endDate": self.end_date,
            "level": self.level,
            "levelDesc": self.level_desc,
            "type": self.type,
            "typeDesc": self.type_desc,
        }

    def __str__(self) -> str:
        return f"Entitlement: {self.type_desc}"

    def __eq__(self, other) -> bool:
        if self.type == other.type and self.level == other.level and self.end_date == other.end_date:
            return True
        return False


class Term(object):
    """FortiCare Term object"""

    def __init__(self, json: dict) -> None:
        # {
        #     "endDate": "2021-09-23T00:00:00",
        #     "startDate": "2020-09-23T00:00:00",
        #     "supportType": "Telephone Support",
        # },
        self._start_date = datetime.strptime(str(json.get("startDate")), "%Y-%m-%dT%H:%M:%S")
        self._end_date = datetime.strptime(str(json.get("endDate")), "%Y-%m-%dT%H:%M:%S")
        self._support_type = json.get("supportType", "")

    @property
    def start_date(self) -> datetime:
        """Get service start date"""
        return self._start_date

    @property
    def end_date(self) -> datetime:
        """Get service end date"""
        return self._end_date

    @property
    def support_type(self) -> str:
        """Get service support type"""
        return self._support_type

    def to_json(self) -> dict:
        """Get object as json"""
        return {
            "startDate": self.start_date,
            "endDate": self.end_date,
            "supportType": self.support_type,
        }

    def __str__(self) -> str:
        return f"Term: {self.support_type}"

    def __repr__(self) -> str:
        return self.__str__()


class Contract(object):
    """FortiCare Contract object"""

    def __init__(self, json: dict) -> None:
        # {
        #     "contractNumber": "5762CL381100",
        #     "sku": "FC2-10-CGSLB-330-02-12",
        #     "terms": [
        #         {
        #             "endDate": "2021-09-23T00:00:00",
        #             "startDate": "2020-09-23T00:00:00",
        #             "supportType": "Telephone Support",
        #         },
        #         {
        #             "endDate": "2021-09-23T00:00:00",
        #             "startDate": "2020-09-23T00:00:00",
        #             "supportType": "Enhanced Support",
        #         },
        #     ],
        # },
        self._contract_number = json.get("contractNumber", "")
        self._sku = json.get("sku", "")
        self._terms = []
        for term in json.get("terms", []):
            self._terms.append(Term(term))

    @property
    def contract_number(self) -> str:
        """Get contract number"""
        return self._contract_number

    @property
    def sku(self) -> str:
        """Get SKU"""
        return self._sku

    @property
    def terms(self) -> list[Term]:
        """Get terms"""
        return self._terms

    def to_json(self) -> dict:
        """Get object as json"""
        return {
            "contractNumber": self.contract_number,
            "sku": self.sku,
            "terms": [term.to_json() for term in self.terms],
        }

    def __str__(self) -> str:
        return f"Contract: {self.sku} - {self.contract_number}"

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return hash(self.contract_number)

    def __eq__(self, other) -> bool:
        if self.contract_number == other.contract_number:
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
        for entitlement in json.get("entitlements", []):
            self._entitlements.append(Service(entitlement))
        __warranty_supports = json.get("warrantySupports", [])
        self._warranty_supports = []
        if __warranty_supports:
            for warranty_support in __warranty_supports:
                self._warranty_supports.append(Service(warranty_support))
        self._asset_groups = json.get("assetGroups", [])
        __contracts = json.get("contracts", [])
        self._contracts = []
        if __contracts:
            for contract in json.get("contracts", []):
                self._contracts.append(Contract(contract))
        self._product_model_eor = json.get("productModelEoR", "")
        self._product_model_eos = json.get("productModelEoS", "")
        __licenses = json.get("licenses", [])
        self._licenses = []
        if __licenses:
            for license in __licenses:
                self._licenses.append(License(license))
        self._location = json.get("location", "")
        self._partner = json.get("partner", "")
        self._folder_id = json.get("folderId", "")
        self._folder_path = json.get("folderPath", "")
        self._status = json.get("status", "")

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
    def entitlements(self) -> list[Service]:
        """Get asset entitlements"""
        return self._entitlements

    @property
    def warranty_supports(self) -> list[Service]:
        """Get asset warranty supports"""
        return self._warranty_supports

    @property
    def asset_groups(self) -> str:
        """Get asset asset groups"""
        return self._asset_groups

    @property
    def contracts(self) -> list[Contract]:
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
    def licenses(self) -> list[License]:
        """Get asset license"""
        return self._licenses

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

    @property
    def status(self) -> str:
        """Get asset status"""
        return self._status

    def to_json(self) -> dict:
        """Get object as json"""
        return {
            "assetGroups": self.asset_groups,
            "contracts": [contract.to_json() for contract in self.contracts],
            "description": self.description,
            "entitlements": [entitlement.to_json() for entitlement in self.entitlements],
            "folderId": self.folder_id,
            "folderPath": self.folder_path,
            "isDecommissioned": self.is_decommissioned,
            "licenses": [license.to_json() for license in self.licenses],
            "location": self.location,
            "partner": self.partner,
            "productModel": self.product_model,
            "productModelEoR": self.product_model_eor,
            "productModelEoS": self.product_model_eos,
            "registrationDate": self.registration_date,
            "serialNumber": self.serial_number,
            "warrantySupports": [warranty_support.to_json() for warranty_support in self.warranty_supports],
            "status": self.status,
        }

    def __str__(self) -> str:
        return f"Asset: {self.product_model} - {self.serial_number}"

    def __repr__(self) -> str:
        return f"Asset({self.serial_number}, {self.product_model})"

    def __eq__(self, other) -> bool:
        if self.serial_number == other.serial_number:
            return True
        return False
