from halo import halo_api_caller
from halo import config_helper
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


def test_get_group_servers(group_id):
    config = config_helper.ConfigHelper()
    halo_api_caller_obj = halo_api_caller.HaloAPICaller(config)
    halo_api_caller_obj.authenticate_client()
    group_servers_list = halo_api_caller_obj.get_group_servers(group_id)
    print(group_servers_list[0])


if __name__ == "__main__":
    test_get_group_servers("GROUP_ID")
