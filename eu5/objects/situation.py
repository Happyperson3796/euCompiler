
from .embeddable import Embeddable
from ..pdxscript import get, format, Pair, Collection
import os, shutil
from .. import globals
from ..utils import gfx_utils, file_utils
from .action import Action

class Situation(Embeddable):
    def get_embeddable(self):
        d = {"name": "$ROOT", "desc": "$ROOT_desc"}
        return d

    def run(self):
        head, tail = os.path.split(self.path)
        name = tail.removesuffix(".situation")

        with open(self.path, "r", encoding="utf-8-sig") as file:
            data = get(file.read())
        super().run(data, name, self.get_embeddable())

        situation = data[0][0]

        on_start: Collection = data[0][-1].get("on_start")
        on_monthly: Collection = data[0][-1].get("on_monthly")
        on_ended: Collection = data[0][-1].get("on_ended")

        factions = data[0][-1].get_pop("factions")
        # map colors
        map = data[0][-1].get_pop("map")
        map_2 = data[0][-1].get_pop("secondary_map_color")
        faction_tags = {}
        map_color = Collection()
        secondary_map_color = Collection()
        if_prefix = "if"
        legend_key = Collection()
        named_colors = Collection()

        def map_key(entry, faction = False, secondary = False):
            nonlocal legend_key
            nonlocal named_colors
            nonlocal map_color
            nonlocal secondary_map_color
            nonlocal if_prefix
            nonlocal faction_tags
            key = entry[0]
            entry = entry[-1]

            limit = entry.get_pop_pair("limit")

            if (faction):
                faction_tags[key] = limit.copy()
                limit[-1] = Collection(Pair("owner","?=",limit[-1]))

            if not secondary:
                map_color.append(Pair(if_prefix,"=",Collection(limit, Pair("value","=","map_situation_"+key))))
            else:
                secondary_map_color.append(Pair(if_prefix,"=",Collection(limit, Pair("value","=","map_situation_"+key))))
            if_prefix = "else_if"

            if f"map_situation_{key}" not in str(legend_key): 
                legend_key.append(get(f"legend_key = {{ desc = {entry.get_pop('desc')} color = map_situation_{key} require_color_on_map = yes }}")[0])
                named_colors.append(Pair("map_situation_"+key, "= rgb", entry.get_pop("color")))

        for entry in factions:
            key = entry[0]
            limit = entry[-1].get_pair("limit").copy()
            limit[0] = "AND"

            strongest = f"""
                ordered_country = {{
                    limit = {{
                        {format(limit)}
                    }}
                    order_by = great_power_score
                    max = 1
                    check_range_bounds = no
                    situation:{situation} = {{
                        set_variable = {{
                            name = strongest_{key}
                            value = prev
                        }}
                    }}
                }}"""
            
            members = f"""
                clear_global_variable_list = situation_var_faction_{key}
                ordered_country = {{
                    limit = {{
                        {format(limit)}
                    }}
                    order_by = great_power_score
                    max = 999
                    check_range_bounds = no
                    save_temporary_scope_as = target_country
                    add_to_global_variable_list = {{ name = situation_var_faction_{key}  target = scope:target_country }}
                }}"""
            
            on_start.append(get(strongest)[0])
            on_start.append(get(members)[0])
            on_start.append(get(members)[1])
            on_monthly.append(get(strongest)[0])
            on_monthly.append(get(members)[0])
            on_monthly.append(get(members)[1])
            on_ended.append(get(f"clear_global_variable_list = situation_var_faction_{key}")[0])
            
            map_key(entry, True)

        for entry in map:
            map_key(entry)

        if_prefix = "if"
        for entry in map_2:
            map_key(entry, False, True)

        if len(map_color) > 0: map_color.append(Pair("else","=",Collection(Pair("value","=","define:NMapColors|DEFAULT_COLOR"))))

        data[0][-1].put(Pair("map_color","=",map_color))
        if len(secondary_map_color) > 0: data[0][-1].put(Pair("secondary_map_color","=",secondary_map_color))
        for x in legend_key: data[0][-1].append(x)

        file_utils.write_file("main_menu/common/named_colors/", name+"_situation_map.txt", Collection(Pair("colors","=",named_colors)))
        
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
            print(head+"/"+situation+".gui")
            if os.path.exists(head+"/"+situation+".gui"):
                os.makedirs(globals.mod+"/in_game/gui/panels/situation/", exist_ok=True)
                shutil.move(head+"/"+situation+".gui", globals.mod+"/in_game/gui/panels/situation/"+situation+".gui")
            else:
                file_utils.write_file("in_game/gui/panels/situation/", situation+".gui", Pair("situation_panel","=",gui))

        # actions
        actions = data[0][-1].get_pop("actions", Collection())
        actions = format(actions).replace("faction = ", "faction=").replace("faction =", "faction=").replace("faction= ", "faction=")
        faction_tags["any"] = Pair("OR","=",Collection())
        for faction, limit in faction_tags.items():
            if faction != "any":
                if limit[0] == "limit": limit[0] = "AND"
                faction_tags["any"][-1].append(limit)
        for faction, limit in faction_tags.items():
            if limit[0] == "limit": limit[0] = "AND"
            actions = actions.replace("faction="+faction, str(limit))
        actions = get(actions)
        for action in actions:
            key = action[0]
            action = action[-1]

            first_select = 0
            for x in action.entries():
                first_select += 1
                if x[0].startswith("select_"):
                    break

            action.put(Pair("type","=","situation"), True)

            visible = "scope:actor={ "+format(action.get_pop("visible"))+" }"

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
                        {visible}
                    }}
                }}"""
            )[0])

        file_utils.write_file("in_game/common/generic_actions/", name+"_situation_actions.action", actions)

        # situation file
        file_utils.write_file("in_game/common/situations/", name+".txt", data)

        if os.path.exists(head+"/"+situation+"/"):
            if os.path.exists(head+"/"+situation+"/illustrations/"):
                shutil.copytree(head+"/"+situation+"/illustrations/", globals.mod+"/main_menu/gfx/interface/illustrations/situation/", dirs_exist_ok=True)
            if os.path.exists(head+"/"+situation+"/icons/"):
                shutil.copytree(head+"/"+situation+"/icons/", globals.mod+"/main_menu/gfx/interface/icons/situations/", dirs_exist_ok=True)

        


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
