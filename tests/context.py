# -*- coding: utf-8 -*-
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from forticare import FortiFlex
from tests.env import API_USERNAME, API_PASSWORD, PROGRAM_SN
