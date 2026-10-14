class Card:
    def __init__(self, name, tags=None):
        self.name = name
        self.tags = tags or set()

CARD_TEMPLATES = {
    "wizard":{"name":"Wizard","tags":{"wizard"}},
    "totem":{"name":"Totem","tags":{"totem"}},
    "sacred_oil":{"name":"Sacred Oil", "tags":{"expensive","sacred"}},
}

def make_card(key):
    t = CARD_TEMPLATES[key]
    return Card(t["name"], set(t["tags"]))