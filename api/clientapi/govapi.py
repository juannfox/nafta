"""
Government's API client
"""
from dataclasses import dataclass

from .dataset import DatasetResponse
from .http import HttpClient


@dataclass
class APIGobierno:
    """
    Argentina government's API (Foreign)
    """

    API_URL = "https://datos.gob.ar/api/3"
    DATASET_ID = "energia-precios-surtidor---resolucion-3142016"
    URL_PATHs = {"get_dataset": "action/package_show"}
    RESOURCE_NAME = "Precios vigentes en surtidor - Resolución 314/2016"

    def datset_url(self):
        """
        Get the predefined Dataset's URL
        """
        url = (
            f"{self.API_URL}/{self.URL_PATHs['get_dataset']}"
            f"?id={self.DATASET_ID}"
        )
        return url

    def is_online(self):
        """
        Verify wether the foreign API service is online
        """
        try:
            HttpClient.http_request(self.API_URL)
            is_online = True
        except ConnectionError:
            is_online = False
        return is_online

    def get_dataset_metadata(self):
        """
        Challenge the foreign API to get metadata for the
        dataset.
        """
        response = HttpClient.api_call(self.datset_url())
        try:
            if isinstance(response, dict):
                dataset = DatasetResponse(response)
            else:
                raise RuntimeError(
                    "Unable to fetch Dataset" f"metadata. Got: {response}"
                )
        except ValueError as exc:
            raise RuntimeError(
                "Unable to parse Dataset" f"metadata. Got: {response}"
            ) from exc
        return dataset

    def get_gas_prices_resource(self):
        """
        Get the resource containing the gas-prices Dataset, as defined
        in the API's metadata response.
        """
        response = None
        try:
            dsmetadata = self.get_dataset_metadata()
            if dsmetadata is not None:
                rsmetadata = dsmetadata.get_resource(self.RESOURCE_NAME)
                if rsmetadata is not None:
                    response = HttpClient.http_download(
                        rsmetadata.url
                    )
        except KeyError:
            pass
        return response
