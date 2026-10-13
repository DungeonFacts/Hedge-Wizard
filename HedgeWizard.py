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
        

        
## VALID_TAGS = {"expensive", "sacred", "raw_food", "cooked_food", "unpleasant"}

chicken = Card("Chicken", {"raw_food"})
sacred_oil = Card("Sacred Oil", {"sacred", "expensive"})
altar = Slot(required_tags={"sacred"})
assert altar.place_card(sacred_oil) is True  # Should return True since sacred_oil has the "sacred" tag
assert altar.is_filled() is True  # Should return True since the slot is now filled with sacred_oil
assert altar.place_card(sacred_oil) is False  # Should return False since the slot is already filled
assert altar.remove_card() is sacred_oil  # Should return the sacred_oil card that was removed
assert not altar.is_filled()  # Should return False since the slot is now empty
assert altar.place_card(chicken) is False  # Should return False since chicken does not have the "sacred" tag
assert not altar.is_filled()  # Should return False since the slot is still empty