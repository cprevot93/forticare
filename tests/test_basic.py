# -*- coding: utf-8 -*-

from tests.context import FortiCare, API_USERNAME, API_PASSWORD

import unittest
import datetime as dt
from forticare import Asset


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

    def test_get_products(self):
        res = self.forticare.get_products(dt.datetime(2023, 1, 1))
        print(res)
        self.assertTrue(res)
        self.assertTrue(isinstance(res, list))

    def test_get_register_product(self):
        # TODO: mockup requests to test this method
        pass

    def test_get_product_details(self):
        sn = "FCGSLB0000000205"
        res = self.forticare.get_product_details(sn)
        print(res)
        self.assertTrue(res)
        self.assertTrue(isinstance(res, Asset))
        self.assertTrue(res.serial_number == sn)
        self.assertTrue(res.product_model == "FortiGSLB Cloud")


if __name__ == "__main__":
    unittest.main()
