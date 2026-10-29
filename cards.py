from content.cards_data import CARD_TEMPLATES

class Card:
    def __init__(self, name, tags=None, aspects=None):
        self.name = name
        self.tags = tags or set()
        self.aspects = aspects


    def __repr__(self):
        return f"Card('{self.name}', {self.tags})"


def make_card(key, templates=None):
    if templates is None:
        templates = CARD_TEMPLATES
    t = templates[key]
    return Card(t["name"], set(t["tags"]), t["aspects"])