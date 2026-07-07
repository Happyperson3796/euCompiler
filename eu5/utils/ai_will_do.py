from ..pdxscript import get, format, Pair, Collection

def preset(key):
    key = str(key)
    if key == "hostile_expansion": return hostile_expansion
    elif key == "always": return always
    elif key == "always_if_target": return always_if_target

always = get("""ai_will_do = {
    add = {
        value = 1000
        desc = "base chance"
    }
}""")[0]

always_if_target = get("""ai_will_do = {

    add = {
        value = 0
        desc = "base chance"
    }
    if = {
        limit = {
            exists = scope:target
        }
        add = {
            value = 1000
            desc = "exists"
        }
    }

}""")[0]

hostile_expansion = get("""ai_will_do = {
    add = {
        value = 13
        desc = "base chance"
    }
    if = {
        limit = {
            scope:actor = {
                has_truce_with = scope:target
            }
        }
        add = {
            value = -200
            desc = "truce"
        }
    }
    if = {
        limit = {
            exists = scope:target
        }
        if = {
            limit = {
                scope:actor = {
                    has_casus_belli_on = scope:target
                }
            }
            add = {
                value = -1000
                desc = "We already have a cb on them"
            }
        }
        if = {
            limit = {
                scope:actor = {
                    has_cooldown = press_claims_cooldown_key
                }
            }
            add = {
                value = scope:actor.stability
                desc = "[stability|e]"
            }
        }
    }
}""")[0]
