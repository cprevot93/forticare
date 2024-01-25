# -*- coding: utf-8 -*-

"""location.py: Objects used in FortiCare API"""

__author__ = "Charles Prevot"
__copyright__ = "Copyright 2024"


# {
#   "company": "<string>",
#   "address": "<string>",
#   "city": "<string>",
#   "stateOrProvince": "<string>",
#   "countryCode": "<string>",
#   "postalCode": "<string>",
#   "email": "<string>",
#   "phone": "<string>",
#   "fax": "<string>"
# }
class Location(object):
    """FortiCare Location object"""

    def __init__(
        self,
        address: str = "",
        postalCode: str = "",
        countryCode: str = "",
        city: str = "",
        stateOrProvince: str = "",
        company: str = "",
        email: str = "",
        phone: str = "",
        fax: str = "",
    ):
        self.company = company
        self.address = address
        self.city = city
        self.stateOrProvince = stateOrProvince
        self.countryCode = countryCode
        self.postalCode = postalCode
        self.email = email
        self.phone = phone
        self.fax = fax

    def to_json(self) -> dict:
        """Return JSON object"""
        body = {}
        if self.company != "":
            body["company"] = str(self.company)
        if self.address != "":
            body["address"] = str(self.address)
        if self.city != "":
            body["city"] = str(self.city)
        if self.stateOrProvince != "":
            body["stateOrProvince"] = str(self.stateOrProvince)
        if self.countryCode != "":
            body["countryCode"] = str(self.countryCode)
        if self.postalCode != "":
            body["postalCode"] = str(self.postalCode)
        if self.email != "":
            body["email"] = str(self.email)
        if self.phone != "":
            body["phone"] = str(self.phone)
        if self.fax != "":
            body["fax"] = str(self.fax)
        return body

    def __str__(self) -> str:
        return f"Location({self.address}, {self.city}, {self.stateOrProvince} {self.countryCode} {self.postalCode})"

    def __repr__(self) -> str:
        return f"Location({self.address})"

    def __eq__(self, other) -> bool:
        return (
            self.address == other.address
            and self.postalCode == other.postalCode
            and self.countryCode == other.countryCode
        )

    def __hash__(self) -> int:
        return hash(self.address + self.postalCode + self.countryCode)
