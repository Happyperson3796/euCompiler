"""flavor_pol.51 = {
    type = country_event

    title = flavor_pol.51.title        # Title key.
    desc = flavor_pol.51.desc        # Description key
    historical_info = flavor_pol.51.historical_info    # (Optional) Historical Info key, responsible for the
    # historical information box
    # Title, desc and historical_info can be made dynamic and be made
    # dependent on triggers or randomized amongst a list of keys.


    # In EU5, mean_time_to_happen events do not exist and all events need to be either fired
    # either by on_actions, script or by a dynamic_historical_event clause.

    dynamic_historical_event = {
        tag = POL        # This event can fire for POL tag. There can be more than one “tag”s
        from = 1500.1.1    # This event can fire from 1500.1.1…
        to = 1510.1.1        #  … to 1510.1.1
        monthly_chance = 10 # with a monthly chance of 10%
    }

    trigger = {
        has_law = distribution_of_power_law     # only requirement for this event is to have “distribution_of_power_law“ available.
    }

    fire_only_once = yes         # This event can only fire once per campaign for any tag.

    illustration_tags = {        # Illustration tags that are used for the pops in the event picture
        10 = angry
        10 = interior
    }


    immediate = {
        # A scripted effect that saves two “pops” as saved scopes for the illustration purposes.
        event_illustration_estate_effect = { foreground = estate_type:nobles_estate background = estate_type:nobles_estate }
    }


    option = {
        name = flavor_pol.51.a    # key for the option.
                        # can also be made dynamic, but with a different syntax.


        historical_option = yes    # This will make AI with “Historical AI” gamerule
                        # always select this option


        if = {
            limit = {
                NOT = {
                    has_policy = dop_favor_the_nobles
                }
            }
            add_policy = policy:dop_favor_the_nobles
        }


        set_variable = unlock_nihil_novi    # set_variable is the unified solution of jomini for
                            # set_country_flag and variables.


        # grant the estate privilege under “estate_privilege:nihil_novi”
        # if this was a generic event, we could, for example, save a random privilege ahead of time
        # and assign it with a scope:target_privilege or a var:saved_privilege instead…
        grant_estate_privilege = estate_privilege:nihil_novi
    }


    option = {
        name = flavor_pol.51.b


        add_estate_satisfaction = {
            type = estate_type:nobles_estate
            value = estate_satisfaction_severe_penalty
        }
        add_stability = stability_severe_penalty
        # the values under “estate_satisfaction_severe_penalty” and “stability_severe_penalty” are
        # scripted - they are defined outside the file, are reusable, and can be made to depend on
        # dynamic factors.
    }
}"""

from .embeddable import Embeddable
from ..pdxscript import get, format, Pair, Collection

class Flag(Embeddable):
    def run(self):
        super().run()

    def clean(self):
        super().clean()

        #try:
        #    os.remove(head+"/"+name)
        #except: pass
