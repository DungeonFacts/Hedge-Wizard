from models import SlotFate
from enums import Way,Form

EVENT_TEMPLATES = {
    "upgrade_augury_reagent":{
        "name":"Upgrade Augury Reagent",
        "narrative_text":"This event upgrades augury reagents to the next tier",
        "deadline":None,
        "slots":None,
        "verbbox":{
            "name":"Upgrade Augury Reagent",
            "slots":[{"required_tags":{Form.REAGENT}, "required_aspects":{Way.AUGURY:1}, "fate":SlotFate.REPLACE, "replacement":"augury_reagent_2"},
                     {"required_tags":{Form.REAGENT}, "required_aspects":{Way.AUGURY:1}, "fate":SlotFate.CONSUME}],
            "duration":1,
            "results":[]
            },
        "becomes":"upgrade_augury_reagent",
        "fails_to":None
        }
}