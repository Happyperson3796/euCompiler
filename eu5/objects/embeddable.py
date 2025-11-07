from .filetype import fileType
from ..pdxscript import get, format, Pair, Collection
from ..utils.file_utils import Locfile

class Embeddable(fileType):

    def run(self, filename, data, embeddable: dict):
        self.embedded_loc = {}
        self.scan_data(data, embeddable)
        for x, y in self.embedded_loc.items():
            locfile = Locfile(filename)
            locfile.add(x, y)

    def clean(self, filename, data, embeddable: dict):
        self.embedded_loc = {}
        self.scan_data(data, embeddable)
        for x, y in self.embedded_loc.items():
            locfile = Locfile(filename)
            locfile.remove(x, y)

    def scan_data(self, obj, embeddable: dict):
        if isinstance(obj, Pair):
            self.scan_data(obj[-1], embeddable)
            for x, y in embeddable.items():
                if x == obj[0]:
                    self.embedded_loc[y] = obj[-1].unquote()
        elif isinstance(obj, Collection):
            for x in obj:
                self.scan_data(x, embeddable)