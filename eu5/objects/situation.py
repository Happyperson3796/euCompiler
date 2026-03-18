
from .embeddable import Embeddable
from ..pdxscript import get, format, Pair, Collection
import os
from .. import globals
from ..utils import gfx_utils, file_utils

class Situation(Embeddable):
    def get_embeddable(self):
        d = {"name": "$ROOT"}
        return d

    def run(self):
        head, tail = os.path.split(self.path)
        name = tail.removesuffix(".situation")

        with open(self.path, "r", encoding="utf-8-sig") as file:
            data = get(file.read())
        super().run(data, name, self.get_embeddable())

        situation = data[0][0]

        # map colors
        map_color_data = data[0][-1].get_pop("map")
        map_color = Collection()
        if_prefix = "if"
        legend_key = Collection()
        named_colors = Collection()

        for entry in map_color_data:
            key = entry[0]
            entry = entry[-1]

            map_color.append(Pair(if_prefix,"=",Collection(entry.get_pop_pair("limit"), Pair("value","=","map_"+key))))
            if_prefix = "else_if"

            legend_key.append(get(f"legend_key = {{ desc = {entry.get_pop('desc')} color = map_{key} require_color_on_map = yes }}")[0])

            named_colors.append(Pair("map_"+key, "= rgb", entry.get_pop("color")))

        if len(map_color) > 0: map_color.append(Pair("else","=",Collection(Pair("value","=","define:NMapColors|DEFAULT_COLOR"))))
        print(format(Collection()))

        data[0][-1].put(Pair("map_color","=",map_color))
        for x in legend_key: data[0][-1].append(x)

        file_utils.write_file("main_menu/common/named_colors/", name+"_map.txt", Collection(Pair("colors","=",named_colors)))
        
        # gui
        gui = None
        gui_template = data[0][-1].get_pop("gui_template", "")
        if not gui_template.is_empty():
            gui_template = gui_template.unquote()
            try:
                with open(globals.mod+"in_game/gui/panels/situation/"+gui_template, "r", encoding="utf-8-sig") as file:
                    gui = get(file.read())[0][-1]
            except:
                with open(globals.vanilla_path+"in_game/gui/panels/situation/"+gui_template, "r", encoding="utf-8-sig") as file:
                    gui = get(file.read())[0][-1]

        if gui == None:
            gui = data[0][-1].get_pop("gui")

        file_utils.write_file("in_game/gui/panels/situation/", situation+".gui", Pair("situation_panel","=",gui))

        # actions
        actions = data[0][-1].get_pop("actions", Collection())
        for action in actions:
            key = action[0]
            action = action[-1]

            first_select = -1
            for x in action.entries():
                first_select += 1
                if x[0] == "select_trigger":
                    break

            action.put(Pair("type","=","situation"), True)

            action.insert(first_select, get(
                f"""select_trigger = {{
                    looking_for_a = situation
                    interaction_source_list = {{
                        situation:{situation} = {{
                            add_to_list = source
                        }}
                    }}
                    target_flag = recipient
                    name = "choose_situation"
                    column = {{
                        data = name
                    }}
                    visible = {{
                        situation:{situation} = this
                        situation_is_active = yes
                    }}
                }}"""
            )[0])

        file_utils.write_file("in_game/common/generic_actions/", name+"_situation.action", actions)

        # situation file
        file_utils.write_file("in_game/common/situations/", name+".txt", data)

        


    def clean(self):
        head, tail = os.path.split(self.path)
        name = tail.removesuffix(".situation")

        with open(self.path, "r", encoding="utf-8-sig") as file:
            data = get(file.read())
        super().clean(data, name, self.get_embeddable())

        situation = data[0][0]

        try: os.remove(globals.mod+"main_menu/common/named_colors/"+name+"_map.txt")
        except: pass

        try: os.remove(globals.mod+"in_game/gui/panels/situation/"+situation+".gui")
        except: pass

        try: os.remove(globals.mod+"in_game/common/situations/"+name+".txt")
        except: pass
