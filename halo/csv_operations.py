from datetime import datetime
from halo.utility import Utility


class CSVOperations(object):

    def prepare_csv_file(self, output_directory):
        current_time = Utility.date_to_iso8601(datetime.now())
        file_name = 'custom_scans_statistics_report_' + current_time + '.csv'
        file_name = file_name.replace(':', '-')
        if output_directory == "":
            absolute_path = file_name
        else:
            absolute_path = output_directory + "/" + file_name
        return absolute_path, file_name, current_time
