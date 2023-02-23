from dataclasses import dataclass
from enum import Enum
import logging
import re

from requests import request, JSONDecodeError, ConnectionError
from os import getenv


# Logging options
log_level = "DEBUG" if getenv("DEBUG") == "1" else "INFO"
logging.basicConfig(level=log_level)


class FileName():
    """
    A file name and it's components.
    """
    name: str
    extension: str

    def __init__(self, file_name: str):
        exp = r"^([\w\.\-]*)(\.)([a-zA-Z0-9]{1,4}$)"
        search = re.search(exp, file_name)
        if search is None:
            self.name = file_name
            self.extension = None
        else:
            self.name = search.group(1)
            self.extension = search.group(3)
    
    def __str__(self):
        ext = "" if self.extension is None else f".{self.extension}"
        return f"{self.name}{ext}"


@dataclass
class HttpClient:
    """
    A wrapper for HTTP requests from Python.
    """
    class HttpMethod(Enum):
        """
        HTTP Verbs/Methods
        """
        PUT = "Create"
        GET = "Read"
        POST = "Update"
        DELETE = "Delete"

    @staticmethod
    def http_request(url: str, method: HttpMethod = HttpMethod.GET):
        """
        An HTTP request
        """
        response = request(method.name, url)
        return response

    @staticmethod
    def api_call(url: str, method: HttpMethod = HttpMethod.GET):
        """
        An API call that expects JSON as response.
        """
        response = HttpClient.http_request(url, method)
        try:
            response = response.json()
        except JSONDecodeError:
            response = None
        return response


class DatasetResource():
    """
    A resource within the gov. API response.
    """
    name: str
    access_url: str
    url: str
    file_name: FileName

    def __init__(self, data: dict):
        try:
            self.name = data["name"]
            self.access_url = data["accessURL"]
            self.url = data["url"]
        except KeyError as exc:
            raise ValueError("Wrong data resource format.") from exc
        try:
            self.file_name = FileName(data["fileName"])
        except KeyError:
            self.file_name = None

    def __str__(self):
        return f"name: {self.name}\n" \
            + f"access_url: {self.access_url}\n" \
            + f"url: {self.url}\n" \
            + f"file_name: {self.file_name}"


class DatasetResponse():
    """
    A response from the Argentina's gov. API.
    """
    success: bool
    id: str
    resources: None

    def __init__(self, data: dict):
        try:
            self.success = data["success"]
            self.id = data["result"]["id"]
            resources = data["result"]["resources"]
            self.resources = []
            for resource in resources:
                self.resources.append(DatasetResource(resource))
        except KeyError as exc:
            raise ValueError("Wrong dataset format.") from exc

    def __str__(self):
        res = ""
        for resource in self.resources:
            res += f"---\n{resource.__str__()}\n"
        return f"success: {self.success}\n" \
            + f"id: {self.id}\n" \
            + f"resources: \n{res}"


@dataclass
class APIGobierno:
    """
    Argentina government's API (Foreign)
    """
    API_URL = "https://datos.gob.ar/api/3"
    DATASET_ID = "energia-precios-surtidor---resolucion-3142016"
    URL_PATHs = {"get_dataset": "action/package_show"}

    def datset_url(self):
        url = f"{self.API_URL}/{self.URL_PATHs['get_dataset']}" \
            + f"?id={self.DATASET_ID}"
        return url

    def is_online(self):
        try:
            HttpClient.http_request(self.API_URL)
            is_online = True
        except ConnectionError:
            is_online = False
        return is_online

    def get_dataset_metadata(self):
        response = HttpClient.api_call(self.datset_url())
        return DatasetResponse(response)


gov = APIGobierno()
print(gov.get_dataset_metadata())