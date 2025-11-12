
from .embeddable import Embeddable
from ..pdxscript import get, format, Pair, Collection
import os
from .. import globals

class Event(Embeddable):
    def get_embeddable(self, id):
        d = {"title": id+".title", "desc": id+".desc", "historical_info": id+".historical_info"}
        for x in ["a","b","c","d","e","f","g","h","i","j","k"]: d[x] = [id+"."+x, "name"]
        return d

    def run(self):
        locfile = "events/"+self.path.split("\\")[-1].removesuffix(".event")
        with open(self.path, "r", encoding="utf-8-sig") as file:
            data = get(file.read())
        e = {}
        for x in data:
            id = x[0]
            e.update(self.get_embeddable(id))
        super().run(data, locfile, e)

        os.makedirs(globals.mod+"in_game/events/", exist_ok=True)
        with open(globals.mod+"in_game/events/"+self.path.split("\\")[-1].removesuffix(".event")+".txt", "w", encoding="utf-8-sig") as file:
            file.write(format(data))

    def clean(self):
        locfile = "events/"+self.path.split("\\")[-1].removesuffix(".event")
        with open(self.path, "r", encoding="utf-8-sig") as file:
            data = get(file.read())
        e = {}
        for x in data:
            id = x[0]
            e.update(self.get_embeddable(id))
        super().clean(data, locfile, e)

        try: os.remove(globals.mod+"in_game/events/"+self.path.split("\\")[-1].removesuffix(".event")+".txt")
        except: pass