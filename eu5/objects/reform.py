
from .embeddable import Embeddable
from ..pdxscript import get, format, Pair, Collection
import os
from .. import globals

class Reform(Embeddable):
    def get_embeddable(self):
        d = {"name": "$ROOT", "desc": "$ROOT_desc"}
        return d

    def run(self):
        head, tail = os.path.split(self.path)
        name = tail.removesuffix(".reform")

        with open(self.path, "r", encoding="utf-8-sig") as file:
            data = get(file.read())
        super().run(data, name, self.get_embeddable())

        os.makedirs(globals.mod+"in_game/common/government_reforms/", exist_ok=True)
        with open(globals.mod+"in_game/common/government_reforms/"+name+".txt", "w", encoding="utf-8-sig") as file:
            file.write(format(data))

        for p in data:
            key = p.key()
            if os.path.exists(head+"/"+key+".dds"):
                os.makedirs(globals.mod+"main_menu/gfx/interface/icons/government_reforms/illustrations/", exist_ok=True)
                try: os.remove(globals.mod+"main_menu/gfx/interface/icons/government_reforms/illustrations/"+key+".dds")
                except: pass
                os.rename(head+"/"+key+".dds", globals.mod+"main_menu/gfx/interface/icons/government_reforms/illustrations/"+key+".dds")


    def clean(self):
        head, tail = os.path.split(self.path)
        name = tail.removesuffix(".reform")

        with open(self.path, "r", encoding="utf-8-sig") as file:
            data = get(file.read())
        super().clean(data, name, self.get_embeddable())

        try: os.remove(globals.mod+"in_game/common/government_reforms/"+name+".txt")
        except: pass