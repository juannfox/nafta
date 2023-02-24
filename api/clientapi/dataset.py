"""
Dataset metadata and resource classes.
"""

from .io import FileName


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

    def get_resource(self, name: str):
        resource = None
        if self.resources is not None:
            for res in self.resources:
                if res.name == name:
                    resource = res
                    break
        return resource
