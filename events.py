from models import Slot, SlotFate, VerbBox, VerbBoxState
from cards import make_card

class Event:
    def __init__(self, name, narrative_text="The text for this event has not been written.", deadline=None, slots=None, verbbox=None, becomes=None, fails_to=None):
        self.name = name
        self.narrative_text = narrative_text
        self.deadline = deadline
        self.slots = slots
        self.verbbox = verbbox
        self.acknowledged = False
        self.becomes = becomes
        self.fails_to = fails_to


    def __repr__(self):
        return f"Event({self.name},{self.deadline},{self.slots},{self.verbbox},{self.acknowledged},{self.becomes},{self.fails_to})"


    def is_blocking(self):
        unread_message = False
        slot_blocking = False
        verb_blocking = False
        slot_empty = False
        if self.slots is not None:
            for index in range(len(self.slots)):
                if self.slots[index].is_filled() is True:
                    slot_blocking = True
                    break
                elif self.slots[index].is_filled() is False:
                    slot_empty = True              
        if self.verbbox is not None:
            if self.verbbox.state is VerbBoxState.COMPLETED:
                for index in range(len(self.verbbox.slots)):
                    if self.verbbox.slots[index].is_filled() is True:
                        verb_blocking = True
                        break
        if self.acknowledged is False:
            if self.slots is None and self.verbbox is None:
                unread_message = True
            elif self.slots is None and self.verbbox.state is VerbBoxState.COMPLETED:
                unread_message = True
            elif slot_empty is True and self.verbbox is None:
                unread_message = True
            elif slot_empty is True and self.verbbox.state is VerbBoxState.COMPLETED:
                unread_message = True
        blockers = [unread_message, slot_blocking, verb_blocking]
        if any(blockers):
            return True
        else:
            return False

        
    def ack(self):
            self.acknowledged = True
        
    
    def tick(self):
        succeeds = True
        self.verbbox.start()
        self.verbbox.tick()
        self.acknowledged = False
        if self.deadline is not None:
            self.deadline -= 1
            if self.deadline < (self.verbbox.duration - self.verbbox.progress):
                succeeds = False
        return succeeds



EVENT_TEMPLATES = {
    "intro":{
        "name":"Introduction",
        "narrative_text":"Welcome to Hedge Wizard. Click the button below to start the game.",
        "deadline":None,
        "slots":None,
        "verbbox":None,
        "becomes":"welcome",
        "fails_to":None
        },
    "welcome":{
        "name":"Welcome",
        "narrative_text":"This card represents you, the wizard. Click it to add it to your tableau.",
        "deadline":None,
        "slots":[{"card":"wizard", "required_tags":{"wizard"}}],
        "verbbox":None,
        "becomes":"get_started",
        "fails_to":None
        },
    "get_started":{
        "name":"Let's Get Started",
        "narrative_text":"In this game, you'll receive tasks to resolve by playing your cards. Let's start by having your wizard carve a totem.",
        "deadline":1,
        "slots":None,
        "verbbox":{
            "name":"A Wizard Is You",
            "slots":[{"required_tags":{"wizard"}}],
            "duration":0,
            "results":["totem"]
            },
        "becomes":None,
        "fails_to":None
        },
    "your_first_potion":{
        "name":"Brew Your First Potion",
        "narrative_text":"To get you started, here's a reagent you can brew into a potion. Place it in the slot below, and brew it!",
        "deadline":1,
        "slots":[{"card":"tea_leaves", "required_tags":{"reagent","raw_food"}}],
        "verbbox":{
            "name":"Brew Some Tea",
            "slots":[{"required_tags":{"reagent","raw_food"}, "fate":SlotFate.REPLACE, "replacement":"tea"}],
            "duration":1,
            "results":[]
            },
        "becomes":None,
        "fails_to":None
        },
    "carve_totem":{
        "name":"Carve A Totem",
        "narrative_text":"Any spare time can be spent carving totems, which are used in many rituals. They take a few turns, but you can interrupt the work at any time.",
        "deadline":None,
        "slots":None,
        "verbbox":{
            "name":"Carve a Totem",
            "slots":[{"required_tags":{"wizard"}}],
            "duration":2,
            "results":["totem"]
            },
        "becomes":"carve_totem",
        "fails_to":None
        },
    "sacrifice_totem":{
        "name":"Sacrifice A Totem",
        "narrative_text":"The spirits demand a sacrifice. Give them a totem before they grow angry!",
        "deadline":1,
        "slots":None,
        "verbbox":{
            "name":"Sacrifice a Totem",
            "slots":[{"required_tags":{"totem"}, "fate":SlotFate.CONSUME}],
            "duration":1,
            "results":[]
            },
        "becomes":None,
        "fails_to":"angry_spirits"
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

    return Event(t["name"], t["narrative_text"], t["deadline"], slots, verbbox, t["becomes"], t["fails_to"])