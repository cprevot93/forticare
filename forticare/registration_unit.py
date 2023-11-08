# -*- coding: utf-8 -*-

"""registration_unit.py: Objects used in FortiCare API"""

__author__ = "Charles Prevot"
__copyright__ = "Copyright 2023"


# {
#   "serialNumber": "{{serial}}",
#   "contractNumber": "", // only for product registration
#   "licenseRegistrationCode": "<string>", // only for license registration
#   "description": "",
#   "isGovernment": false
#   "additionalInfo": "<string>",
#   "folderId": "<number>",
#   "assetGroupIds": "<string>",
#   "replacedSerialNumber": "<string>",
#   "cloudKey": "<string>",
#   "location": {
#     "ref": "<string>"
#   }
class RegistrationUnit(object):
    """FortiCare Registration Units object"""

    def __init__(
        self,
        serialNumber: str,
        description: str = "",
        isGovernment: bool = False,
        additionalInfo: str = "",
        folderId: str = "",
        assetGroupIds: str = "",
        replacedSerialNumber: str = "",
        cloudKey: str = "",
        location: dict = {},
    ):
        self.serialNumber = serialNumber
        self.description = description
        self.isGovernment = isGovernment
        self.additionalInfo = additionalInfo
        self.folderId = folderId
        self.assetGroupIds = assetGroupIds
        self.replacedSerialNumber = replacedSerialNumber
        self.cloudKey = cloudKey
        self.location = location

        if self.serialNumber == "":
            raise Exception("Serial number is empty")

    def to_json(self) -> dict:
        """Return JSON object"""
        body = {
            "description": self.description,
            "isGovernment": self.isGovernment,
        }
        if self.serialNumber != "":
            body["serialNumber"] = str(self.serialNumber)
        if self.additionalInfo != "":
            body["additionalInfo"] = str(self.additionalInfo)
        if self.folderId != "":
            body["folderId"] = str(self.folderId)
        if self.assetGroupIds != "":
            body["assetGroupIds"] = str(self.assetGroupIds)
        if self.replacedSerialNumber != "":
            body["replacedSerialNumber"] = str(self.replacedSerialNumber)
        if self.cloudKey != "":
            body["cloudKey"] = str(self.cloudKey)
        if self.location != {}:
            body["location"] = self.location
        return body

    def __str__(self) -> str:
        return f"RegistrationUnits(sn={self.serialNumber})"


class LicenseRegistrationUnit(RegistrationUnit):
    """
    License registration units object
    """

    def __init__(self, licenseRegistrationCode: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.licenseRegistrationCode = licenseRegistrationCode

    def to_json(self) -> dict:
        """Return JSON object"""
        body = super().to_json()
        if self.licenseRegistrationCode != "":
            body["licenseRegistrationCode"] = str(self.licenseRegistrationCode)
        return dict(sorted(body.items()))

    def __str__(self) -> str:
        return f"LicenseRegistrationUnits(code={self.licenseRegistrationCode})"

    def __eq__(self, other) -> bool:
        return self.licenseRegistrationCode == other._license_registration_code

    def __hash__(self) -> int:
        return hash(self.licenseRegistrationCode)


class ProductRegistrationUnit(RegistrationUnit):
    """
    Product registration units object
    """

    def __init__(self, contractNumber: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.contractNumber = contractNumber

    def to_json(self) -> dict:
        """Return JSON object"""
        body = super().to_json()
        if self.contractNumber != "":
            body["contractNumber"] = str(self.contractNumber)
        return dict(sorted(body.items()))

    def __str__(self) -> str:
        return f"ProductRegistrationUnits(contract={self.contractNumber})"

    def __eq__(self, other) -> bool:
        return self.contractNumber == other._contract_number

    def __hash__(self) -> int:
        return hash(self.contractNumber)


class ServiceRegistrationUnit(object):
    """FortiCare Registration Units Service object"""

    def __init__(
        self,
        contractNumber: str,
        description: str = "",
        isGovernment: bool = False,
        additionalInfo: str = "",
    ):
        self.contractNumber = contractNumber
        self.description = description
        self.isGovernment = isGovernment
        self.additionalInfo = additionalInfo

        if self.contractNumber == "":
            raise ValueError("Contract number is empty")

    def to_json(self) -> dict:
        """Return JSON object"""
        body = {
            "description": self.description,
            "contractNumber": self.contractNumber,
            "isGovernment": self.isGovernment,
        }
        if self.additionalInfo != "":
            body["additionalInfo"] = str(self.additionalInfo)
        return dict(sorted(body.items()))

    def __str__(self) -> str:
        return f"ServiceRegistrationUnits(contract={self.contractNumber})"

    def __eq__(self, other) -> bool:
        return self.contractNumber == other._contrat_number

    def __hash__(self) -> int:
        return hash(self.contractNumber)

    def __repr__(self) -> str:
        return self.__str__()
