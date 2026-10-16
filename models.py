from enum import Enum
from cards import make_card

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
    def __init__(self, name, slots=None, duration=1, results=None):
        self.name = name
        self.slots = slots or []
        self.duration = duration
        self.progress = 0
        self.state = VerbBoxState.UNLOADED
        self.results = results or []


    def add_slot(self, card=None, required_tags=None):
        new_slot = Slot(card=card, required_tags=required_tags)
        self.slots.append(new_slot)
        self.update_state()
        return new_slot


    def is_loaded(self):
        for slot in self.slots:
            if not slot.is_filled():
                return False
        return True


    def generate_results(self):
        if self.results is not None:
            for card_key in self.results:
                result_output = make_card(card_key)
                self.add_slot(card=result_output, required_tags=None)


    def update_state(self):
        loaded = self.is_loaded()
        if self.state == VerbBoxState.COMPLETED:
            pass
        elif loaded and self.state == VerbBoxState.UNLOADED:
            self.state = VerbBoxState.LOADED
        elif not loaded:
            self.state = VerbBoxState.UNLOADED


    def place_card(self, card, slot):
        if slot.place_card(card) is True:
            self.update_state()
            return True
        else:
            return False


    def remove_card(self, slot):
        removed_card = slot.remove_card()
        if removed_card is not None:
            self.update_state()
            return removed_card


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
                self.generate_results()
            return True
        else:
            return False