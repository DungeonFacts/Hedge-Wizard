from enum import Enum

class Card:
    def __init__(self, name, tags=None):
        self.name = name
        self.tags = tags or set()

    def has_tag(self, tag):
        return tag in self.tags

class Slot:
    def __init__(self, card=None, required_tags=None):
        self.card = card
        self.required_tags = required_tags or set()

    def is_filled(self):
        if self.card is not None:
            return True
        else:
            return False


    def place_card(self, card):
        if self.required_tags <= card.tags and not self.is_filled():
            self.card = card
            return True
        else:
            return False


    def remove_card(self):
        if self.is_filled():
            removed_card = self.card
            self.card = None
            return removed_card

class VerbBoxState(Enum):
    UNLOADED = 1
    LOADED = 2
    RUNNING = 3
    COMPLETED = 4

class VerbBox:
    def __init__(self, name, slots=None, duration=1):
        self.name = name
        self.slots = slots or []
        self.duration = duration
        self.progress = 0
        self.state = VerbBoxState.UNLOADED

    def is_loaded(self):
        for slot in self.slots:
            if not slot.is_filled():
                return False
        return True

    def update_state(self):
        loaded = self.is_loaded()
        if self.state == VerbBoxState.COMPLETED:
            pass
        elif loaded and self.state == VerbBoxState.UNLOADED:
            self.state = VerbBoxState.LOADED
        elif not loaded:
            self.state = VerbBoxState.UNLOADED


    def place_card(self, card, slot_name):
        if Slot.place_card(card, slot_name) is True:
            self.update_state()
            return True
        else:
            return False

    def remove_card(self, slot_name):
        if Slot.remove_card(slot_name) is not None:
            self.update_state()
            return True
        else:
            return False

    def start(self):
        if self.is_loaded() and self.state == VerbBoxState.LOADED:
            self.state = VerbBoxState.RUNNING
            return True
        else:
            return False

    def tick(self):
        self.update_state()
        if self.state == VerbBoxState.RUNNING:
            self.progress += 1
            if self.progress >= self.duration:
                self.state = VerbBoxState.COMPLETED
            return True
        else:
            return False

## VALID_TAGS = {"expensive", "sacred", "raw_food", "cooked_food", "unpleasant"}

chicken = Card("Chicken", {"raw_food"})
sacred_oil = Card("Sacred Oil", {"sacred", "expensive"})
altar_slot = Slot(required_tags={"sacred"})
altar = VerbBox("Altar", slots=[altar_slot], duration=1)

assert altar_slot.place_card(sacred_oil) is True  # Should return True since sacred_oil has the "sacred" tag
assert altar_slot.is_filled() is True  # Should return True since the slot is now filled with sacred_oil
assert altar_slot.place_card(sacred_oil) is False  # Should return False since the slot is already filled
assert altar_slot.remove_card() is sacred_oil  # Should return the sacred_oil card that was removed
assert not altar_slot.is_filled()  # Should return False since the slot is now empty
assert altar_slot.place_card(chicken) is False  # Should return False since chicken does not have the "sacred" tag
assert not altar_slot.is_filled()  # Should return False since the slot is still empty
assert altar.start() is False  # Should return False since the slot is not filled
assert altar.place_card(sacred_oil, altar_slot) is True  # Should return True since sacred_oil has the "sacred" tag
assert altar.tick() is False  # Should return False since the verb box is not running
assert altar.start() is True  # Should return True since the slot is now filled
assert altar.start() is False  # Should return False since the verb box is already running
assert altar.tick() is True  # Should return True since the verb box is running
assert altar.progress == 1  # Should return True since the progress is now 1
assert altar.tick() is False  # Should return False since the verb box is completed