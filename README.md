# custom_scans_statistics_report

## Goal:
Custom scans statistics report script shows statistics about scans' status (i.e., ```completed_clean```, ```completed_with_errors```, ```failed```, ```pending```, ```queued```, and ```running```) on different scan types (```csm```, ```fim```, ```svm```, and ```sam```) for all servers that belong to specific HALO group. the script exports report results into external CSV file.

## Requirements:
- CloudPassage Halo API key (with Auditor privileges).
- Python 3.6 or later including packages specified in "requirements.txt".

## Installation:
```
   git clone https://github.com/cloudpassage/custom_scans_statistics_report
   cd custom_scans_statistics_report
   pip install -r requirements.txt
```

## Configuration:
| Variable | Description | Default Value |
| -------- | ----- | ----- |
| HALO_API_KEY | ID of HALO API Key | ef\*\*ds\*\*fa |
| HALO_API_SECRET_KEY | Secret of HALO API Key | fgfg\*\*\*\*\*heyw\*\*\*\*ter352\*\*\* |
| HALO_API_HOSTNAME | Halo API Host Name | https://api.cloudpassage.com |
| HALO_API_PORT | Halo API Port Number | 443 |
| HALO_API_VERSION | HALO EndPoint Version | v1 |
| OUTPUT_DIRECTORY | Location for generated CSV file | /tmp |
| HALO_GROUP_ID | Halo Group ID | 0962\*\*\*\*013\*\*\*ec22\*\*\* |
| MODULE_NAME | HALO Scan Module Name (csm, svm, fim, or sam) | svm |

## How the scripts works:
- Checking and validation of the provided configuration parameters and fails in case of missing any required parameter.
- Use HALO API key id/secret to generate access token to be used to access protected HALO API resources.
- Retrieving the list of servers that belongs the provided HALO group ID.
- For every server retrieved from the previous call, the script retrieves details of all the historical scans related to this server and filter these scans based on the provided module name (csm, fim, svm, and sam).
- Formating and exporting all retreived Report data of into CSV file format and save it in the provided output directory.

## How to run the script (stand-alone):
To run the script follow the below steps.

1.  Navigate to the script root directory that contains the python module named "app.py", and run it as described below;

```
    cd custom_scans_statistics_report
    python app.py
```

## How to run the tool (containerized):

- Clone the script repository:
```
   git clone https://github.com/cloudpassage/custom_scans_statistics_report
```

- Build the docker image:
```
   cd custom_scans_statistics_report
   docker build -t custom_scans_statistics_report .
```

- Run the docker container:
```
    docker run -it \
    -e HALO_API_KEY=$HALO_API_KEY \
    -e HALO_API_SECRET_KEY=$HALO_API_SECRET_KEY \
    -e HALO_GROUP_ID=$HALO_GROUP_ID \
    -e MODULE_NAME=$MODULE_NAME \
    -v $OUTPUT_DIRECTORY:/tmp \
    custom_scans_statistics_report
```