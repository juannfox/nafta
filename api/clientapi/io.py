"""
Input/Output classes and methods.
"""
import re


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
