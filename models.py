from enum import Enum
from cards import make_card

class SlotFate(Enum):
    KEEP = 1
    CONSUME = 2
    REPLACE = 3
    SEIZE = 4


class Slot:
    def __init__(self, card=None, required_tags=None, required_aspects=None, fate=SlotFate.KEEP, replacement=None):
        self.card = card
        self.required_tags = required_tags or set()
        self.required_aspects = required_aspects
        self.fate = fate
        self.replacement = replacement


    def __repr__(self):
        return f"Slot({self.card},{self.required_tags},{self.fate},{self.replacement})"


    def is_filled(self):
        if self.card is not None:
            return True
        else:
            return False


    def meets_aspect_requirements(self, card):
        if self.required_aspects is not None:
            for aspect in self.required_aspects:
                if card.aspects.get(aspect) >= self.required_aspects.get(aspect):
                    return True
                else:
                    return False
        else:
            return True


    def place_card(self, card):
        requirements = [self.required_tags <= card.tags, self.meets_aspect_requirements(card), self.is_filled() == False]
        if all(requirements):
            self.card = card
            return True
        else:
            return False


    def force_card(self, card):
        self.card = card
        return True


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


    def __repr__(self):
        return f"VerbBox({self.name},{self.slots},{self.duration},{self.progress},{self.state},{self.results})"


    def add_slot(self, card=None, required_tags=None, fate=SlotFate.KEEP, replacement=None):
        new_slot = Slot(card=card, required_tags=required_tags, fate=fate, replacement=replacement)
        self.slots.append(new_slot)
        self.update_state()
        return new_slot


    def is_loaded(self):
        for slot in self.slots:
            if not slot.is_filled():
                return False
        return True


    def generate_results(self):
        for card_key in self.results:
            result_output = make_card(card_key)
            self.add_slot(card=result_output, required_tags=None)


    def fulfill_fate(self):
        for slot in self.slots:
            if slot.fate == SlotFate.CONSUME:
                self.remove_card(slot)
            if slot.fate == SlotFate.REPLACE:
                self.remove_card(slot)
                new_card = slot.replacement
                replacement = make_card(new_card)
                self.force_card(replacement, slot)


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

    def force_card(self, card, slot):
        if slot.force_card(card) is True:
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
                self.fulfill_fate()
                self.generate_results()
            return True
        else:
            return False