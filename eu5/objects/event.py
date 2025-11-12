
from .embeddable import Embeddable
from ..pdxscript import get, format, Pair, Collection
import os
from .. import globals

class Event(Embeddable):
    def get_embeddable(self):
        d = {"title": "$R$.title", "desc": "$R$.desc", "historical_info": "$R$.historical_info"}
        for x in ["a","b","c","d","e","f","g","h","i","j","k"]: d[x] = ["$R$."+x, "name"]
        return d

    def run(self):
        locfile = "events/"+self.path.split("\\")[-1].removesuffix(".event")
        with open(self.path, "r", encoding="utf-8-sig") as file:
            data = get(file.read())
        super().run(data, locfile, self.get_embeddable())

        os.makedirs(globals.mod+"in_game/events/", exist_ok=True)
        with open(globals.mod+"in_game/events/"+self.path.split("\\")[-1].removesuffix(".event")+".txt", "w", encoding="utf-8-sig") as file:
            file.write(format(data))

    def clean(self):
        locfile = "events/"+self.path.split("\\")[-1].removesuffix(".event")
        with open(self.path, "r", encoding="utf-8-sig") as file:
            data = get(file.read())
        super().clean(data, locfile, self.get_embeddable())

        try: os.remove(globals.mod+"in_game/events/"+self.path.split("\\")[-1].removesuffix(".event")+".txt")
        except: pass