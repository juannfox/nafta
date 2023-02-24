"""
Government's API client
"""
from dataclasses import dataclass

from .http import HttpClient
from .dataset import DatasetResponse


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

    def get_gas_prices_resource(self):
        try:
            dsmetadata = self.get_dataset_metadata()
            rsmetadata = dsmetadata.get_resource(self.RESOURCE_NAME)
            response = HttpClient.http_request(
                rsmetadata.url, stream=True
            )
        except KeyError:
            response = None
        return response
