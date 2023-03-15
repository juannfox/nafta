"""
A wrapper for HTTP interactions from Python.
"""
from dataclasses import dataclass
from enum import Enum
from urllib3 import PoolManager
from shutil import copyfileobj

from requests import JSONDecodeError, request


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
    def http_request(
        url: str,
        method: HttpMethod = HttpMethod.GET,
        stream: bool = False,
        timeout: int = 60,
    ):
        """
        An HTTP request
        """
        response = request(method.name, url, stream=stream, timeout=timeout)
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

    @staticmethod
    def http_download(
        url: str,
        # outfile: str,
        method: HttpMethod = HttpMethod.GET,
        timeout: int = 60,
    ):
        """
        An HTTP request
        """
        pool = PoolManager()
        response = pool.request(
            method.name, url,
            preload_content=False, timeout=timeout
        )
        # with pool.request(
        #     method.name, url,
        #     preload_content=False, timeout=timeout
        # ) as res, open(outfile, 'wb') as file_hwnd:
        #     copyfileobj(res, file_hwnd)
        return response
