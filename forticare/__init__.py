# -*- coding: utf-8 -*-
"""
FortiCare API wrapper for Python
"""

from .asset import Asset, Service, License
from .location import Location
from .registration_unit import LicenseRegistrationUnit, ProductRegistrationUnit, ServiceRegistrationUnit


class FortiCare(object):
    """
    FortiCare API wrapper
    """

    def __init__(self, api_user=None, api_key=None, auto_login=False, timeout=20, debug=False):
        self._api_user = api_user
        self._api_key = api_key
        self._token = None
        self._auto_login = auto_login
        self._timeout = timeout
        self._debug = debug

    from ._helpers import _post
    from ._core import login
    from ._license import get_licenses, register_licenses, download_licenses
    from ._product import get_products, get_product_details, register_product
    from ._service import register_services

    @property
    def token(self):
        """Get API token"""
        return self._token

    @token.setter
    def token(self, token):
        """Set API token"""
        self._token = token

    @property
    def api_user(self):
        """Get API User"""
        return self._api_user

    @api_user.setter
    def api_user(self, api_user):
        """Set API User"""
        self._api_user = api_user

    @property
    def api_key(self):
        """Get API Key"""
        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        """Set API Key"""
        self._api_key = api_key

    @property
    def auto_login(self):
        """Get auto login"""
        return self._auto_login

    @auto_login.setter
    def auto_login(self, auto_login):
        """Set auto login"""
        self._auto_login = auto_login

    @property
    def timeout(self):
        """Get timeout"""
        return self._timeout

    @timeout.setter
    def timeout(self, timeout):
        """Set timeout"""
        self._timeout = timeout

    @property
    def debug(self):
        """Get debug"""
        return self._debug

    @debug.setter
    def debug(self, debug):
        """Set debug"""
        self._debug = debug

    def __str__(self):
        return f"FortiCare: logged with {self.api_user}"
