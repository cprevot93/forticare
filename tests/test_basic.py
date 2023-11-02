# -*- coding: utf-8 -*-

from tests.context import FortiFlex, API_USERNAME, API_PASSWORD, PROGRAM_SN

import requests
import unittest


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def __init__(self, *args, **kwargs):
        self.flex = FortiFlex(API_USERNAME, API_PASSWORD)
        self.flex.login()
        super(BasicTestSuite, self).__init__(*args, **kwargs)

    def setUp(self) -> None:
        return super().setUp()

    def test_login_token(self):
        token = ""
        try:
            token = self.flex.token
        except Exception as exp:
            print(str(exp.args))
        assert token  # <> None

    def test_invalid_cred(self):
        res = self.flex.login(API_USERNAME, "toto")
        assert res == False

    def test_get_config(self):
        res = self.flex.get_configs(PROGRAM_SN)
        print(res)
        self.assertTrue(res)
        self.assertTrue(isinstance(res, list))

    def test_auto_login(self):
        with self.subTest("Test auto login True"):
            self.flex._auto_login = True
            self.flex.token = None
            res = self.flex.get_configs(PROGRAM_SN)
            print(res)
            self.assertTrue(res)
            self.assertTrue(isinstance(res, list))

        with self.subTest("Test auto login False"):
            self.flex._auto_login = False
            self.flex.token = None
            with self.assertRaises(ValueError):
                res = self.flex.get_configs(PROGRAM_SN)
                print(res)

        with self.subTest("Test auto login True and change token to an invalid one"):
            self.flex._auto_login = True
            self.flex.token = "toto"
            res = self.flex.get_configs(PROGRAM_SN)
            print(res)
            self.assertTrue(res)
            self.assertTrue(isinstance(res, list))


if __name__ == "__main__":
    unittest.main()
