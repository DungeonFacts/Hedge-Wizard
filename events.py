from enum import Enum
from models import Slot, SlotFate, VerbBox, VerbBoxState
from cards import make_card
from content.events_data import EVENT_TEMPLATES

class EventState(Enum):
    PENDING = 1
    SUCCESS = 2
    FAILED = 3

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
        self.state = EventState.PENDING


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
        self.verbbox.start()
        self.verbbox.tick()
        self.acknowledged = False
        if self.deadline is not None:
            self.deadline -= 1


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


def make_event(event_key, templates=None):
    if templates is None:
        templates = EVENT_TEMPLATES
    t = templates[event_key]

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