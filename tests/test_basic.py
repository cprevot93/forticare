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
import json
import requests
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
        data = {"error": "invalid_grant", "error_description": "Invalid credentials given."}
        ret = requests.Response()
        ret.status_code = 400
        ret._content = bytes(json.dumps(data), "utf-8")
        ret.headers = {"Content-Type": "application/json"}

        with patch.object(requests, "post", return_value=ret) as mock_method:
            res = self.forticare.login("toto", "toto")

        mock_method.assert_called_once_with(
            "https://customerapiauth.fortinet.com/api/v1/oauth/token/",
            json={
                "username": "toto",
                "password": "toto",
                "client_id": "assetmanagement",
                "grant_type": "password",
            },
        )

        assert res is False

    def test_invalid_pwd(self):
        data = {"error": "Unexpected error has happened", "status": "failure"}
        ret = requests.Response()
        ret.status_code = 401
        ret._content = bytes(json.dumps(data), "utf-8")

        with patch.object(requests, "post", return_value=ret) as mock_method:
            res = self.forticare.login(API_USERNAME, "toto")

        mock_method.assert_called_once_with(
            "https://customerapiauth.fortinet.com/api/v1/oauth/token/",
            json={
                "username": API_USERNAME,
                "password": "toto",
                "client_id": "assetmanagement",
                "grant_type": "password",
            },
        )

        assert res is False

    def test_auto_login_true(self):
        self.forticare._auto_login = True
        self.forticare.token = None
        res = self.forticare.get_products(dt.datetime(2023, 1, 1))
        print(res)
        self.assertTrue(res)
        self.assertTrue(isinstance(res, list))

    def test_auto_login_false(self):
        self.forticare._auto_login = False
        self.forticare.token = None

        with self.assertRaises(ValueError):
            res = self.forticare.get_products(dt.datetime(2023, 1, 1))
            print(res)

    def test_auto_login_true_invalid_token(self):
        data = {
            "build": "1.0.0",
            "error": {
                "errorCode": 202,
                "message": "Access denied. No permission to access the requested action or resource.",
            },
            "message": "Invalid incoming request.",
            "status": -1,
            "token": "fg7UDR6xzE9MAgw0MMcggk6WTgZVKr",
            "version": "3.0",
            "assets": None,
        }
        ret = requests.Response()
        ret.status_code = 400
        ret._content = bytes(json.dumps(data), "utf-8")

        data = {
            "access_token": "Qd8vpxWGfQkMv7XzX75vGjgMZ6Wsc3",
            "expires_in": 3600,
            "token_type": "Bearer",
            "scope": "read write",
            "refresh_token": "bUgkJ74cXH2tyD4Ps4pAGDnxnuqcbA",
            "message": "successfully authenticated",
            "status": "success",
        }
        ret2 = requests.Response()
        ret2.status_code = 200
        ret2._content = bytes(json.dumps(data), "utf-8")

        data = {
            "build": "1.0.0",
            "error": None,
            "message": "Request processed successfully",
            "status": 0,
            "token": "gI2aj6bEl5pVzi1FQCRUG0OzFc0kra",
            "version": "3.0",
            "assets": [
                {
                    "description": "Automatically registered by Synapflo",
                    "entitlements": [
                        {
                            "endDate": "2027-01-17T00:00:00",
                            "level": 6,
                            "levelDesc": "Web/Online",
                            "startDate": "2024-01-18T00:00:00",
                            "type": 2,
                            "typeDesc": "Firmware & General Updates",
                        },
                        {
                            "endDate": "2027-01-17T00:00:00",
                            "level": 20,
                            "levelDesc": "Premium",
                            "startDate": "2024-01-18T00:00:00",
                            "type": 11,
                            "typeDesc": "Enhanced Support",
                        },
                        {
                            "endDate": "2027-01-17T00:00:00",
                            "level": 20,
                            "levelDesc": "Premium",
                            "startDate": "2024-01-18T00:00:00",
                            "type": 12,
                            "typeDesc": "Telephone Support",
                        },
                        {
                            "endDate": "2027-01-17T00:00:00",
                            "level": 6,
                            "levelDesc": "Web/Online",
                            "startDate": "2024-01-18T00:00:00",
                            "type": 21,
                            "typeDesc": "Advanced Malware Protection",
                        },
                        {
                            "endDate": "2027-01-17T00:00:00",
                            "level": 6,
                            "levelDesc": "Web/Online",
                            "startDate": "2024-01-18T00:00:00",
                            "type": 28,
                            "typeDesc": "FortiWeb Security Service",
                        },
                        {
                            "endDate": "2027-01-17T00:00:00",
                            "level": 6,
                            "levelDesc": "Web/Online",
                            "startDate": "2024-01-18T00:00:00",
                            "type": 43,
                            "typeDesc": "IP Reputation",
                        },
                    ],
                    "isDecommissioned": False,
                    "productModel": "FortiWeb VM 2 CPU",
                    "registrationDate": "2024-01-18T00:13:44",
                    "serialNumber": "FVVM02TM24000714",
                    "warrantySupports": None,
                    "assetGroups": [],
                    "contracts": [
                        {
                            "contractNumber": "4927CQ108750",
                            "sku": "FC-10-VVM02-936-02-36",
                            "terms": [
                                {
                                    "endDate": "2027-01-17T03:06:54",
                                    "startDate": "2024-01-18T03:06:54",
                                    "supportType": "Firmware & General Updates",
                                },
                                {
                                    "endDate": "2027-01-17T03:06:54",
                                    "startDate": "2024-01-18T03:06:54",
                                    "supportType": "IP Reputation",
                                },
                                {
                                    "endDate": "2027-01-17T03:06:54",
                                    "startDate": "2024-01-18T03:06:54",
                                    "supportType": "Telephone Support",
                                },
                                {
                                    "endDate": "2027-01-17T03:06:54",
                                    "startDate": "2024-01-18T03:06:54",
                                    "supportType": "FortiWeb Security Service",
                                },
                                {
                                    "endDate": "2027-01-17T03:06:54",
                                    "startDate": "2024-01-18T03:06:54",
                                    "supportType": "Enhanced Support",
                                },
                                {
                                    "endDate": "2027-01-17T03:06:54",
                                    "startDate": "2024-01-18T03:06:54",
                                    "supportType": "Advanced Malware Protection",
                                },
                            ],
                        }
                    ],
                    "productModelEoR": None,
                    "productModelEoS": None,
                    "folderId": 0,
                    "folderPath": "/My Assets",
                    "status": "Registered",
                }
            ],
            "pageNumber": 1,
            "totalPages": 1,
        }
        ret3 = requests.Response()
        ret3.status_code = 200
        ret3._content = bytes(json.dumps(data), "utf-8")

        self.forticare._auto_login = True
        self.forticare.token = "toto"

        with patch.object(
            requests,
            "post",
            side_effect=[ret, ret2, ret3],
        ) as mock_method:
            res = self.forticare.get_products(dt.datetime(2028, 1, 1))
            print(res)
            self.assertTrue(res)

        mock_method.call_count == 3

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
        # self.assertTrue(isinstance(asset.contracts[0], dict))
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
        location = Location(**data)
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
        sn = "FEVM04TM23XXXXXX"
        res = self.forticare.download_licenses(sn)
        print(res)
        self.assertTrue(res)
        self.assertTrue(isinstance(res, str))
        self.assertTrue(res.startswith("-----BEGIN FE VM LICENSE-----\n"))

        _ret = {
            "token": "JnMYRfKrLVStMHFxrf5fqtPPQpMbWN",
            "version": "3.0",
            "status": 200,
            "message": "Success",
            "build": "1.0.0",
            "error": None,
            "assets": [
                {
                    "serialNumber": "FEVM04TM23XXXXXX",
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
                serialNumber="FEVM04TM23XXXXXX", contractNumber="2863TP100247", description="", isGovernment=False
            )
            self.forticare.register_product([unit], [])

        mock_method.assert_called_once_with(
            "/products/register",
            {
                "registrationUnits": [
                    {
                        "contractNumber": "2863TP100247",
                        "description": "",
                        "isGovernment": False,
                        "serialNumber": "FEVM04TM23XXXXXX",
                    }
                ]
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
                "serialNumber": "FEVM04TM23XXXXXX",
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

    def test_register_service_bad_value_return(self):
        """
        API returns None (inexpected).
        """
        with patch.object(FortiCare, "_post", return_value=None) as mock_method:
            service = ServiceRegistrationUnit(contractNumber="2863TP100247", description="", isGovernment=False)
            with self.assertRaises(Exception):
                self.forticare.register_services(service)

        mock_method.assert_called_once_with(
            "/services/register",
            {
                "contractNumber": "2863TP100247",
                "description": "",
                "isGovernment": False,
            },
        )

    def test_register_service_bad_value_return_2(self):
        """
        API returns None (inexpected).
        """
        with patch.object(FortiCare, "_post", return_value={}) as mock_method:
            service = ServiceRegistrationUnit(contractNumber="2863TP100247", description="", isGovernment=False)
            with self.assertRaises(Exception):
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
                "serialNumber": "FEVM04TM23XXXXXX",
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

    def test_register_product_missing_forticloud_key(self):
        # TODO: implement test
        _ret = {
            "build": "1.0.0",
            "error": {"errorCode": 301, "message": "Failed"},
            "message": "Failed",
            "status": 2,
            "token": "t9IIeGdc5YEXJkfbnAlDYoIJSLE15q",
            "version": "3.0",
            "assets": [
                {
                    "description": None,
                    "entitlements": None,
                    "isDecommissioned": False,
                    "productModel": None,
                    "registrationDate": None,
                    "serialNumber": "FGT91GTK23001XXX",
                    "warrantySupports": None,
                    "assetGroups": None,
                    "contracts": None,
                    "productModelEoR": None,
                    "productModelEoS": None,
                    "additionalInfo": None,
                    "contractNumber": None,
                    "contractTerms": None,
                    "location": None,
                    "message": "Product-> FortiCloud Key is Required.",
                    "sku": None,
                    "status": 2,
                    "folderId": 0,
                    "folderPath": None,
                }
            ],
        }

    def test_register_product_bad_forticloud_key(self):
        # TODO: implement test and exception
        data = {
            "registrationUnits": [
                {"cloudKey": "ABC", "description": "", "isGovernment": false, "serialNumber": "FG40FTK190001XXX"}
            ]
        }
        _ret = {
            "build": "1.0.0",
            "error": {"errorCode": 102, "message": "Invalid cloud key provided for registration units[0]. "},
            "message": "Invalid incoming request.",
            "status": -1,
            "token": "XQ4qlcU8MGVpjuZKJYGSk4RXQFFrFf",
            "version": "3.0",
            "assets": None,
        }


if __name__ == "__main__":
    unittest.main()
