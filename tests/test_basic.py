# -*- coding: utf-8 -*-
from unittest.mock import patch

from tests.context import (
    API_USERNAME,
    API_PASSWORD,
    Asset,
    Service,
    FortiCare,
    Location,
    License,
    LicenseRegistrationUnit,
    ProductRegistrationUnit,
    ServiceRegistrationUnit,
)

import unittest
import datetime as dt


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def __init__(self, *args, **kwargs):
        self.forticare = FortiCare(API_USERNAME, API_PASSWORD, True)
        self.forticare.login()
        super(BasicTestSuite, self).__init__(*args, **kwargs)

    def setUp(self) -> None:
        return super().setUp()

    def test_login_token(self):
        token = ""
        try:
            token = self.forticare.token
        except Exception as exp:
            print(str(exp.args))
        assert token  # <> None

    def test_invalid_cred(self):
        res = self.forticare.login(API_USERNAME, "toto")
        assert res is False

    def test_auto_login(self):
        with self.subTest("Test auto login True"):
            self.forticare._auto_login = True
            self.forticare.token = None
            res = self.forticare.get_products(dt.datetime(2023, 1, 1))
            print(res)
            self.assertTrue(res)
            self.assertTrue(isinstance(res, list))

        with self.subTest("Test auto login False"):
            self.forticare._auto_login = False
            self.forticare.token = None
            with self.assertRaises(ValueError):
                res = self.forticare.get_products(dt.datetime(2023, 1, 1))
                print(res)

        with self.subTest("Test auto login True and change token to an invalid one"):
            self.forticare._auto_login = True
            self.forticare.token = "toto"
            res = self.forticare.get_products(dt.datetime(2023, 1, 1))
            print(res)
            self.assertTrue(res)
            self.assertTrue(isinstance(res, list))

    def test_asset_class(self):
        """ "Create an assert from a dict"""
        data = {
            "description": "",
            "entitlements": [
                {
                    "endDate": "2021-09-23T00:00:00",
                    "level": 20,
                    "levelDesc": "Premium",
                    "startDate": "2020-09-23T00:00:00",
                    "type": 11,
                    "typeDesc": "Enhanced Support",
                },
                {
                    "endDate": "2021-09-23T00:00:00",
                    "level": 20,
                    "levelDesc": "Premium",
                    "startDate": "2020-09-23T00:00:00",
                    "type": 12,
                    "typeDesc": "Telephone Support",
                },
                {
                    "endDate": "2021-09-23T00:00:00",
                    "level": 6,
                    "levelDesc": "Web/Online",
                    "startDate": "2020-09-23T00:00:00",
                    "type": 118,
                    "typeDesc": "FortiADC GSLB Cloud Service QPS",
                },
                {
                    "endDate": "2021-09-23T00:00:00",
                    "level": 6,
                    "levelDesc": "Web/Online",
                    "startDate": "2020-09-23T00:00:00",
                    "type": 120,
                    "typeDesc": "FortiADC GSLB Cloud Service checks",
                },
            ],
            "isDecommissioned": False,
            "productModel": "FortiGSLB Cloud",
            "registrationDate": "2020-09-23T02:46:42",
            "serialNumber": "FCGSLB0000000205",
            "warrantySupports": None,
            "assetGroups": [],
            "contracts": [
                {
                    "contractNumber": "5762CL381100",
                    "sku": "FC2-10-CGSLB-330-02-12",
                    "terms": [
                        {
                            "endDate": "2021-09-23T00:00:00",
                            "startDate": "2020-09-23T00:00:00",
                            "supportType": "Telephone Support",
                        },
                        {
                            "endDate": "2021-09-23T00:00:00",
                            "startDate": "2020-09-23T00:00:00",
                            "supportType": "Enhanced Support",
                        },
                        {
                            "endDate": "2021-09-23T00:00:00",
                            "startDate": "2020-09-23T00:00:00",
                            "supportType": "FortiADC GSLB Cloud Service QPS",
                        },
                    ],
                },
                {
                    "contractNumber": "1162XX438908",
                    "sku": "FC2-10-CGSLB-332-02-12",
                    "terms": [
                        {
                            "endDate": "2021-09-23T00:00:00",
                            "startDate": "2020-09-23T00:00:00",
                            "supportType": "Telephone Support",
                        },
                        {
                            "endDate": "2021-09-23T00:00:00",
                            "startDate": "2020-09-23T00:00:00",
                            "supportType": "Enhanced Support",
                        },
                        {
                            "endDate": "2021-09-23T00:00:00",
                            "startDate": "2020-09-23T00:00:00",
                            "supportType": "FortiADC GSLB Cloud Service checks",
                        },
                    ],
                },
            ],
            "productModelEoR": None,
            "productModelEoS": None,
            "status": "Registered",
        }
        asset = Asset(data)
        print(asset)
        self.assertTrue(asset)
        self.assertTrue(isinstance(asset, Asset))
        self.assertTrue(asset.serialNumber == "FCGSLB0000000205")
        self.assertTrue(asset.productModel == "FortiGSLB Cloud")
        self.assertTrue(asset.registrationDate == dt.datetime(2020, 9, 23, 2, 46, 42))
        self.assertTrue(asset.description == "")
        self.assertTrue(asset.isDecommissioned is False)
        self.assertTrue(isinstance(asset.entitlements, list))
        self.assertTrue(isinstance(asset.entitlements[1], Service))
        self.assertTrue(asset.entitlements[1].level == 20)
        self.assertTrue(asset.entitlements[1].levelDesc == "Premium")
        self.assertTrue(asset.entitlements[1].type == 12)
        self.assertTrue(asset.entitlements[1].typeDesc == "Telephone Support")
        self.assertTrue(asset.entitlements[1].startDate == dt.datetime(2020, 9, 23, 0, 0))
        self.assertTrue(asset.entitlements[1].endDate == dt.datetime(2021, 9, 23, 0, 0))
        self.assertTrue(isinstance(asset.entitlements[3], Service))
        self.assertTrue(asset.entitlements[3].level == 6)
        self.assertTrue(asset.entitlements[3].levelDesc == "Web/Online")
        self.assertTrue(asset.entitlements[3].type == 120)
        self.assertTrue(asset.entitlements[3].typeDesc == "FortiADC GSLB Cloud Service checks")
        self.assertTrue(asset.entitlements[3].startDate == dt.datetime(2020, 9, 23, 0, 0))
        self.assertTrue(asset.entitlements[3].endDate == dt.datetime(2021, 9, 23, 0, 0))
        self.assertTrue(isinstance(asset.warrantySupports, list))
        self.assertTrue(asset.warrantySupports == [])
        self.assertTrue(isinstance(asset.assetGroups, list))
        self.assertTrue(asset.assetGroups == [])
        self.assertTrue(isinstance(asset.contracts, list))
        self.assertTrue(isinstance(asset.contracts[0], dict))
        # self.assertTrue(asset.contracts[0]["contractNumber"] == "5762CL381100")
        # self.assertTrue(asset.contracts[0]["sku"] == "FC2-10-CGSLB-330-02-12")
        # self.assertTrue(isinstance(asset.contracts[0]["terms"], list))
        # self.assertTrue(isinstance(asset.contracts[0]["terms"][0], dict))
        # self.assertTrue(asset.contracts[0]["terms"][0]["endDate"] == dt.datetime(2021, 9, 23, 0, 0))
        # self.assertTrue(asset.contracts[0]["terms"][0]["startDate"] == dt.datetime(2020, 9, 23, 0, 0))
        # self.assertTrue(asset.contracts[0]["terms"][0]["supportType"] == "Telephone Support")
        # self.assertTrue(isinstance(asset.contracts[1], dict))
        # self.assertTrue(asset.contracts[1]["contractNumber"] == "1162XX438908")
        # self.assertTrue(asset.contracts[1]["sku"] == "FC2-10-CGSLB-332-02-12")
        # self.assertTrue(isinstance(asset.contracts[1]["terms"], list))
        # self.assertTrue(isinstance(asset.contracts[1]["terms"][0], dict))
        # self.assertTrue(asset.contracts[1]["terms"][0]["endDate"] == dt.datetime(2021, 9, 23, 0, 0))
        # self.assertTrue(asset.contracts[1]["terms"][0]["startDate"] == dt.datetime(2020, 9, 23, 0, 0))
        # self.assertTrue(asset.contracts[1]["terms"][0]["supportType"] == "Telephone Support")
        self.assertTrue(asset.productModelEor is None)
        self.assertTrue(asset.productModelEos is None)
        self.assertTrue(asset.status == "Registered")

    def test_service_class(self):
        data = {
            "endDate": "2021-09-23T00:00:00",
            "level": 20,
            "levelDesc": "Premium",
            "startDate": "2020-09-23T00:00:00",
            "type": 11,
            "typeDesc": "Enhanced Support",
        }
        service = Service(data)
        print(service)
        self.assertTrue(service)
        self.assertTrue(isinstance(service, Service))
        self.assertTrue(service.level == 20)
        self.assertTrue(service.levelDesc == "Premium")
        self.assertTrue(service.type == 11)
        self.assertTrue(service.typeDesc == "Enhanced Support")
        self.assertTrue(service.startDate == dt.datetime(2020, 9, 23, 0, 0))
        self.assertTrue(service.endDate == dt.datetime(2021, 9, 23, 0, 0))

    def test_location_class(self):
        data = {
            "company": "test",
            "address": "1 rue de la paix",
            "city": "Paris",
            "countryCode": "FR",
            "stateOrProvince": "Ile de France",
            "postalCode": "75000",
            "email": "test",
            "phone": "0123456789",
            "fax": "0123456789",
        }
        location = Location()
        location.from_json(data)
        print(location)
        self.assertTrue(location)
        self.assertTrue(isinstance(location, Location))
        self.assertTrue(location.company == "test")
        self.assertTrue(location.address == "1 rue de la paix")
        self.assertTrue(location.city == "Paris")
        self.assertTrue(location.countryCode == "FR")
        self.assertTrue(location.stateOrProvince == "Ile de France")
        self.assertTrue(location.postalCode == "75000")
        self.assertTrue(location.email == "test")
        self.assertTrue(location.phone == "0123456789")
        self.assertTrue(location.fax == "0123456789")

    def test_get_products(self):
        res = self.forticare.get_products(dt.datetime(2023, 1, 1))
        print(res)
        self.assertTrue(res)
        self.assertTrue(isinstance(res, list))

    def test_get_product_details(self):
        sn = "FCGSLB0000000205"
        res = self.forticare.get_product_details(sn)
        print(res)
        self.assertTrue(res)
        self.assertTrue(isinstance(res, Asset))
        self.assertTrue(res.serialNumber == sn)
        self.assertTrue(res.productModel == "FortiGSLB Cloud")

    def test_get_licenses(self):
        with self.subTest("Test without parameters"):
            res = self.forticare.get_licenses()
            print(res)
            self.assertTrue(res)
            self.assertTrue(isinstance(res, list))
            for _r in res:
                self.assertTrue(isinstance(_r, License))

        with self.subTest("Test with parameters"):
            license_number = "FMLVM4714475461"
            res = self.forticare.get_licenses(license_number=license_number)
            print(res)
            self.assertTrue(res)
            self.assertTrue(isinstance(res, list))
            self.assertTrue(isinstance(res[0], License))
            self.assertTrue(res[0].licenseNumber == license_number)

    def test_download_licenses(self):
        sn = "FEVM04TM23000333"
        res = self.forticare.download_licenses(sn)
        print(res)
        self.assertTrue(res)
        self.assertTrue(isinstance(res, str))
        self.assertTrue(res.startswith("-----BEGIN FE VM LICENSE-----\n"))

    def test_register_product(self):
        _ret = {
            "token": "JnMYRfKrLVStMHFxrf5fqtPPQpMbWN",
            "version": "3.0",
            "status": 200,
            "message": "Success",
            "build": "1.0.0",
            "error": None,
            "assets": [
                {
                    "serialNumber": "FEVM04TM23000333",
                    "folderId": 1,
                    "folderPath": "<string>",
                    "registrationDate": dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                    "description": "",
                    "isDecommissioned": False,
                    "status": "Registered",
                    "productModel": "<string>",
                    "productModelEoR": "<string>",
                    "productModelEoS": "<string>",
                    "entitlements": [
                        {
                            "level": 2,
                            "levelDesc": "",
                            "type": 2,
                            "typeDesc": "",
                            "startDate": dt.datetime.today().strftime("%Y-%m-%dT%H:%M:%S"),
                            "endDate": (dt.datetime.today() + dt.timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%S"),
                        },
                        {
                            "level": 1,
                            "levelDesc": "<string>",
                            "type": 1,
                            "typeDesc": "<string>",
                            "startDate": dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                            "endDate": (dt.datetime.today() + dt.timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%S"),
                        },
                    ],
                    "assetGroups": None,
                    "warrantySupports": None,
                }
            ],
        }
        with patch.object(FortiCare, "_post", return_value=_ret) as mock_method:
            unit = ProductRegistrationUnit(
                serialNumber="FEVM04TM23000333", contractNumber="2863TP100247", description="", isGovernment=False
            )
            self.forticare.register_product([unit], [])

        mock_method.assert_called_once_with(
            "/products/register",
            {
                "registrationUnits": [
                    {
                        "serialNumber": "FEVM04TM23000333",
                        "contractNumber": "2863TP100247",
                        "description": "",
                        "isGovernment": False,
                    }
                ],
                "locations": [],
            },
        )

    def test_register_service(self):
        _ret = {
            "token": "JnMYRfKrLVStMHFxrf5fqtPPQpMbWN",
            "version": "3.0",
            "status": 200,
            "message": "Success",
            "build": "1.0.0",
            "error": None,
            "assetDetails": {
                "serialNumber": "FEVM04TM23000333",
                "registrationDate": dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                "description": "",
                "isDecommissioned": False,
                "productModel": "<string>",
                "productModelEoR": "<string>",
                "productModelEoS": "<string>",
                "entitlements": [
                    {
                        "level": 2,
                        "levelDesc": "Web/Online",
                        "type": 2,
                        "typeDesc": "",
                        "startDate": dt.datetime.today().strftime("%Y-%m-%dT%H:%M:%S"),
                        "endDate": (dt.datetime.today() + dt.timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%S"),
                    },
                    {
                        "level": 1,
                        "levelDesc": "",
                        "type": 1,
                        "typeDesc": "<string>",
                        "startDate": dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                        "endDate": (dt.datetime.today() + dt.timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%S"),
                    },
                ],
                "partner": "",
                "licenses": [
                    {
                        "licenseNumber": "FSMAI4714475459",
                        "licenseSKU": "FSM-VM-INTERNAL",
                        "licenseType": "Eval",
                        "experiationDate": (dt.datetime.today() + dt.timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%S"),
                    }
                ],
                "location": {},
            },
        }
        with patch.object(FortiCare, "_post", return_value=_ret) as mock_method:
            service = ServiceRegistrationUnit(contractNumber="2863TP100247", description="", isGovernment=False)
            self.forticare.register_services(service)

        mock_method.assert_called_once_with(
            "/services/register",
            {
                "contractNumber": "2863TP100247",
                "description": "",
                "isGovernment": False,
            },
        )

    def test_register_license(self):
        _ret = {
            "token": "JnMYRfKrLVStMHFxrf5fqtPPQpMbWN",
            "version": "3.0",
            "status": 200,
            "message": "Success",
            "build": "1.0.0",
            "error": None,
            "assetDetails": {
                "serialNumber": "FEVM04TM23000333",
                "registrationDate": dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                "description": "",
                "isDecommissioned": False,
                "productModel": "<string>",
                "productModelEoR": "<string>",
                "productModelEoS": "<string>",
                "entitlements": [
                    {
                        "level": 2,
                        "levelDesc": "Web/Online",
                        "type": 2,
                        "typeDesc": "",
                        "startDate": dt.datetime.today().strftime("%Y-%m-%dT%H:%M:%S"),
                        "endDate": (dt.datetime.today() + dt.timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%S"),
                    }
                ],
                "partner": "",
                "licenses": [
                    {
                        "licenseNumber": "FSMAI4714475459",
                        "licenseSKU": "FSM-VM-INTERNAL",
                        "licenseType": "Eval",
                        "experiationDate": (dt.datetime.today() + dt.timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%S"),
                    }
                ],
                "location": {},
            },
        }
        with patch.object(FortiCare, "_post", return_value=_ret) as mock_method:
            license = LicenseRegistrationUnit(
                licenseRegistrationCode="2863TP100247",
                serialNumber="FSMAI4714475459",
                description="",
                isGovernment=False,
            )
            self.forticare.register_licenses(license)

        mock_method.assert_called_once_with(
            "/licenses/register",
            {
                "description": "",
                "isGovernment": False,
                "licenseRegistrationCode": "2863TP100247",
                "serialNumber": "FSMAI4714475459",
            },
        )


if __name__ == "__main__":
    unittest.main()
