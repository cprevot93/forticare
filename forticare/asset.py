# -*- coding: utf-8 -*-

"""asset.py: Objects used in FortiCare API"""

from datetime import datetime
from typing import Union

__author__ = "Charles Prevot"
__copyright__ = "Copyright 2023"


def parse_datetime(date: str) -> datetime:
    """Parse date string to datetime object"""
    if date is None:
        raise ValueError("Invalid date format: None")
    _formats = ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S%z"]
    for _f in _formats:
        try:
            return datetime.strptime(str(date), _f)
        except ValueError:
            continue
    raise ValueError(f"Invalid date format: {date}")


# {
#     "licenseNumber": "FMCLD4713562246",
#     "licenseSKU": "FMG-VM-CLOUD",
#     "serialNumber": "FMGVCLTM20000051",
#     "status": "Registered"
# }
class License(object):
    """FortiCare License object"""

    def __init__(self, json: dict):
        self.licenseNumber = json.get("licenseNumber", "")
        self.licenseSKU = json.get("licenseSKU", "")
        self.serialNumber = json.get("serialNumber", "")
        self.status = json.get("status", "")

    def to_json(self) -> dict:
        """Get object as json"""
        return {
            "licenseNumber": self.licenseNumber,
            "licenseSKU": self.licenseSKU,
            "serialNumber": self.serialNumber,
            "status": self.status,
        }

    def __str__(self) -> str:
        return f"License: {self.licenseSKU} - {self.licenseNumber}"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        if self.serialNumber == other.serial_number:
            return True
        return False

    def __hash__(self) -> int:
        return hash(self.serialNumber)


class Service(object):
    """FortiCare Entitlement or Warranty object"""

    def __init__(self, json: dict):
        self.startDate = parse_datetime(json.get("startDate", None))
        self.endDate = parse_datetime(json.get("endDate", None))
        self.level = json.get("level")
        self.levelDesc = json.get("levelDesc")
        self.type = json.get("type")
        self.typeDesc = json.get("typeDesc")

    def to_json(self) -> dict:
        """Get object as json"""
        return {
            "startDate": self.startDate.strftime("%Y-%m-%dT%H:%M:%S"),
            "endDate": self.endDate.strftime("%Y-%m-%dT%H:%M:%S"),
            "level": self.level,
            "levelDesc": self.levelDesc,
            "type": self.type,
            "typeDesc": self.typeDesc,
        }

    def __str__(self) -> str:
        return f"Entitlement: {self.typeDesc}"

    def __eq__(self, other) -> bool:
        if self.type == other.type and self.level == other.level and self.endDate == other.end_date:
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
        self.startDate = parse_datetime(json.get("startDate", None))
        self.endDate = parse_datetime(json.get("endDate", None))
        self.supportType = json.get("supportType", "")

    def to_json(self) -> dict:
        """Get object as json"""
        return {
            "startDate": self.startDate.strftime("%Y-%m-%dT%H:%M:%S"),
            "endDate": self.endDate.strftime("%Y-%m-%dT%H:%M:%S"),
            "supportType": self.supportType,
        }

    def __str__(self) -> str:
        return f"Term: {self.supportType}"

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
        self.contractNumber = json.get("contractNumber", "")
        self.sku = json.get("sku", "")
        self.terms = []
        for term in json.get("terms", []):
            self.terms.append(Term(term))

    def to_json(self) -> dict:
        """Get object as json"""
        return {
            "contractNumber": self.contractNumber,
            "sku": self.sku,
            "terms": [term.to_json() for term in self.terms],
        }

    def __str__(self) -> str:
        return f"Contract: {self.sku} - {self.contractNumber}"

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return hash(self.contractNumber)

    def __eq__(self, other) -> bool:
        if self.contractNumber == other.contract_number:
            return True
        return False


class AssetGroup(object):
    """FortiCare Asset Group object"""

    def __init__(self, json: dict) -> None:
        # {"assetGroupId": "<integer>", "assetGroup": "<string>"},
        self.assetGroupId = json.get("assetGroupId", 0)
        self.assetGroup = json.get("assetGroup", "")

    def to_json(self) -> dict:
        """Get object as json"""
        return {
            "assetGroupId": self.assetGroupId,
            "assetGroup": self.assetGroup,
        }

    def __str__(self) -> str:
        return f"AssetGroup: {self.assetGroup}"

    def __repr__(self) -> str:
        return self.__str__()


class Asset(object):
    """FortiCare Asset object"""

    def __init__(self, json: dict):
        self.description = json.get("description", "")
        self.isDecommissioned = json.get("isDecommissioned", "")
        self.productModel = json.get("productModel", "")
        self.registrationDate = parse_datetime(json.get("registrationDate", None))
        self.serialNumber = json.get("serialNumber", "")
        self.entitlements = []
        for entitlement in json.get("entitlements", []):
            self.entitlements.append(Service(entitlement))
        __warranty_supports = json.get("warrantySupports", [])
        self.warrantySupports = []
        if __warranty_supports:
            for warranty_support in __warranty_supports:
                self.warrantySupports.append(Service(warranty_support))
        __asset_groups = json.get("assetGroups", [])
        self.assetGroups = []
        if __asset_groups:
            for asset_group in __asset_groups:
                self.assetGroups.append(AssetGroup(asset_group))
        __contracts = json.get("contracts", [])
        self.contracts = []
        if __contracts:
            for contract in json.get("contracts", []):
                self.contracts.append(Contract(contract))
        self.productModelEor = json.get("productModelEoR", "")
        self.productModelEos = json.get("productModelEoS", "")
        __licenses = json.get("licenses", [])
        self.licenses = []
        if __licenses:
            for license in __licenses:
                self.licenses.append(License(license))
        self.location = json.get("location", "")
        self.partner = json.get("partner", "")
        self.folderId = json.get("folderId", "")
        self.folderPath = json.get("folderPath", "")
        self.status = json.get("status", "")

    def to_json(self) -> dict:
        """Get object as json"""
        return {
            "assetGroups": [asset_group.to_json() for asset_group in self.assetGroups],
            "contracts": [contract.to_json() for contract in self.contracts],
            "description": self.description,
            "entitlements": [entitlement.to_json() for entitlement in self.entitlements],
            "folderId": self.folderId,
            "folderPath": self.folderPath,
            "isDecommissioned": self.isDecommissioned,
            "licenses": [license.to_json() for license in self.licenses],
            "location": self.location,
            "partner": self.partner,
            "productModel": self.productModel,
            "productModelEoR": self.productModelEor,
            "productModelEoS": self.productModelEos,
            "registrationDate": self.registrationDate.strftime("%Y-%m-%dT%H:%M:%S"),
            "serialNumber": self.serialNumber,
            "warrantySupports": [warranty_support.to_json() for warranty_support in self.warrantySupports],
            "status": self.status,
        }

    def __str__(self) -> str:
        return f"Asset: {self.productModel} - {self.serialNumber}"

    def __repr__(self) -> str:
        return f"Asset({self.serialNumber}, {self.productModel})"

    def __eq__(self, other) -> bool:
        if self.serialNumber == other.serialNumber:
            return True
        return False
