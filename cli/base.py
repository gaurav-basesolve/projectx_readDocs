import os
import json
import botocore
from urllib.parse import urlparse


def aws_cp(projectx_service, folder, link, patient_name, flowcell_id, sample_id, workflow_name):
    """Copy file from AWS s3 using projectX service and store them specifed location.

    :param projectx_service: ProejctX session object
    :type projectx_service: projectx_service
    :param folder: download folder location
    :type folder: path
    :param link: s3 uri
    :type link: str
    :param patient_name: name of the patient
    :type patient_name: str
    :param flowcell_id: flowcell id
    :type flowcell_id: str
    :param sample_id: sample id
    :type sample_id: str
    :param workflow_name: workflow name
    :type workflow_name: str
    :return: None
    :rtype: NoneType
    """
    s3_client = projectx_service.get_s3_client()

    bucket_name = urlparse(link).netloc.replace(".s3.amazonaws.com", "")
    url_path = urlparse(link).path
    filename = os.path.basename(url_path)
    try:
        os.makedirs(f"{folder}/projectx-download/", exist_ok=True)
        os.makedirs(
            f"{folder}/projectx-download/{patient_name}_{flowcell_id}_{sample_id}_{workflow_name}",
            exist_ok=True,
        )
        try:
            s3_client.Bucket(bucket_name).download_file(
                url_path[1:],
                f"{folder}/projectx-download/{patient_name}_{flowcell_id}_{sample_id}_{workflow_name}/{filename}",
            )
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                print("The object does not exist.")
            else:
                raise
            quit("Exiting...")

    except FileNotFoundError:
        print(f"[Error] No such file or directory: {folder}")
        quit("Exiting...")
    except NotADirectoryError:
        print(f"[Error] Not a directory: {folder}")
        quit("Exiting...")


def save_access(deployment_name, key):
    """Save user provided configuration information

    :param deployment_name: Name of the deployment
    :type deployment_name: str
    :param key: API key
    :type key: str
    :return: None
    :rtype: NoneType
    """
    full_path = os.path.expanduser("~/.projectx/credentials.json")
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    access_details = {"deployment-name": deployment_name, "access-key": key}
    with open(full_path, "w") as f:
        json.dump(access_details, f)
    print("[INFO]: projectx configured")


def check_access():
    """Check if credentials exists.

    :return: Pre-configured Deployment name and api-key
    :rtype: tuple
    """
    full_path = os.path.expanduser("~/.projectx/credentials.json")
    try:
        with open(full_path, "r") as f:
            conf = json.load(f)

        print(conf)
        return conf["deployment-name"], conf["access-key"]
    except FileNotFoundError:
        exit("[INFO] No access-key found. Please configure projectx-cli first")
