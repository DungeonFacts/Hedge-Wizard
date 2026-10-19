from models import Slot, VerbBox, VerbBoxState
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
        if self.verbbox.state is not None:
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
        "verbbox":[{"name":"A Wizard Is You", "slots":[{"required_tags":{"wizard"}}], "duration":0, "results":["totem"]}],
        "becomes":None
        }
}


def make_event(event_key):
    t = EVENT_TEMPLATES[event_key]
    slots = []
    verbbox = []
    if t["slots"] is None and t["verbbox"] is None:
        return Event(t["name"], t["narrative_text"], t["deadline"], None, None, t["becomes"])
    if t["slots"] is not None and t["verbbox"] is None:
        for entry in t["slots"]:
            card = make_card(entry["card"])
            new_slot = Slot(required_tags=set(entry["required_tags"]))
            new_slot.place_card(card)
            slots.append(new_slot)
        return Event(t["name"], t["narrative_text"], t["deadline"], slots, None, t["becomes"])
    if t["slots"] is None and t["verbbox"] is not None:
        for entry in t["verbbox"]:
            verbbox.append(VerbBox(name=entry["name"], slots=[Slot(entry["slots"])], duration=entry["duration"], results=entry["results"]))
        return Event(t["name"], t["narrative_text"], t["deadline"], None, verbbox, t["becomes"])
    if t["slots"] is not None and t["verbbox"] is not None:
        for entry in t["slots"]:
                card = make_card(entry["card"])
                slots.append(Slot(card=card, required_tags=set(entry["required_tags"])))
                for entry in t["verbbox"]:
                    verbbox.append(VerbBox(name=entry["name"], slots=[Slot(entry["slots"])], duration=entry["duration"], results=entry["results"]))
        return Event(t["name"], t["narrative_text"], t["deadline"], slots, verbbox, t["becomes"])