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
            action_key = action[0]
            action_data: Collection = action[-1]

            ai_preset = action_data.get_pop("ai_preset", "")
            if not ai_preset.is_empty():
                action_data.append(ai_will_do.preset(ai_preset))

            for x in action_data.entries():
                if (x[0] == "select_country"):
                    x[0] = "select_trigger"
                    ed = get("""
				looking_for_a = country
				target_flag = target
				name = "choose_a_country"
				none_available_msg_key = "no_valid_countries"
                show_why_not_enabled = yes
				column = {
					data = name
				}""")
                    ed.reverse()
                    for y in ed: x[-1].insert(0, y)



        file_utils.write_file("in_game/common/generic_actions/", name+".txt", data)

        


    def clean(self):
        head, tail = os.path.split(self.path)
        name = tail.removesuffix(".action")

        with open(self.path, "r", encoding="utf-8-sig") as file:
            data = get(file.read())
        super().clean(data, name, self.get_embeddable())

        try: os.remove(globals.mod+"in_game/common/generic_actions/"+name+".txt")
        except: pass
