"""
A wrapper for HTTP interactions from Python.
"""
import logging
from dataclasses import dataclass
from enum import Enum

from requests import JSONDecodeError, request
from urllib3 import PoolManager
from urllib3 import exceptions as ul3exc


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
        timeout: int = 60,
    ):
        """
        An HTTP request
        """
        response = None
        pool = PoolManager()
        try:
            logging.debug("Attempting to download %s.", url)
            response = pool.request(
                "GET", url, preload_content=False, timeout=timeout
            )
        except ul3exc.MaxRetryError as exc:
            logging.error("Failed to download %s: %s", url, exc)
        return response
