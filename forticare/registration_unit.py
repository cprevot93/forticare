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
        serial_number: str,
        description: str = "",
        is_government: bool = False,
        additional_info: str = "",
        folder_id: str = "",
        asset_group_ids: str = "",
        replaced_serial_number: str = "",
        cloud_key: str = "",
        location: dict = {},
    ):
        self._serial_number = serial_number
        self._description = description
        self._is_government = is_government
        self._additional_info = additional_info
        self._folder_id = folder_id
        self._asset_group_ids = asset_group_ids
        self._replaced_serial_number = replaced_serial_number
        self._cloud_key = cloud_key
        self._location = location

        if self._serial_number == "":
            raise Exception("Serial number is empty")

    @property
    def serialNumber(self) -> str:
        """Serial number"""
        return self._serial_number

    @property
    def description(self) -> str:
        """Description"""
        return self._description

    @property
    def isGovernment(self) -> bool:
        """Is government"""
        return self._is_government

    @property
    def additionalInfo(self) -> str:
        """Additional information"""
        return self._additional_info

    @property
    def folderId(self) -> str:
        """Folder ID"""
        return self._folder_id

    @property
    def assetGroupIds(self) -> str:
        """Asset group IDs"""
        return self._asset_group_ids

    @property
    def replacedSerialNumber(self) -> str:
        """Replaced serial number"""
        return self._replaced_serial_number

    @property
    def cloudKey(self) -> str:
        """Cloud key"""
        return self._cloud_key

    @property
    def location(self) -> dict:
        """Location"""
        return self._location

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

    def from_json(self, json: dict):
        """Populate from JSON object"""
        self._serial_number = json.get("serialNumber", "")
        self._description = json.get("description", "")
        self._is_government = json.get("isGovernment", False)
        self._additional_info = json.get("additionalInfo", "")
        self._folder_id = json.get("folderId", "")
        self._asset_group_ids = json.get("assetGroupIds", "")
        self._replaced_serial_number = json.get("replacedSerialNumber", "")
        self._cloud_key = json.get("cloudKey", "")
        self._location = json.get("location", {})

    def __str__(self) -> str:
        return f"RegistrationUnits(sn={self.serialNumber})"


class LicenseRegistrationUnit(RegistrationUnit):
    """
    License registration units object
    """

    def __init__(self, licence_registration_code: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._license_registration_code = licence_registration_code

    @property
    def licenseRegistrationCode(self) -> str:
        """License registration code"""
        return self._license_registration_code

    def to_json(self) -> dict:
        """Return JSON object"""
        body = super().to_json()
        if self.licenseRegistrationCode != "":
            body["licenseRegistrationCode"] = str(self.licenseRegistrationCode)
        return dict(sorted(body.items()))

    def from_json(self, json: dict):
        """Populate from JSON object"""
        super().from_json(json)
        self._license_registration_code = json.get("licenseRegistrationCode", "")

    def __str__(self) -> str:
        return f"LicenseRegistrationUnits(code={self._license_registration_code})"

    def __eq__(self, other) -> bool:
        return self._license_registration_code == other._license_registration_code

    def __hash__(self) -> int:
        return hash(self._license_registration_code)


class ProductRegistrationUnit(RegistrationUnit):
    """
    Product registration units object
    """

    def __init__(self, contract_number: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._contract_number = contract_number

    @property
    def contractNumber(self) -> str:
        """Contract number"""
        return self._contract_number

    def to_json(self) -> dict:
        """Return JSON object"""
        body = super().to_json()
        if self.contractNumber != "":
            body["contractNumber"] = str(self.contractNumber)
        return dict(sorted(body.items()))

    def from_json(self, json: dict):
        """Populate from JSON object"""
        super().from_json(json)
        self._contract_number = json.get("contractNumber", "")

    def __str__(self) -> str:
        return f"ProductRegistrationUnits(contract={self._contract_number})"

    def __eq__(self, other) -> bool:
        return self._contract_number == other._contract_number

    def __hash__(self) -> int:
        return hash(self._contract_number)


class ServiceRegistrationUnit(object):
    """FortiCare Registration Units Service object"""

    def __init__(
        self,
        contract_number: str,
        description: str = "",
        is_government: bool = False,
        additional_info: str = "",
    ):
        self._contract_number = contract_number
        self._description = description
        self._is_government = is_government
        self._additional_info = additional_info

        if self._contract_number == "":
            raise ValueError("Contract number is empty")

    @property
    def contractNumber(self) -> str:
        """Contract number"""
        return self._contract_number

    @property
    def description(self) -> str:
        """Description"""
        return self._description

    @property
    def isGovernment(self) -> bool:
        """Is government"""
        return self._is_government

    @property
    def additionalInfo(self) -> str:
        """Additional information"""
        return self._additional_info

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

    def from_json(self, json: dict):
        """Populate from JSON object"""
        self._contract_number = json.get("contractNumber", "")
        self._description = json.get("description", "")
        self._is_government = json.get("isGovernment", False)
        self._additional_info = json.get("additionalInfo", "")

    def __str__(self) -> str:
        return f"ServiceRegistrationUnits(contract={self._contract_number})"

    def __eq__(self, other) -> bool:
        return self._contract_number == other._contrat_number

    def __hash__(self) -> int:
        return hash(self._contract_number)

    def __repr__(self) -> str:
        return self.__str__()
