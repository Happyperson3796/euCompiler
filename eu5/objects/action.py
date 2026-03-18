from .embeddable import Embeddable
from ..pdxscript import get, format, Pair, Collection
import os
from .. import globals
from ..utils import gfx_utils, file_utils, ai_will_do

class Action(Embeddable):
    def get_embeddable(self):
        d = {"name": "$ROOT", "desc": "$ROOT_desc"}
        return d

    def run(self):
        head, tail = os.path.split(self.path)
        name = tail.removesuffix(".action")

        with open(self.path, "r", encoding="utf-8-sig") as file:
            data = get(file.read())
        super().run(data, name, self.get_embeddable())

        for action in data.entries():
            ai_preset = action[-1].get_pop("ai_preset", "")
            if not ai_preset.is_empty():
                action[-1].append(ai_will_do.preset(ai_preset))

        file_utils.write_file("in_game/common/generic_actions/", name+".txt", data)

        


    def clean(self):
        head, tail = os.path.split(self.path)
        name = tail.removesuffix(".action")

        with open(self.path, "r", encoding="utf-8-sig") as file:
            data = get(file.read())
        super().clean(data, name, self.get_embeddable())

        try: os.remove(globals.mod+"in_game/common/generic_actions/"+name+".txt")
        except: pass
