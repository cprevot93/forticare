# -*- coding: utf-8 -*-

"""location.py: Objects used in FortiCare API"""

__author__ = "Charles Prevot"
__copyright__ = "Copyright 2023"


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
        postal_code: str = "",
        country_code: str = "",
        city: str = "",
        state_or_province: str = "",
        company: str = "",
        email: str = "",
        phone: str = "",
        fax: str = "",
    ):
        self._company = company
        self._address = address
        self._city = city
        self._state_or_province = state_or_province
        self._country_code = country_code
        self._postal_code = postal_code
        self._email = email
        self._phone = phone
        self._fax = fax

    @property
    def company(self) -> str:
        """Company"""
        return self._company

    @property
    def address(self) -> str:
        """Address"""
        return self._address

    @property
    def city(self) -> str:
        """City"""
        return self._city

    @property
    def stateOrProvince(self) -> str:
        """State or province"""
        return self._state_or_province

    @property
    def countryCode(self) -> str:
        """Country code"""
        return self._country_code

    @property
    def postalCode(self) -> str:
        """Postal code"""
        return self._postal_code

    @property
    def email(self) -> str:
        """Email"""
        return self._email

    @property
    def phone(self) -> str:
        """Phone"""
        return self._phone

    @property
    def fax(self) -> str:
        """Fax"""
        return self._fax

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

    def from_json(self, json: dict) -> None:
        """Populate from JSON object"""
        self._company = json.get("company", "")
        self._address = json.get("address", "")
        self._city = json.get("city", "")
        self._state_or_province = json.get("stateOrProvince", "")
        self._country_code = json.get("countryCode", "")
        self._postal_code = json.get("postalCode", "")
        self._email = json.get("email", "")
        self._phone = json.get("phone", "")
        self._fax = json.get("fax", "")

    def __str__(self) -> str:
        return f"Location({self._address}, {self._city}, {self._state_or_province} {self._country_code} {self._postal_code})"

    def __repr__(self) -> str:
        return f"Location({self._address})"

    def __eq__(self, other) -> bool:
        return (
            self._address == other._address
            and self._postal_code == other._postal_code
            and self._country_code == other._country_code
        )

    def __hash__(self) -> int:
        return hash(self._address + self._postal_code + self._country_code)
