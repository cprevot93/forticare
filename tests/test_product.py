# -*- coding: utf-8 -*-
from unittest.mock import patch

from tests.context import (
    API_USERNAME,
    API_PASSWORD,
    Asset,
    FortiCare,
    Location,
    ProductRegistrationUnit,
)
import os
import json
import unittest
import requests
import datetime as dt


class RegisterProductUnitTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        self.forticare = FortiCare(API_USERNAME, API_PASSWORD, True)
        self.forticare.login()
        super(RegisterProductUnitTest, self).__init__(*args, **kwargs)

    def setUp(self) -> None:
        return super().setUp()


class RegisterProductE2ETestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        self.forticare = FortiCare(API_USERNAME, API_PASSWORD, True)
        self.forticare.login()
        super(RegisterProductE2ETestCase, self).__init__(*args, **kwargs)

    def setUp(self) -> None:
        return super().setUp()

    def test_get_products(self):
        _ret = {
            "build": "1.0.0",
            "error": None,
            "message": "Request processed successfully",
            "status": 0,
            "token": "S4vAmY3nrlYPUaa6VK8KNR206skfBR",
            "version": "3.0",
            "assets": [
                {
                    "description": "Internal test 6.0",
                    "entitlements": [
                        {
                            "endDate": "2020-01-21T00:00:00",
                            "level": 20,
                            "levelDesc": "Premium",
                            "startDate": "2019-11-22T00:00:00",
                            "type": 11,
                            "typeDesc": "Enhanced Support",
                        },
                        {
                            "endDate": "2020-01-21T00:00:00",
                            "level": 20,
                            "levelDesc": "Premium",
                            "startDate": "2019-11-22T00:00:00",
                            "type": 12,
                            "typeDesc": "Telephone Support",
                        },
                        {
                            "endDate": "2020-01-21T00:00:00",
                            "level": 6,
                            "levelDesc": "Web/Online",
                            "startDate": "2019-11-22T00:00:00",
                            "type": 31,
                            "typeDesc": "FortiClient Endpoint Management",
                        },
                    ],
                    "isDecommissioned": True,
                    "productModel": "FortiClient EMS",
                    "registrationDate": "2019-11-22T01:30:49",
                    "serialNumber": "FCTEMS0000102441",
                    "warrantySupports": None,
                    "assetGroups": [],
                    "contracts": [
                        {
                            "contractNumber": "8490TR105214",
                            "sku": "FC1-15-EMS01-158-02-02",
                            "terms": [
                                {
                                    "endDate": "2020-01-21T01:30:49",
                                    "startDate": "2019-11-22T01:30:49",
                                    "supportType": "Telephone Support",
                                },
                                {
                                    "endDate": "2020-01-21T01:30:49",
                                    "startDate": "2019-11-22T01:30:49",
                                    "supportType": "Enhanced Support",
                                },
                                {
                                    "endDate": "2020-01-21T01:30:49",
                                    "startDate": "2019-11-22T01:30:49",
                                    "supportType": "FortiClient Endpoint Management",
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

        with patch.object(self.forticare, "_post", return_value=_ret):
            res = self.forticare.get_products(dt.datetime(2023, 1, 1))

        print(res)
        self.assertTrue(res)
        self.assertTrue(isinstance(res, list))

    def test_get_product_details(self):
        sn = "FCGSLB0000000205"
        _ret = {
            "build": "1.0.0",
            "error": None,
            "message": "Success",
            "status": 0,
            "token": "S4vAmY3nrlYPUaa6VK8KNR206skfBR",
            "version": "3.0",
            "assetDetails": {
                "description": None,
                "entitlements": [
                    {
                        "endDate": "2021-09-23T00:00:00",
                        "level": 20,
                        "levelDesc": "Premium                                 ",
                        "startDate": "2020-09-23T00:00:00",
                        "type": 11,
                        "typeDesc": "Enhanced Support       ",
                    },
                    {
                        "endDate": "2021-09-23T00:00:00",
                        "level": 20,
                        "levelDesc": "Premium                                 ",
                        "startDate": "2020-09-23T00:00:00",
                        "type": 12,
                        "typeDesc": "Telephone Support                                                                                                                                                                                                                                              ",
                    },
                    {
                        "endDate": "2021-09-23T00:00:00",
                        "level": 6,
                        "levelDesc": "Web/Online                              ",
                        "startDate": "2020-09-23T00:00:00",
                        "type": 118,
                        "typeDesc": "FortiADC GSLB Cloud Service QPS",
                    },
                    {
                        "endDate": "2021-09-23T00:00:00",
                        "level": 6,
                        "levelDesc": "Web/Online                              ",
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
                "assetGroups": None,
                "contracts": [
                    {
                        "contractNumber": "1162XX438908",
                        "sku": "FC2-10-CGSLB-332-02-12",
                        "terms": [
                            {
                                "endDate": "2021-09-23T00:00:00",
                                "startDate": "2020-09-23T00:00:00",
                                "supportType": "Enhanced Support",
                            },
                            {
                                "endDate": "2021-09-23T00:00:00",
                                "startDate": "2020-09-23T00:00:00",
                                "supportType": "Telephone Support",
                            },
                            {
                                "endDate": "2021-09-23T00:00:00",
                                "startDate": "2020-09-23T00:00:00",
                                "supportType": "FortiADC GSLB Cloud Service checks",
                            },
                        ],
                    },
                    {
                        "contractNumber": "5762CL381100",
                        "sku": "FC2-10-CGSLB-330-02-12",
                        "terms": [
                            {
                                "endDate": "2021-09-23T00:00:00",
                                "startDate": "2020-09-23T00:00:00",
                                "supportType": "Enhanced Support",
                            },
                            {
                                "endDate": "2021-09-23T00:00:00",
                                "startDate": "2020-09-23T00:00:00",
                                "supportType": "Telephone Support",
                            },
                            {
                                "endDate": "2021-09-23T00:00:00",
                                "startDate": "2020-09-23T00:00:00",
                                "supportType": "FortiADC GSLB Cloud Service QPS",
                            },
                        ],
                    },
                ],
                "productModelEoR": None,
                "productModelEoS": None,
                "license": None,
                "location": None,
                "partner": "FORTITEST",
                "folderId": 0,
                "folderPath": "/My Assets",
            },
        }

        with patch.object(self.forticare, "_post", return_value=_ret):
            res = self.forticare.get_product_details(sn)
        print(res)
        self.assertTrue(res)
        self.assertTrue(isinstance(res, Asset))
        self.assertTrue(res.serialNumber == sn)
        self.assertTrue(res.productModel == "FortiGSLB Cloud")

    def test_register_product(self):
        units = [
            ProductRegistrationUnit(cloudKey="ABC", description="", isGovernment=False, serialNumber="FG40FTK190001XXX")
        ]
        _ret = {}  # TODO
        with patch.object(self.forticare, "_post", return_value=_ret):
            with self.assertRaises(Exception):
                res = self.forticare.register_product(units)

    def test_register_product_with_location(self):
        serial = "FG40FTK190001XXX"
        units = [ProductRegistrationUnit(cloudKey="ABC", description="", isGovernment=False, serialNumber=serial)]
        locations = [(serial, Location("Test", "Test", "Test", "Test", "Test", "Test", "Test", "Test"))]
        _ret = json.load(
            open(os.path.join(os.path.dirname(__file__), "data", "product_already_registered.json"), encoding="utf-8")
        )  # TODO: get a sample response
        with patch.object(self.forticare, "_post", return_value=_ret):
            res = self.forticare.register_product(units, locations)

    def test_register_product_already_registered(self):
        units = [
            ProductRegistrationUnit(cloudKey="ABC", description="", isGovernment=False, serialNumber="FG40FTK190001XXX")
        ]
        data = json.load(
            open(os.path.join(os.path.dirname(__file__), "data", "product_already_registered.json"), encoding="utf-8")
        )
        response = requests.Response()
        response.request = requests.Request()
        response.status_code = 400
        response._content = bytes(json.dumps(data), "utf-8")
        response.headers = {"Content-Type": "application/json"}

        with patch.object(requests, "post", return_value=response):
            with self.assertRaises(requests.exceptions.HTTPError) as e:
                res = self.forticare.register_product(units)
            self.assertEqual(
                e.exception.args[1],
                "POST /products/register FG40FTK190001XXX | Product-> Product already registered, but no contract associated with request. Please check again.",
            )

    def test_register_product_missing_forticloud_key(self):
        units = [ProductRegistrationUnit(description="", isGovernment=False, serialNumber="FG40FTK190001XXX")]
        data = json.load(
            open(
                os.path.join(os.path.dirname(__file__), "data", "product_missing_forticloud_key.json"), encoding="utf-8"
            )
        )
        response = requests.Response()
        response.request = requests.Request()
        response.status_code = 400
        response._content = bytes(json.dumps(data), "utf-8")
        response.headers = {"Content-Type": "application/json"}

        with patch.object(requests, "post", return_value=response):
            with self.assertRaises(requests.exceptions.HTTPError) as e:
                res = self.forticare.register_product(units)
            self.assertEqual(
                e.exception.args[1], "POST /products/register FG40FTK190001XXX | Product-> FortiCloud Key is Required."
            )

    def test_register_product_bad_forticloud_key(self):
        units = [
            ProductRegistrationUnit(cloudKey="ABC", description="", isGovernment=False, serialNumber="FG40FTK190001XXX")
        ]
        data = json.load(
            open(os.path.join(os.path.dirname(__file__), "data", "product_invalid_cloud_key.json"), encoding="utf-8")
        )
        response = requests.Response()
        response.request = requests.Request()
        response.status_code = 400
        response._content = bytes(json.dumps(data), "utf-8")
        response.headers = {"Content-Type": "application/json"}

        with patch.object(requests, "post", return_value=response):
            with self.assertRaises(requests.exceptions.HTTPError) as e:
                res = self.forticare.register_product(units)
            self.assertEqual(
                e.exception.args[1], "POST /products/register Invalid cloud key provided for registration units[0]. "
            )
