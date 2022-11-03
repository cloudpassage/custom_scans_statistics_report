import sys
import os
from ensurepip import version
from halo import config_helper
from halo import halo_api_caller
from halo import utility

SCRIPT_DIR = os.path.abspath(__file__)
sys.path.append(os.path.dirname(SCRIPT_DIR))

__author__ = "Thomas.Miller@fidelissecurity.com"