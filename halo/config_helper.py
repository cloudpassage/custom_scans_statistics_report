import os
from halo.utility import Utility


class ConfigHelper(object):
    """
    This class contains all application configuration variables.

    Attributes:
        halo_api_key_id (str): Halo API key ID, sometimes referred to as 'key id'
        halo_api_key_secret (str): Halo API Key Secret associated with halo_api_key_id
        halo_api_hostname (str): Hostname for Halo API
        halo_api_port (str): Halo API port
        halo_api_version (str): Halo API version
        halo_api_auth_url (str): Halo API authentication URL
        halo_api_auth_args (str): Halo API authentication arguments (grant_type)
        halo_api_auth_token (str): Halo API authentication token
        output_directory (str): directory for generated output files.
        halo_group_id (str): Halo Group ID.
        module_name (str): HALO Scan Module Name (CSM, SVM, FIM, or SAM)
    """

    def __init__(self):
        self.halo_api_key_id = os.getenv("HALO_API_KEY", "HARDSTOP")
        self.halo_api_key_secret = os.getenv("HALO_API_SECRET_KEY", "HARDSTOP")
        self.halo_api_hostname = os.getenv(
            "HALO_API_HOSTNAME", "https://api.cloudpassage.com")
        self.halo_api_port = os.getenv("HALO_API_PORT", "443")
        self.halo_api_version = os.getenv("HALO_API_VERSION", "v1")
        self.halo_api_auth_url = "oauth/access_token"
        self.halo_api_auth_args = {'grant_type': 'client_credentials'}
        self.halo_api_auth_token = None
        self.output_directory = os.getenv("OUTPUT_DIRECTORY", "/tmp")
        self.halo_group_id = os.getenv("HALO_GROUP_ID", "HARDSTOP")
        self.module_name = os.getenv("MODULE_NAME", "svm")

    def sane(self):
        """
        Test to make sure that config items for Halo are set.
        Returns:
            True if everything is OK, False if otherwise
        """

        sanity = True
        template = "Required configuration variable {0} is not set!"
        critical_vars = {"HALO_API_KEY_ID": self.halo_api_key_id,
                         "HALO_API_KEY_SECRET": self.halo_api_key_secret,
                         "HALO_GROUP_ID": self.halo_group_id}
        for name, varval in critical_vars.items():
            if varval == "HARDSTOP":
                sanity = False
                Utility.log_stdout(template.format(name))
        return sanity
