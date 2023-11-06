# -*- coding: utf-8 -*-
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from forticare import (
    Asset,
    Service,
    FortiCare,
    Location,
    License,
    LicenseRegistrationUnit,
    ProductRegistrationUnit,
    ServiceRegistrationUnit,
)
from tests.env import API_USERNAME, API_PASSWORD
