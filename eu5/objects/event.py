
from .embeddable import Embeddable
from ..pdxscript import get, format, Pair, Collection

class Event(Embeddable):
    def get_embeddable(self, id):
        return {"title":id+".title", "desc":id+".desc", "historical_info":id+".historical_info"}

    def run(self):
        with open(self.path, "r", encoding="utf-8-sig") as file:
            data = get(file.read())
        for x in data:
            id = x[0]
            filename = "events/"+".".join(id.split(".")[:-1])
            super().run(filename, x[-1], self.get_embeddable(id))

    def clean(self):
        with open(self.path, "r", encoding="utf-8-sig") as file:
            data = get(file.read())
        for x in data:
            id = x[0]
            filename = "events/"+".".join(id.split(".")[:-1])
            super().clean(filename, x[-1], self.get_embeddable(id))