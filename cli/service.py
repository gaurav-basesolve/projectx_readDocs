import json
import requests
import boto3

PROJECTX_DOMAIN = "testengine.link"
PROJECTX_ENDPOINTS = {
    "NCGM-US": f"https://projectx.{PROJECTX_DOMAIN}",
    "DHM": f"https://dartmouht.{PROJECTX_DOMAIN}",
    "NCGM-IN": f"https://ncgm-in.{PROJECTX_DOMAIN}",
    "DEV": f"https://ui.{PROJECTX_DOMAIN}",
    "LOCAL": "http://localhost:6000",
}


class projectx_service:
    """ProjectX API service provider

    :return: projectx session object with configurations to call apis.
    :rtype: object[projectx_service]
    """

    __projectx_url = None
    __api_key = None
    __client_url_base = None
    __auth_header = None
    __access_key = None
    __secret_key = None

    def __init__(self, api_key, deployment_name):
        """Initialize the service with access related information obtained based on projectx url and user apikey

        :param projectx_url: http or https url of projectx webapp
        :type projectx_url: str
        :param api_key: User specific api key
        :type api_key: str
        """
        # TODO: Fetch projectx_url from global database.
        self.deployment_name = deployment_name
        self.__projectx_url = PROJECTX_ENDPOINTS[deployment_name]
        self.__api_key = api_key
        self.__client_url_base = f"{self.__projectx_url}/api/v1/client"
        verification_url = f"{self.__client_url_base}/verify-api-key"
        payload = json.dumps(
            {"apikey": self.__api_key, "deployment_name": self.deployment_name}
        )
        headers = {"Content-Type": "application/json"}
        validation_response = requests.post(
            url=verification_url, data=payload, headers=headers
        )
        validity_info = validation_response.json()
        self.apikey_is_valid = validity_info["verified"]
        access_token = validity_info["access_token"]
        self.__access_key = validity_info["aws"]["aws_access_key_id"]
        self.__secret_key = validity_info["aws"]["aws_secret_access_key"]
        self.__auth_header = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

    def get_analysis_samples(self, more):
        """Fetch all the analysis assigned to the user and thier metadata

        :param more: Fetch more meta data
        :type more: bool
        :return: List of analysis access to the user
        :rtype: list[dict]
        """
        analysis_url = f"{self.__client_url_base}/get-samples"
        payload = json.dumps({"apikey": self.__api_key, "more": more})
        analysis_response = requests.post(
            url=analysis_url, data=payload, headers=self.__auth_header
        )
        analysis_data = analysis_response.json()
        samples = analysis_data["sample_info"]

        return samples

    def get_downloadable_files_from_analysis(self, analysis, filenames=None):
        """Get downloadable files that belong to a specific sample that has been analysed via ProjectX.

        :param analysis: Analysis ID, [Sample-ID]
        :type analysis: str
        :param filenames: Comma seperated list fo file names, optionally required for downloading specific files only, defaults to None
        :type filenames: str, optional
        :return: Set of files available form the analysis
        :rtype: dict
        """
        analysis_files_url = f"{self.__client_url_base}/list-sample-files"
        payload = json.dumps(
            {"apikey": self.__api_key, "sample_id": analysis, "filenames": filenames}
        )
        analysis_files_reponse = requests.post(
            url=analysis_files_url, data=payload, headers=self.__auth_header
        )
        fp_data = analysis_files_reponse.json()
        filepaths_retrieved = fp_data["file_paths"]

        return filepaths_retrieved

    def get_s3_client(self):
        """Initialize a s3 client with Credentials picked from api-server

        :return: boto3 S3 client for downloading
        :rtype: boto3.resource
        """
        s3 = boto3.resource(
            "s3",
            aws_access_key_id=self.__access_key,
            aws_secret_access_key=self.__secret_key,
        )
        return s3
