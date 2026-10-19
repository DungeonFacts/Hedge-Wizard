from models import Slot, SlotFate, VerbBox, VerbBoxState
from cards import make_card

class Event:
    def __init__(self, name, narrative_text="The text for this event has not been written.", deadline=None, slots=None, verbbox=None, becomes=None):
        self.name = name
        self.narrative_text = narrative_text
        self.deadline = deadline
        self.slots = slots
        self.verbbox = verbbox
        self.acknowledged = False
        self.becomes = becomes


    def __repr__(self):
        return f"Event({self.name},{self.deadline},{self.slots},{self.verbbox},{self.acknowledged},{self.becomes})"


    def has_verb_status(self):
        if self.verbbox is not None:
            return True


    def tick(self):
        if self.has_verb_status() is True and self.deadline > 0:
            status = self.verbbox.state
            if status == VerbBoxState.UNLOADED:
                pass #WIP
            elif status == VerbBoxState.LOADED:
                self.verbbox.start()
                self.verbbox.tick()
            elif status == VerbBoxState.RUNNING:
                self.verbbox.tick()
            elif status == VerbBoxState.COMPLETED:
                pass #WIP
            self.deadline -=1
        else:
            pass
            
EVENT_TEMPLATES = {
    "welcome":{
        "name":"Welcome",
        "narrative_text":"Welcome to Hedge Wizard. You are a wizard, and this card is you.",
        "deadline":None,
        "slots":[{"card":"wizard", "required_tags":{"wizard"}}],
        "verbbox":None,
        "becomes":"get_started"
        },
    "get_started":{
        "name":"Let's Get Started",
        "narrative_text":"In this game, you'll receive tasks to resolve by playing your cards. Let's start by having your wizard carve a totem.",
        "deadline":1,
        "slots":None,
        "verbbox":{"name":"A Wizard Is You", "slots":[{"required_tags":{"wizard"}}], "duration":0, "results":["totem"]},
        "becomes":None
        },
    "your_first_potion":{
        "name":"Brew Your First Potion",
        "narrative_text":"To get you started, here's a reagent you can brew into a potion. Place it in the slot below, and brew it!",
        "deadline":1,
        "slots":[{"card":"tea_leaves", "required_tags":{"reagent","raw_food"}}],
        "verbbox":{"name":"Brew Some Tea", "slots":[{"required_tags":{"reagent","raw_food"}}], "duration":0, "results":["tea"]},
        "becomes":None
        }
    }

def make_slot(slot_data):
    card = None
    if slot_data.get("card") is not None:
        card = make_card(slot_data["card"])
    return Slot(
        card=card,
        required_tags=set(slot_data.get("required_tags", set())),
        fate=slot_data.get("fate", SlotFate.KEEP),
        replacement=slot_data.get("replacement"),
    )


def make_event(event_key):
    t = EVENT_TEMPLATES[event_key]

    slots = None
    if t["slots"] is not None:
        slots = []
        for slot_data in t["slots"]:
            slots.append(make_slot(slot_data))

    verbbox = None
    if t["verbbox"] is not None:
        box_data = t["verbbox"]
        box_slots = []
        for slot_data in box_data["slots"]:
            box_slots.append(make_slot(slot_data))
        verbbox = VerbBox(
            name=box_data["name"],
            slots=box_slots,
            duration=box_data["duration"],
            results=list(box_data["results"]),
        )

    return Event(t["name"], t["narrative_text"], t["deadline"], slots, verbbox, t["becomes"])