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

    def is_empty(self):
        return self.card is None

    def place_card(self, card):
        if not self.is_empty():
            raise ValueError("Slot is already occupied.")
        self.card = card

    def remove_card(self):
        if self.is_empty():
            raise ValueError("Slot is already empty.")
        removed_card = self.card
        self.card = None
        return removed_card

    def is_filled(self):
        if not self.is_empty():
            print (f"Slot is filled with card: {self.card.name}")

VALID_TAGS = {"expensive", "sacred", "raw_food", "cooked_food", "unpleasant"}

chicken = Card("Chicken", {"raw_food"})
sacred_oil = Card("Sacred Oil", {"sacred", "expensive"})

altar = Slot(required_tags={"sacred"})
altar.place_card(sacred_oil)

print(chicken.name, chicken.tags)
print(sacred_oil.name, sacred_oil.tags)
print(altar.is_filled())