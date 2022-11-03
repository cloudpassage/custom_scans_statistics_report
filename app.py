import sys
import math
import time
import csv
from unicodedata import name
from halo import config_helper
from halo import halo_api_caller
from halo import utility
from halo import csv_operations


def main():

    util = utility.Utility()
    util.log_stdout("   Custom Scans Statistics Report Script")
    config = config_helper.ConfigHelper()
    json_to_csv_obj = csv_operations.CSVOperations()
    output_directory = config.output_directory
    halo_group_id = config.halo_group_id
    scan_module_name = config.module_name
    script_start_time = time.time()
    util.log_stdout("1- Creating HALO API CALLER Object.")
    halo_api_caller_obj = halo_api_caller.HaloAPICaller(config)

    """
    First we make sure that all configs are sound...
    """
    util.log_stdout(
        "2- Checking the provided configuration parameters")
    check_configs(config, halo_api_caller_obj, util)

    """
    Retrieving Total Number of Servers that belongs to the provided Group
    """
    util.log_stdout(
        "3- Retrieving Total Number of Servers that belongs to Group ID: %s" % halo_group_id)
    group_servers_list = halo_api_caller_obj.get_group_servers(halo_group_id)
    group_servers_list_data = group_servers_list[0]
    try:
        total_number_of_servers = group_servers_list_data['count']
    except:
        total_number_of_servers = 0
    servers_pages = math.ceil(total_number_of_servers/100)

    """
    Preparing CSV File to store the report results into it
    """
    util.log_stdout(
        "4- Preparing CSV File (Name and Location) to store the report results into it")
    absolute_path, file_name, current_time = json_to_csv_obj.prepare_csv_file(
        output_directory)

    table_header = ['OS Type', 'OS Version', 'Server Hostname', 'Reported FQDN', 'Completed Clean', 'Completed With Errors',
                    'Failed', 'Pending', 'Queued', 'Running']

    """
    Retrieving & Exporting Report Data into the CSV file
    """
    util.log_stdout(
        "5- Retrieving & Exporting Report Data into the CSV file")
    header_flag = True
    row_counter = 0
    all_scans_completed_clean = 0
    all_scans_completed_with_errors = 0
    all_scans_failed = 0
    all_scans_pending = 0
    all_scans_queued = 0
    all_scans_running = 0
    for page in range(servers_pages):
        current_page = page+1
        page_group_servers_list = halo_api_caller_obj.get_group_servers_per_page(
            halo_group_id, current_page)
        servers_list = page_group_servers_list[0]['servers']
        for server in servers_list:
            server_id = server['id']
            os_type = server['platform']
            os_version = server['os_version']
            server_hostname = server['hostname']
            reported_fqdn = server['reported_fqdn']

            server_scans_results = halo_api_caller_obj.get_server_scans(
                server_id, scan_module_name)
            server_scans_list_data = server_scans_results[0]
            try:
                total_number_of_server_scans = server_scans_list_data['count']
            except:
                total_number_of_server_scans = 0
            server_scans_pages = math.ceil(total_number_of_server_scans/100)

            server_scans_completed_clean = 0
            server_scans_completed_with_errors = 0
            server_scans_failed = 0
            server_scans_pending = 0
            server_scans_queued = 0
            server_scans_running = 0
            scan_number = 0
            for scans_page in range(server_scans_pages):
                current_server_scans_page = scans_page+1
                page_server_scans_list = halo_api_caller_obj.get_server_scans_per_page(
                    server_id, scan_module_name, current_server_scans_page)
                scans_list = page_server_scans_list[0]['scans']
                for scan in scans_list:
                    scan_number += 1
                    util.log_stdout("   Retrieving & Exporting Data of Scan # [%s / %s] into the CSV file" % (
                        scan_number, total_number_of_server_scans))
                    current_temp_time = time.time()
                    if((current_temp_time - script_start_time) > 840):
                        check_configs(config, halo_api_caller_obj, util)
                    scan_status = scan['status']
                    if scan_status == 'completed_clean':
                        server_scans_completed_clean += 1
                        all_scans_completed_clean += 1
                    elif scan_status == 'completed_with_errors':
                        server_scans_completed_with_errors += 1
                        all_scans_completed_with_errors += 1
                    elif scan_status == 'failed':
                        server_scans_failed += 1
                        all_scans_failed += 1
                    elif scan_status == 'pending':
                        server_scans_pending += 1
                        all_scans_pending += 1
                    elif scan_status == 'queued':
                        server_scans_queued += 1
                        all_scans_queued += 1
                    elif scan_status == 'running':
                        server_scans_running += 1
                        all_scans_running += 1
                    else:
                        continue

            table_row = [os_type, os_version, server_hostname, reported_fqdn, server_scans_completed_clean,
                         server_scans_completed_with_errors, server_scans_failed, server_scans_pending,
                         server_scans_queued, server_scans_running]

            with open(absolute_path, 'a', newline='') as f:
                writer = csv.writer(f)
                if header_flag == True:
                    writer.writerow(
                        ["# ------------------------------- #"])
                    writer.writerow(
                        ["# Report Name: %s" % (file_name)])
                    writer.writerow(
                        ["# Report Generated at: %s" % (current_time)])
                    writer.writerow(
                        ["# Servers Filters: Group ID: [%s],  Scan Type: [%s]" % (halo_group_id, scan_module_name)])
                    writer.writerow(
                        ["# ------------------------------- #"])
                    writer.writerow(table_header)
                    row_counter += 1
                    writer.writerow(table_row)
                    header_flag = False
                else:
                    row_counter += 1
                    writer.writerow(table_row)

    """
    Adding Overall Scans Statistics into the CSV file
    """
    util.log_stdout(
        "6- Adding Overall Scans Statistics into the CSV file")
    with open(absolute_path, 'r') as readFile:
        reader = csv.reader(readFile)
        lines = list(reader)
        lines.insert(4, ["# Total Number of Completed Clean Scans = %s" % (
            all_scans_completed_clean)])
        lines.insert(5, ["# Total Number of Completed With Errors Scans = %s" % (
            all_scans_completed_with_errors)])
        lines.insert(6, ["# Total Number of Failed Scans = %s" %
                     (all_scans_failed)])
        lines.insert(7, ["# Total Number of Pending Scans = %s" %
                     (all_scans_pending)])
        lines.insert(8, ["# Total Number of Queued Scans = %s" %
                     (all_scans_queued)])
        lines.insert(
            9, ["# Total Number of Running Scans = %s" % (all_scans_running)])
        lines.insert(10, ["# Total Number of Rows = %s" % (row_counter)])
    with open(absolute_path, 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)
    readFile.close()
    writeFile.close()

    """
    Operation Completed
    """
    util.log_stdout(
        "7- Operation Completed, Check Generated CSV File!")

    script_end_time = time.time()
    consumed_time = script_end_time - script_start_time
    optimized_consumed_time = round(consumed_time, 3)
    utility.Utility.log_stdout(
        "Total Time Consumed = [%s] seconds" % (optimized_consumed_time))


def check_configs(config, halo_api_caller, util):
    halo_api_caller_obj = halo_api_caller
    if halo_api_caller_obj.credentials_work() is False:
        util.log_stdout("Halo credentials are bad!  Exiting!")
        sys.exit(1)

    if config.sane() is False:
        util.log_stdout("Configuration is bad!  Exiting!")
        sys.exit(1)


if __name__ == "__main__":
    main()
