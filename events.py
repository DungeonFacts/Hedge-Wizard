from models import Slot, VerbBox, VerbBoxState

class Event:
    def __init__(self, name, narrative_text="The text for this event has not been written.", deadline=None, verbbox=None, becomes=None):
        self.name = name
        self.narrative_text = narrative_text
        self.deadline = deadline
        self.verbbox = verbbox
        self.acknowledged = False
        self.becomes = becomes


    def __repr__(self):
        return f"Event({self.name},{self.deadline},{self.verbbox},{self.acknowledged},{self.becomes})"


    def has_verb_status(self):
        if self.verbbox.state is not None:
            return True


    def tick(self):
        if self.has_verb_status is True and self.deadline > 0:
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
        "verbbox":Slot(card="wizard", required_tags="wizard"),
        "becomes":"get_started"
        },
    "get_started":{
        "name":"Let's Get Started",
        "narrative_text":"In this game, you'll receive tasks to resolve by playing your cards. Let's start by having your wizard carve a totem.",
        "deadline":1,
        "verbbox":VerbBox("A Wizard Is You", slots=[Slot(required_tags="wizard")], duration=0, results="totem"),
        "becomes":None
        }
}


def spawn_event(event_key):
    t = EVENT_TEMPLATES[event_key]
    return Event(t["name"], t["narrative_text"], t["deadline"], t["verbbox"], t["becomes"])